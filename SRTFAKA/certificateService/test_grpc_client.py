import grpc
import json
from datetime import datetime
from generated import certificate_pb2
from generated import certificate_pb2_grpc

# Define the server address and port (must match your server's settings)
SERVER_ADDRESS = "localhost:50055"

def test_create_certificate():
    """Test the CreateCertificate gRPC method"""

    # Establish a gRPC channel
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = certificate_pb2_grpc.CertificateServiceStub(channel)

    # Create a request object
    request = certificate_pb2.CertificateData(
        name="Test Certificate",
        courseId="",
        validityPeriod="12:00:00",  # Format must match the server's expected format
        description="A test certificate",
        additionalInfo=json.dumps({"issuer": "Admin", "issued_to": "Student123"})
    )

    # Call the gRPC service
    try:
        response = stub.CreateCertificate(request)
        print("\n✅ Certificate Created Successfully!\n")
        print(f"📜 Certificate ID: {response.id}")
        print(f"📌 Name: {response.name}")
        print(f"📚 Course ID: {response.courseId}")
        print(f"⏳ Validity Period: {response.validityPeriod}")
        print(f"📝 Description: {response.description}")
        print(f"🔗 Additional Info: {response.additionalInfo}")

    except grpc.RpcError as e:
        print(f"❌ gRPC Error: {e.details()}")

if __name__ == "__main__":
    test_create_certificate()
