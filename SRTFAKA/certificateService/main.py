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

from ..generated import certificate_pb2
from ..generated import certificate_pb2_grpc
from ..common.utils import generateRandomId
#from .db import CertificateDB
from .db import get_db, Certificate, UserCertificate
from .fabric_gateway import FabricClient

fabric_client = FabricClient()  # Blockchain client instance

class CertificateService(certificate_pb2_grpc.CertificateServicer):
    
    async def GetAllCertificate(self, request, context):
        """Fetches all certificates from the centralized database."""
        try:
            with next(get_db()) as db:
                certificates = db.query(Certificate).all()
                if not certificates:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("No certificates found.")
                    return certificate_pb2.CertificateList()
                
                return certificate_pb2.CertificateList(
                    certificates=[
                        certificate_pb2.CertificateData(
                            certificateId=str(cert.id),
                            name=cert.name,
                            courseId=str(cert.course_id),
                            blockchainTxId=cert.blockchain_tx_id or "",
                            certificateHash=cert.certificate_hash or "",
                        )
                        for cert in certificates
                    ]
                )
        except Exception as e:
            logging.error(f"Error in GetAllCertificate: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error.")
            return certificate_pb2.CertificateList()

    async def CreateCertificate(self, request, context):
        """Issues a certificate, stores it in the database, and submits to the blockchain."""
        new_certificate_id = generateRandomId()

        try:
            # Call Blockchain to issue certificate
            tx_id, cert_hash = fabric_client.create_certificate(new_certificate_id, request.name, request.courseId)

            if not tx_id:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Blockchain transaction failed.")
                return certificate_pb2.CertificateData()

            # Store certificate in DB
            with next(get_db()) as db:
                new_cert = Certificate(
                    id=new_certificate_id,
                    name=request.name,
                    course_id=int(request.courseId),
                    blockchain_tx_id=tx_id,
                    certificate_hash=cert_hash
                )
                db.add(new_cert)
                db.commit()
                db.refresh(new_cert)

                return certificate_pb2.CertificateData(
                    certificateId=str(new_cert.id),
                    name=new_cert.name,
                    courseId=str(new_cert.course_id),
                    blockchainTxId=tx_id,
                    certificateHash=cert_hash
                )

        except Exception as e:
            logging.error(f"Error in CreateCertificate: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to create certificate.")
            return certificate_pb2.CertificateData()

    async def GetUserCertificates(self, request, context):
        """Fetches all certificates owned by a user from the centralized database."""
        try:
            with next(get_db()) as db:
                user_certificates = (
                    db.query(UserCertificate)
                    .filter(UserCertificate.user_id == request.user_id)
                    .all()
                )

                if not user_certificates:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("No certificates found for user.")
                    return certificate_pb2.CertificateList()

                return certificate_pb2.CertificateList(
                    certificates=[
                        certificate_pb2.CertificateData(
                            certificateId=str(cert.cert_id),
                            name=cert.cert_info.name,
                            courseId=str(cert.cert_info.course_id),
                            blockchainTxId=cert.blockchain_tx_id or "",
                            certificateHash=cert.certificate_hash or "",
                        )
                        for cert in user_certificates
                    ]
                )
        except Exception as e:
            logging.error(f"Error in GetUserCertificates: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error.")
            return certificate_pb2.CertificateList()

    async def GetCertificateDetails(self, request, context):
        """Fetches details of a specific certificate from the centralized database."""
        try:
            with next(get_db()) as db:
                certificate = db.query(Certificate).filter(Certificate.id == request.certificateId).first()
                if not certificate:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Certificate not found.")
                    return certificate_pb2.CertificateData()

                return certificate_pb2.CertificateData(
                    certificateId=str(certificate.id),
                    name=certificate.name,
                    courseId=str(certificate.course_id),
                    blockchainTxId=certificate.blockchain_tx_id or "",
                    certificateHash=certificate.certificate_hash or "",
                )
        except Exception as e:
            logging.error(f"Error in GetCertificateDetails: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error.")
            return certificate_pb2.CertificateData()


async def serve():
    """Starts the gRPC server."""
    server = grpc.aio.server()
    certificate_pb2_grpc.add_CertificateServicer_to_server(CertificateService(), server)
    listen_addr = "[::]:50055"
    server.add_insecure_port(listen_addr)
    logging.info("Starting gRPC server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())

