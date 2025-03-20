# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
import grpc
from sqlalchemy.orm import Session
from typing import List
#from grpc_reflection.v1alpha import reflection

import sys

from google.protobuf.timestamp_pb2 import Timestamp
#from ..generated import certificate_pb2
#from ..generated import certificate_pb2_grpc
from generated import certificate_pb2
from generated import certificate_pb2_grpc
import datetime
import json
from google.protobuf.json_format import MessageToDict


from common.utils import generateRandomId
#from .db import CertificateDB
from .db import get_db, Certificate, UserCertificate, create_certificate, issue_certificate, get_user_certificates, update_certificate, update_user_certificate, get_all_certificates 
#from .fabric_gateway import FabricClient



#fabric_client = FabricClient()  # Blockchain client instance

def datetime_to_proto(dt: datetime.datetime) -> Timestamp:
        """Converts a Python datetime to a protobuf Timestamp."""
        ts = Timestamp()
        ts.FromDatetime(dt)
        return ts

class CertificateService(certificate_pb2_grpc.CertificateService):
    def __init__(self):
        self.db = next(get_db())

    async def CreateCertificate(self, request, context):
        """Creates a new generic certificate and stores it in the database."""

        # For optional int32 fields in proto3, if they are not provided, they default to 0.
        # We interpret a 0 value as "not set" and convert it to None.
        course_id = request.courseId if request.courseId != 0 else None
        years_valid = request.yearsValid if request.yearsValid != 0 else None

        # Parse additionalInfo: convert the JSON string to a dict.
        additional_info = json.loads(request.additionalInfo) if request.additionalInfo else {}

        # Create the certificate in the database.
        new_cert = create_certificate(
            db=self.db,
            name=request.name,
            course_id=course_id,
            years_valid=years_valid,
            description=request.description,
            additional_info=additional_info
        )

        # Debug logs.
        print(f"✅ Created Certificate: {new_cert}")
        print(f"🆔 Certificate ID: {new_cert.id}")
        print(f"📜 Attributes: {vars(new_cert)}")

        # Return the created certificate in the gRPC response.
        # Note: We return integers for courseId and yearsValid as defined in your .proto file.
        return certificate_pb2.CertificateData(
            id=new_cert.id,
            name=new_cert.name,
            courseId=new_cert.course_id if new_cert.course_id is not None else 0,
            yearsValid=new_cert.years_valid if new_cert.years_valid is not None else 0,
            description=new_cert.description if new_cert.description else "",
            additionalInfo=json.dumps(new_cert.additional_info) if new_cert.additional_info else "{}"
        )
    
    

    async def IssueCertificate(self, request, context):
        """
        Issues a certificate to a user based on an existing generic certificate,
        and returns the issued certificate data.
        
        Expects the following fields in the request:
        - userId (int)
        - certId (int)
        - issuedOn (Timestamp)
        - expiresOn (Timestamp, optional)
        - additionalInfo (JSON string, optional)
        """
        # Convert the issuedOn proto timestamp to a Python datetime.
        issued_on = datetime.datetime.fromtimestamp(
            request.issuedOn.seconds + request.issuedOn.nanos / 1e9
        )
        
        # Convert expiresOn to datetime if provided; else use None.
        expires_on = (
            datetime.datetime.fromtimestamp(
                request.expiresOn.seconds + request.expiresOn.nanos / 1e9
            ) if request.HasField("expiresOn") else None
        )

        # Parse the additionalInfo JSON string into a dictionary.
        additional_info = json.loads(request.additionalInfo) if request.additionalInfo else {}

        try:
            # Issue the certificate using the db helper function.
            new_user_cert = issue_certificate(
                db=self.db,
                user_id=request.userId,
                cert_id=request.certId,
                issued_on=issued_on,
                expires_on=expires_on,
                additional_info=additional_info
            )
        except ValueError as e:
            # If the certificate does not exist or another error occurs,
            # set gRPC context details and return an empty response.
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return certificate_pb2.UserCertificateData()

        # Debug logs.
        print(f"✅ Issued Certificate: {new_user_cert}")
        print(f"🆔 User Certificate ID: {new_user_cert.id}")
        print(f"📜 Attributes: {vars(new_user_cert)}")

        # Convert datetimes back to proto timestamps for the response.
        issued_on_proto = datetime_to_proto(new_user_cert.issued_on)
        expires_on_proto = datetime_to_proto(new_user_cert.expires_on) if new_user_cert.expires_on else None

        # Return the issued certificate data.
        # Assumes your proto message `UserCertificateData` includes fields:
        # id, userId, certId, issuedOn, expiresOn, and additionalInfo.
        return certificate_pb2.UserCertificateData(
            id=new_user_cert.id,
            userId=new_user_cert.user_id,
            certId=new_user_cert.cert_id,
            issuedOn=issued_on_proto,
            expiresOn=expires_on_proto,
            additionalInfo=json.dumps(new_user_cert.additional_info) if new_user_cert.additional_info else "{}"
        )
    
    async def GetUserCertificates(self, request, context):
        """
        Retrieves all certificates associated with a given user.
        Expects the request to have a field:
          - userId (string) -> which will be cast to an integer
        Returns a UserCertificateList containing the user's certificates.
        """
        # Convert userId from string to int.
        try:
            user_id = int(request.userId)
        except ValueError as e:
            context.set_details("Invalid userId: " + str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return certificate_pb2.UserCertificateList()

        try:
            user_certs = get_user_certificates(self.db, user_id)
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return certificate_pb2.UserCertificateList()

        # Convert each database UserCertificate object into a proto message.
        user_certificates_proto = []
        for cert in user_certs:
            issued_on_proto = datetime_to_proto(cert.issued_on)
            expires_on_proto = datetime_to_proto(cert.expires_on) if cert.expires_on else None

            user_cert = certificate_pb2.UserCertificateData(
                id=cert.id,
                userId=cert.user_id,
                certId=cert.cert_id,
                issuedOn=issued_on_proto,
                expiresOn=expires_on_proto,
                additionalInfo=json.dumps(cert.additional_info) if cert.additional_info else "{}"
            )
            user_certificates_proto.append(user_cert)

        # Return the list of user certificates.
        return certificate_pb2.UserCertificateList(userCertificates=user_certificates_proto)
    
    async def UpdateCertificate(self, request, context):
        """
        Updates an existing generic certificate.
        Expects fields:
          - id (int) for the certificate to update
          - name, courseId, yearsValid, description, additionalInfo (optional)
        """
        # Convert optional fields: treat 0 as None for int fields.
        course_id = request.courseId if request.courseId != 0 else None
        years_valid = request.yearsValid if request.yearsValid != 0 else None
        additional_info = json.loads(request.additionalInfo) if request.additionalInfo else None

        try:
            updated_cert = update_certificate(
                db=self.db,
                certificate_id=request.id,
                name=request.name if request.name else None,
                course_id=course_id,
                years_valid=years_valid,
                description=request.description if request.description else None,
                additional_info=additional_info
            )
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return certificate_pb2.CertificateData()

        return certificate_pb2.CertificateData(
            id=updated_cert.id,
            name=updated_cert.name,
            courseId=updated_cert.course_id if updated_cert.course_id is not None else 0,
            yearsValid=updated_cert.years_valid if updated_cert.years_valid is not None else 0,
            description=updated_cert.description if updated_cert.description else "",
            additionalInfo=json.dumps(updated_cert.additional_info) if updated_cert.additional_info else "{}"
        )

    async def GetAllCertificates(self, request, context):
        """
        Retrieves all certificates from the database.
        Returns a CertificateList containing all certificates.
        """
        try:
            # Fetch all certificates from the database
            all_certs = get_all_certificates(self.db)
        except Exception as e:
            context.set_details("Error retrieving certificates: " + str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return certificate_pb2.CertificateList()

        # Convert each database Certificate object into a proto message.
        certificates_proto = []
        for cert in all_certs:
            # Convert any fields if necessary (e.g., additional_info can be converted to JSON).
            additional_info_proto = json.dumps(cert.additional_info) if cert.additional_info else "{}"

            certificate_proto = certificate_pb2.CertificateData(
                id=cert.id,
                name=cert.name,
                yearsValid=cert.years_valid,
                description=cert.description,
                additionalInfo=additional_info_proto,
                courseId=cert.course_id
            )
            certificates_proto.append(certificate_proto)

        # Return the list of certificates.
        return certificate_pb2.CertificateList(certificates=certificates_proto)

    async def UpdateUserCertificate(self, request, context):
        """
        Updates an existing user-issued certificate.
        Expects fields:
          - id (int) for the user certificate record to update
          - userId, certId, issuedOn, expiresOn, additionalInfo (optional)
        """
        # For timestamps, check if provided. If not, pass None.
        issued_on = None
        if request.HasField("issuedOn"):
            issued_on = datetime.datetime.fromtimestamp(
                request.issuedOn.seconds + request.issuedOn.nanos / 1e9
            )
        expires_on = None
        if request.HasField("expiresOn"):
            expires_on = datetime.datetime.fromtimestamp(
                request.expiresOn.seconds + request.expiresOn.nanos / 1e9
            )
        additional_info = json.loads(request.additionalInfo) if request.additionalInfo else None

        try:
            updated_user_cert = update_user_certificate(
                db=self.db,
                user_cert_id=request.id,
                user_id=request.userId if request.userId != 0 else None,
                cert_id=request.certId if request.certId != 0 else None,
                issued_on=issued_on,
                expires_on=expires_on,
                additional_info=additional_info
            )
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return certificate_pb2.UserCertificateData()

        issued_on_proto = datetime_to_proto(updated_user_cert.issued_on)
        expires_on_proto = datetime_to_proto(updated_user_cert.expires_on) if updated_user_cert.expires_on else None

        return certificate_pb2.UserCertificateData(
            id=updated_user_cert.id,
            userId=updated_user_cert.user_id,
            certId=updated_user_cert.cert_id,
            issuedOn=issued_on_proto,
            expiresOn=expires_on_proto,
            additionalInfo=json.dumps(updated_user_cert.additional_info) if updated_user_cert.additional_info else "{}"
        )
    

'''
    async def IssueCertificate(self, request, context):
        """Issues a certificate to a user and adds it to the blockchain."""
        issued_cert = issue_certificate(
            db=self.db,
            user_id=int(request.userId),
            cert_id=int(request.certificateId),
            issued_on=datetime.strptime(request.issuedOn, "%Y-%m-%d"),
            expires_on=datetime.strptime(request.expiresOn, "%Y-%m-%d"),
            additional_info=json.loads(request.additionalInfo) if request.additionalInfo else {}
        )

        if not issued_cert:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Base certificate not found in database.")
            return certificate_pb2.UserCertificateData()

        # Issue certificate in blockchain
        success = fabric_client.create_certificate(
            certificate_id=str(issued_cert.id),
            #name=issued_cert.cert_info.name,
            course_id=str(issued_cert.cert_info.course_id),
            owner=str(issued_cert.user_id)
        )

        if not success:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to write certificate to blockchain.")
            return certificate_pb2.UserCertificateData()

        return certificate_pb2.UserCertificateData(
            id=str(issued_cert.id),
            userId=str(issued_cert.user_id),
            certificateId=str(issued_cert.cert_id),
            issuedOn=issued_cert.issued_on.strftime("%Y-%m-%d"),
            expiresOn=issued_cert.expires_on.strftime("%Y-%m-%d"),
            additionalInfo=json.dumps(issued_cert.additional_info) if issued_cert.additional_info else "{}"
        )

    async def GetUserCertificates(self, request, context):
        """Fetches all certificates owned by a user."""
        user_certificates = get_user_certificates(self.db, int(request.userId))
        if not user_certificates:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No certificates found for user.")
            return certificate_pb2.UserCertificateList()

        return certificate_pb2.UserCertificateList(
            userCertificates=[
                certificate_pb2.UserCertificateData(
                    id=str(cert.id),
                    userId=str(cert.user_id),
                    certificateId=str(cert.cert_id),
                    issuedOn=cert.issued_on.strftime("%Y-%m-%d"),
                    expiresOn=cert.expires_on.strftime("%Y-%m-%d"),
                    additionalInfo=cert.additional_info or ""
                )
                for cert in user_certificates
            ]
        )
'''
async def serve():
    server = grpc.aio.server()
    certificate_pb2_grpc.add_CertificateServiceServicer_to_server(CertificateService(), server)


    
    listen_addr = "[::]:50055"
    server.add_insecure_port(listen_addr)
    logging.info("Starting gRPC server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())



'''
    # Enable reflection
    SERVICE_NAMES = (
        certificate_pb2.DESCRIPTOR.services_by_name['CertificateService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
'''