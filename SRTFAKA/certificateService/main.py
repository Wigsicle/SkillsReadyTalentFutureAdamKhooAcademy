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



from ..generated import certificate_pb2
from ..generated import certificate_pb2_grpc
#from SRTFAKA.generated import certificate_pb2
#from SRTFAKA.generated import certificate_pb2_grpc
from datetime import datetime
import json



from ..common.utils import generateRandomId
#from .db import CertificateDB
from .db import get_db, Certificate, UserCertificate, create_certificate, issue_certificate, get_user_certificates
from .fabric_gateway import FabricClient

fabric_client = FabricClient()  # Blockchain client instance

class CertificateService(certificate_pb2_grpc.CertificateService):
    def __init__(self):
        self.db = next(get_db())

    async def CreateCertificate(self, request, context):
        """Creates a new generic certificate and stores it in the database."""

        new_cert = create_certificate(
            db=self.db,
            name=request.name,
            course_id=int(request.courseId),
            validity_period=datetime.strptime(request.validityPeriod, "%H:%M:%S"),
            description=request.description,
            additional_info=request.additionalInfo
        )
        return certificate_pb2.CertificateData(
            id=str(new_cert.id),
            name=new_cert.name,
            courseId=str(new_cert.course_id),
            validityPeriod=new_cert.validity_period.strftime("%H:%M:%S"),
            description=new_cert.description,
            additionalInfo=json.dumps(new_cert.additional_info) if new_cert.additional_info else "{}"  # Convert to JSON string
        )

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

async def serve():
    server = grpc.aio.server()
    certificate_pb2_grpc.add_CertificateServiceServicer_to_server(CertificateService(), server)
'''
    # Enable reflection
    SERVICE_NAMES = (
        certificate_pb2.DESCRIPTOR.services_by_name['CertificateService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    listen_addr = "[::]:50055"
    server.add_insecure_port(listen_addr)
    logging.info("Starting gRPC server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()
'''
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())

