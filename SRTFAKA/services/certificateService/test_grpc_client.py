import grpc
import json
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from SRTFAKA.generated import certificate_pb2
from SRTFAKA.generated import certificate_pb2_grpc

# Define the server address and port (must match your server's settings)
SERVER_ADDRESS = "localhost:50055"

def test_create_certificate():
    """Test the CreateCertificate gRPC method"""

    # Establish a gRPC channel
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = certificate_pb2_grpc.CertificateServiceStub(channel)

    # Create a request object (aligned with `db.py`)
    request = certificate_pb2.CertificateData(
        name="Test Certificate",
        courseId=3,  # Optional: 
        yearsValid=25,  # Now an integer, previously was `validityPeriod`
        description="A test certificate for alignment",
        additionalInfo=json.dumps({"issuer": "Admin", "issued_to": "Student123"})  # Ensure JSON format
    )

    # Call the gRPC service
    try:
        response = stub.CreateCertificate(request)
        
        print("\n✅ Certificate Created Successfully!\n")
        print(f"📜 Certificate ID: {response.id}")
        print(f"📌 Name: {response.name}")
        print(f"📚 Course ID: {response.courseId if response.courseId else 'N/A'}")  # Handle optional
        print(f"⏳ Years Valid: {response.yearsValid if response.yearsValid else 'N/A'}")  # Handle optional
        print(f"📝 Description: {response.description if response.description else 'N/A'}")  # Handle optional
        print(f"🔗 Additional Info: {response.additionalInfo if response.additionalInfo else '{}'}")  # Handle optional

    except grpc.RpcError as e:
        print(f"❌ gRPC Error: {e.details()}")
        print(f"📌 Status Code: {e.code()}")

def test_issue_certificate():
    """Test the IssueCertificate gRPC method"""

    # Establish a gRPC channel
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = certificate_pb2_grpc.CertificateServiceStub(channel)

    """
    # Prepare issuedOn and expiresOn timestamps
    issued_dt = datetime.datetime.now()
    expires_dt = issued_dt + datetime.timedelta(days=365)  # Example: certificate expires in 1 year

    issued_on = Timestamp()
    issued_on.FromDatetime(issued_dt)
    expires_on = Timestamp()
    expires_on.FromDatetime(expires_dt)
    """
    # Prepare an issuedOn timestamp
    issued_dt = datetime.datetime.now()
    issued_on = Timestamp()
    issued_on.FromDatetime(issued_dt) 

    # Create a request object.
    # Use test values for userId and certId. Adjust these values to match records in your database.
    request = certificate_pb2.UserCertificateData(
        userId=6,
        certId=17,
        issuedOn=issued_on,
        additionalInfo=json.dumps({"chain": "BlockchainTest", "issued_by": "Admin"})
    )

    # Call the gRPC service
    try:
        response = stub.IssueCertificate(request)
        print("\n✅ Certificate Issued Successfully!\n")
        print(f"📜 User Certificate ID: {response.id}")
        print(f"👤 User ID: {response.userId}")
        print(f"🛡 Certificate ID: {response.certId}")
        # Convert protobuf timestamps to Python datetime objects for display
        print(f"⏰ Issued On: {response.issuedOn.ToDatetime()}")
        if response.HasField("expiresOn"):
            print(f"⏳ Expires On: {response.expiresOn.ToDatetime()}")
        else:
            print("⏳ Expires On: N/A")
        print(f"🔗 Additional Info: {response.additionalInfo}")
    except grpc.RpcError as e:
        print(f"❌ gRPC Error: {e.details()}")
        print(f"📌 Status Code: {e.code()}")

def test_get_user_certificates():
    """Test the GetUserCertificates gRPC method."""
    
    # Establish a gRPC channel
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = certificate_pb2_grpc.CertificateServiceStub(channel)
    
    # Create a request for user ID "1" (as defined in your proto, userId is a string)
    request = certificate_pb2.UserId(userId="6")
    
    try:
        # Call the GetUserCertificates method
        response = stub.GetUserCertificates(request)
        
        print("\n✅ User Certificates Retrieved Successfully!\n")
        
        # Check if any certificates were returned
        if not response.userCertificates:
            print("No certificates found for the user.")
        else:
            # Loop through and print details of each certificate
            for cert in response.userCertificates:
                print("------------------------------")
                print(f"User Certificate ID: {cert.id}")
                print(f"User ID: {cert.userId}")
                print(f"Certificate ID: {cert.certId}")
                
                # Convert issuedOn and expiresOn timestamps to human-readable format.
                # These are protobuf Timestamp objects and support the ToDatetime() method.
                try:
                    issued_on = cert.issuedOn.ToDatetime()
                except Exception as e:
                    issued_on = "Conversion error"
                
                try:
                    # Check if expiresOn is set
                    if cert.HasField("expiresOn"):
                        expires_on = cert.expiresOn.ToDatetime()
                    else:
                        expires_on = "N/A"
                except Exception as e:
                    expires_on = "Conversion error"
                
                print(f"Issued On: {issued_on}")
                print(f"Expires On: {expires_on}")
                print(f"Additional Info: {cert.additionalInfo}")
                
    except grpc.RpcError as e:
        print(f"❌ gRPC Error: {e.details()}")
        print(f"📌 Status Code: {e.code()}")


def test_update_certificate():
    """
    Tests the UpdateCertificate gRPC method.
    This assumes that a certificate with the specified ID already exists.
    """
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = certificate_pb2_grpc.CertificateServiceStub(channel)
    
    # Prepare an update request.
    # For example, assume certificate with id=1 exists.
    # For optional int fields, use 0 if you don't want to update (they'll be treated as None).
    update_request = certificate_pb2.CertificateData(
        id=6,  # Certificate ID to update
        name="UPDATE UPDATE",
        courseId=8,  # New course ID (if applicable, or 0 for None)
        yearsValid=69,
        description="UPDATE UPDATE",
        additionalInfo=json.dumps({"UPDATE": True})
    )
    
    try:
        response = stub.UpdateCertificate(update_request)
        print("\n✅ UpdateCertificate response:")
        print(f"ID: {response.id}")
        print(f"Name: {response.name}")
        print(f"Course ID: {response.courseId}")
        print(f"Years Valid: {response.yearsValid}")
        print(f"Description: {response.description}")
        print(f"Additional Info: {response.additionalInfo}")
    except grpc.RpcError as e:
        print("❌ UpdateCertificate gRPC Error:")
        print(f"Details: {e.details()}")
        print(f"Status Code: {e.code()}")

def test_update_user_certificate():
    """
    Tests the UpdateUserCertificate gRPC method.
    This assumes that a user certificate record with the specified ID already exists.
    """
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = certificate_pb2_grpc.CertificateServiceStub(channel)
    
    # Prepare protobuf Timestamp objects for issuedOn and expiresOn.
    issued_on_ts = Timestamp()
    issued_dt = datetime.datetime.now()
    issued_on_ts.FromDatetime(issued_dt)
    
    expires_on_ts = Timestamp()
    expires_dt = issued_dt + datetime.timedelta(days=365)
    expires_on_ts.FromDatetime(expires_dt)
    
    # Prepare the update request.
    # For example, assume the user certificate with id=1 exists.
    update_request = certificate_pb2.UserCertificateData(
        id=12,       # The user certificate record to update.
        userId=2,   # New user id (or the same if you don't want to change)
        certId=6,   # New certificate id (or the same if you don't want to change)
        issuedOn=issued_on_ts,
        expiresOn=expires_on_ts,
        additionalInfo=json.dumps({"UPDATEDEDED": True})
    )
    
    try:
        response = stub.UpdateUserCertificate(update_request)
        print("\n✅ UpdateUserCertificate response:")
        print(f"ID: {response.id}")
        print(f"User ID: {response.userId}")
        print(f"Certificate ID: {response.certId}")
        # Convert proto timestamps back to datetime for display.
        try:
            issued_on = response.issuedOn.ToDatetime()
        except Exception:
            issued_on = "Conversion error"
        try:
            if response.HasField("expiresOn"):
                expires_on = response.expiresOn.ToDatetime()
            else:
                expires_on = "N/A"
        except Exception:
            expires_on = "Conversion error"
        print(f"Issued On: {issued_on}")
        print(f"Expires On: {expires_on}")
        print(f"Additional Info: {response.additionalInfo}")
    except grpc.RpcError as e:
        print("❌ UpdateUserCertificate gRPC Error:")
        print(f"Details: {e.details()}")
        print(f"Status Code: {e.code()}")

if __name__ == "__main__":
    #test_create_certificate()
    test_issue_certificate()
    #test_get_user_certificates()
    #test_update_certificate()
    #test_update_user_certificate()

