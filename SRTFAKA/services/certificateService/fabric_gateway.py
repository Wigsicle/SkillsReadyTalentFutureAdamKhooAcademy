import os
import hashlib
from hfc.fabric import Client as FabricClient

class FabricGateway:
    def __init__(self):
        """Initialize Hyperledger Fabric connection using fabric-sdk-py"""
        self.msp_id = "Org1MSP"
        self.channel_name = "mychannel"
        self.chaincode_name = "basic"
        self.peer_name = "peer0.org1.example.com"

        # Paths to crypto materials
        self.crypto_path = "../../test-network/organizations/peerOrganizations/org1.example.com"
        self.cert_path = os.path.join(self.crypto_path, "users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem")
        self.key_path = os.path.join(self.crypto_path, "users/User1@org1.example.com/msp/keystore")
        self.tls_cert_path = os.path.join(self.crypto_path, "peers/peer0.org1.example.com/tls/ca.crt")
        self.config_path = "../../test-network/connection-org1.yaml"

        # Initialize Fabric client
        self.client = FabricClient(net_profile=self.config_path)
        self.client.new_channel(self.channel_name)

        # Load user credentials
        self.user_name = "User1"
        self.client.get_user("org1.example.com", self.user_name)

    def create_certificate(self, certificate_id, course_id, owner):
        """
        Invoke chaincode to create a new certificate in Hyperledger Fabric.
        - certificate_id: Unique certificate identifier.
        - course_id: Course ID the certificate belongs to.
        - owner: User ID who receives the certificate.
        """
        try:
            response = self.client.chaincode_invoke(
                requestor=self.user_name,
                channel_name=self.channel_name,
                peers=[self.peer_name],
                fcn="CreateAsset",
                args=[certificate_id, course_id, owner],
                cc_name=self.chaincode_name,
                wait_for_event=True,
            )

            # Generate a unique hash of the certificate
            cert_hash = hashlib.sha256(certificate_id.encode()).hexdigest()

            print(f"✅ Certificate {certificate_id} successfully created on blockchain!")
            return certificate_id, cert_hash

        except Exception as e:
            print(f"❌ Blockchain error: {str(e)}")
            return None, None

    def close(self):
        """Close Fabric client connection"""
        print("🔒 Closing Fabric client connection")
