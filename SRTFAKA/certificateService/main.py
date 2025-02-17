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
from ..generated import certificate_pb2
from ..generated import certificate_pb2_grpc
from ..common.utils import generateRandomId
from .db import CertificateDB

certificateDB = CertificateDB()

class Certificate(certificate_pb2_grpc.CertificateServicer):
    async def GetAllCertificate(
        self,
        request: certificate_pb2.CertificateData,
        context: grpc.aio.ServicerContext,
    ) -> certificate_pb2.CertificateList:
        rows = certificateDB.getAllCertificate()
        if rows is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No certificates found.")
            return certificate_pb2.CertificateList()
        certificates = [certificate_pb2.CertificateData(certificateId=row["certificateId"], name=row["name"],
                                           courseId=row["courseId"]) for row in rows]
        return certificate_pb2.CertificateList(certificates=certificates)


    async def CreateCertificate(
                self,
                request: certificate_pb2.CertificateData,
                context: grpc.aio.ServicerContext,
            ) -> certificate_pb2.CertificateData:
                newCertificateId = generateRandomId()
                print(f"GRPC Server: {request}")
                certificate = certificateDB.createCertificate((newCertificateId, request.name, request.courseId))
                if certificate is None:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details("Certificate creation failed or error occured.")
                    return certificate_pb2.CertificateData()
                return certificate_pb2.CertificateData(certificateId=newCertificateId, name=request.name, courseId=request.courseId)

    async def UpdateCertificate(self, request: certificate_pb2.CertificateData, context: grpc.aio.ServicerContext) -> certificate_pb2.CertificateData:
        updated = certificateDB.updateCertificate(
            {"certificateId": request.certificateId, "name": request.name, "courseId": request.courseId}
        )
        if not updated:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Certificate update failed or error occured.")
            return certificate_pb2.CertificateData()
        return certificate_pb2.CertificateData(certificateId=request.certificateId)
    
    async def DeleteCertificate(self, request: certificate_pb2.CertificateId, context: grpc.aio.ServicerContext) -> certificate_pb2.CertificateId:
        deleted = certificateDB.deleteCertificate(request.certificateId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Certificate not found for deletion or error occured.")
        return certificate_pb2.CertificateId()


async def serve() -> None:
    server = grpc.aio.server()
    certificate_pb2_grpc.add_CertificateServicer_to_server(Certificate(), server)
    listen_addr = "[::]:50055"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
