# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import certificate_pb2 as certificate__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in certificate_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class CertificateServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateCertificate = channel.unary_unary(
                '/Certificate.CertificateService/CreateCertificate',
                request_serializer=certificate__pb2.CertificateData.SerializeToString,
                response_deserializer=certificate__pb2.CertificateData.FromString,
                _registered_method=True)
        self.IssueCertificate = channel.unary_unary(
                '/Certificate.CertificateService/IssueCertificate',
                request_serializer=certificate__pb2.UserCertificateData.SerializeToString,
                response_deserializer=certificate__pb2.UserCertificateData.FromString,
                _registered_method=True)
        self.GetUserCertificates = channel.unary_unary(
                '/Certificate.CertificateService/GetUserCertificates',
                request_serializer=certificate__pb2.UserId.SerializeToString,
                response_deserializer=certificate__pb2.UserCertificateList.FromString,
                _registered_method=True)
        self.GetAllCertificates = channel.unary_unary(
                '/Certificate.CertificateService/GetAllCertificates',
                request_serializer=certificate__pb2.Empty.SerializeToString,
                response_deserializer=certificate__pb2.CertificateList.FromString,
                _registered_method=True)
        self.UpdateCertificate = channel.unary_unary(
                '/Certificate.CertificateService/UpdateCertificate',
                request_serializer=certificate__pb2.CertificateData.SerializeToString,
                response_deserializer=certificate__pb2.CertificateData.FromString,
                _registered_method=True)
        self.UpdateUserCertificate = channel.unary_unary(
                '/Certificate.CertificateService/UpdateUserCertificate',
                request_serializer=certificate__pb2.UserCertificateData.SerializeToString,
                response_deserializer=certificate__pb2.UserCertificateData.FromString,
                _registered_method=True)


class CertificateServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateCertificate(self, request, context):
        """Creates a new generic certificate in the database
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IssueCertificate(self, request, context):
        """Issues a certificate to a user & adds it to the blockchain
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserCertificates(self, request, context):
        """Retrieves all certificates owned by a specific user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllCertificates(self, request, context):
        """Retrieves all certificates in the database
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateCertificate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateUserCertificate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CertificateServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateCertificate': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCertificate,
                    request_deserializer=certificate__pb2.CertificateData.FromString,
                    response_serializer=certificate__pb2.CertificateData.SerializeToString,
            ),
            'IssueCertificate': grpc.unary_unary_rpc_method_handler(
                    servicer.IssueCertificate,
                    request_deserializer=certificate__pb2.UserCertificateData.FromString,
                    response_serializer=certificate__pb2.UserCertificateData.SerializeToString,
            ),
            'GetUserCertificates': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserCertificates,
                    request_deserializer=certificate__pb2.UserId.FromString,
                    response_serializer=certificate__pb2.UserCertificateList.SerializeToString,
            ),
            'GetAllCertificates': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllCertificates,
                    request_deserializer=certificate__pb2.Empty.FromString,
                    response_serializer=certificate__pb2.CertificateList.SerializeToString,
            ),
            'UpdateCertificate': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateCertificate,
                    request_deserializer=certificate__pb2.CertificateData.FromString,
                    response_serializer=certificate__pb2.CertificateData.SerializeToString,
            ),
            'UpdateUserCertificate': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateUserCertificate,
                    request_deserializer=certificate__pb2.UserCertificateData.FromString,
                    response_serializer=certificate__pb2.UserCertificateData.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Certificate.CertificateService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Certificate.CertificateService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CertificateService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateCertificate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Certificate.CertificateService/CreateCertificate',
            certificate__pb2.CertificateData.SerializeToString,
            certificate__pb2.CertificateData.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def IssueCertificate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Certificate.CertificateService/IssueCertificate',
            certificate__pb2.UserCertificateData.SerializeToString,
            certificate__pb2.UserCertificateData.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetUserCertificates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Certificate.CertificateService/GetUserCertificates',
            certificate__pb2.UserId.SerializeToString,
            certificate__pb2.UserCertificateList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllCertificates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Certificate.CertificateService/GetAllCertificates',
            certificate__pb2.Empty.SerializeToString,
            certificate__pb2.CertificateList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateCertificate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Certificate.CertificateService/UpdateCertificate',
            certificate__pb2.CertificateData.SerializeToString,
            certificate__pb2.CertificateData.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateUserCertificate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Certificate.CertificateService/UpdateUserCertificate',
            certificate__pb2.UserCertificateData.SerializeToString,
            certificate__pb2.UserCertificateData.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
