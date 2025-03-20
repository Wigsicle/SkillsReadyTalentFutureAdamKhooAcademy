from fastapi import APIRouter, Depends, HTTPException, Query
from google.protobuf.json_format import MessageToDict
from ..models import CertificateResponse, Certificate, UserCertificate, UserCertificateResponse
from ..auth import getCurrentUser
import json
import datetime
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

from ..gRPCHandler import (
    createCertificate,
    issueCertificate,
    getUserCertificates,
    updateCertificate,
    updateUserCertificate,
    getAllCertificates
)

certificate = APIRouter()

@certificate.post("/certificate/create")
async def create_certificate_api(cert: Certificate, currentUser: CertificateResponse = Depends(getCurrentUser)):
    """
    Create a new generic certificate via the gRPC service.
    """
    # Use the dict provided by the Pydantic model (or empty dict if None)
    additional_dict = cert.additionalInfo if cert.additionalInfo is not None else {}
    
    response = await createCertificate(
        name=cert.name,
        course_id=cert.courseId,
        years_valid=cert.yearsValid,
        description=cert.description,
        additional_info=additional_dict
    )
    response_dict = MessageToDict(response)
    # Convert the gRPC field "id" to "certificateId" to match our Pydantic model.
    response_dict["certificateId"] = response_dict.pop("id")
    cert_response = CertificateResponse(**response_dict)
    return {"message": "Certificate created", "data": cert_response.dict()}

@certificate.post("/certificate/issue")
async def issue_certificate_api(user_cert: UserCertificate, currentUser: UserCertificateResponse = Depends(getCurrentUser)):
    """
    Issue a user certificate via the gRPC service.
    """
    # 1. Set issuedOn to now
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    issued_ts = Timestamp()
    issued_ts.FromDatetime(now_utc)

    # 2. Provide None for expiresOn so the server logic can compute it if needed
    expires_ts = None
    
    response = await issueCertificate(
        user_id=user_cert.userId,
        cert_id=user_cert.certId,
        issued_on=issued_ts,
        expires_on=expires_ts,
        additional_info=user_cert.additionalInfo if user_cert.additionalInfo is not None else {}
    )
    response_dict = MessageToDict(response)
    user_cert_response = UserCertificateResponse(**response_dict)
    return {"message": "User certificate issued", "data": user_cert_response.dict()}

# @certificate.get("/certificate/user")
# async def get_user_certificates_api(userId: str):
#     """
#     Retrieve all certificates for a given user.
#     """
#     response = await getUserCertificates(userId)
#     response_dict = MessageToDict(response)
#     # The response_dict should contain a key "userCertificates" which is a list.
#     user_cert_list = []
#     for cert_dict in response_dict.get("userCertificates", []):
#         user_cert_response = UserCertificateResponse(**cert_dict)
#         user_cert_list.append(user_cert_response.dict())
#     return {"message": "User certificates retrieved", "data": user_cert_list}

@certificate.get("/certificate/all")
async def get_all_certificates_api(userId: str, currentUser: CertificateResponse = Depends(getCurrentUser)):
    """
    Retrieve all certificates that the user has, including the certificate name
    and other details.
    """
    # First, get the list of user certificates associated with the user
    user_cert_response = await getUserCertificates(userId)
    user_cert_response_dict = MessageToDict(user_cert_response)
    
    # Extract the cert_ids from the user's certificates
    user_cert_ids = {cert['certId'] for cert in user_cert_response_dict.get("userCertificates", [])}
    
    # Now, retrieve all certificates in the system
    all_certificates_response = await getAllCertificates()  # Call the gRPC function to get all certificates
    all_certificates_response_dict = MessageToDict(all_certificates_response)
    
    # Filter out certificates that the user has (match certId)
    matching_certificates = [
        {
            "certificateId": cert["id"],
            "name": cert["name"],
            "courseId": cert.get("course_id"),
            "yearsValid": cert.get("yearsValid"),
            "description": cert.get("description"),
            "additionalInfo": cert.get("additionalInfo"),
        }
        for cert in all_certificates_response_dict.get("certificates", [])
        if cert["id"] in user_cert_ids
    ]
    
    return {"message": "Certificates matching user retrieved", "data": matching_certificates}

@certificate.put("/certificate/update")
async def update_certificate_api(cert: Certificate, certificateId: int, currentUser: CertificateResponse = Depends(getCurrentUser)):
    """
    Update an existing certificate record via gRPC.
    """
    additional_dict = cert.additionalInfo if cert.additionalInfo is not None else {}
    response = await updateCertificate(
        certificate_id=certificateId,
        name=cert.name if cert.name else None,
        course_id=cert.courseId,
        years_valid=cert.yearsValid,
        description=cert.description,
        additional_info=additional_dict
    )
    response_dict = MessageToDict(response)
    response_dict["certificateId"] = response_dict.pop("id")
    cert_response = CertificateResponse(**response_dict)
    return {"message": "Certificate updated", "data": cert_response.dict()}

@certificate.put("/certificate/user/update")
async def update_user_certificate_api(user_cert: UserCertificate, userCertId: int, currentUser: UserCertificateResponse = Depends(getCurrentUser)):
    """
    Update an existing user-issued certificate via gRPC.
    """
    issued_ts = None
    if user_cert.issuedOn:
        issued_ts = Timestamp()
        issued_ts.FromDatetime(user_cert.issuedOn)
    
    expires_ts = None
    if user_cert.expiresOn:
        expires_ts = Timestamp()
        expires_ts.FromDatetime(user_cert.expiresOn)
    
    response = await updateUserCertificate(
        user_cert_id=userCertId,
        user_id=user_cert.userId,
        cert_id=user_cert.certId,
        issued_on=issued_ts,
        expires_on=expires_ts,
        additional_info=user_cert.additionalInfo if user_cert.additionalInfo is not None else {}
    )
    response_dict = MessageToDict(response)
    user_cert_response = UserCertificateResponse(**response_dict)
    return {"message": "User certificate updated", "data": user_cert_response.dict()}

'''
certificate = APIRouter()

@certificate.get("/certificate")
async def get_certificate():
    certificates = MessageToDict(await getCertificate())
    return {"message": "Certificates retrieved", "data": certificates}
    
@certificate.post("/certificate/create") 
async def create_certificate(certificate: Certificate): 
    newCertificate = await createCertificate(certificate) 
    if newCertificate is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Certificate created", "data": MessageToDict(newCertificate)}

@certificate.put("/certificate/update")
async def update_certificate(certificateId: str, certificate: Certificate, currentUser: CertificateResponse = Depends(getCurrentUser)):
    response = await updateCertificate(certificateId, certificate)
    if response is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Certificate updated", "data": MessageToDict(response)}

@certificate.delete("/certificate")
async def delete_certificate(certificateId: str, currentUser: CertificateResponse = Depends(getCurrentUser)):
    deletedCertificate = await deleteCertificate(certificateId)
    if deletedCertificate is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Certificate deleted successfully"}'
'''