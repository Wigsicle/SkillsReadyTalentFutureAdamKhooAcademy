from fastapi import APIRouter, Depends, HTTPException, Query
from ..gRPCHandler import getCertificate, createCertificate, updateCertificate, deleteCertificate
from google.protobuf.json_format import MessageToDict
from ..models import CertificateResponse, Certificate
from ..auth import getCurrentUser

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
    return {"message": "Certificate deleted successfully"}