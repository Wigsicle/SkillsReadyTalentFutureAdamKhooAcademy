# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import courseProgress_pb2 as courseProgress__pb2

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
        + f' but the generated code in courseProgress_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class CourseProgressStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.JoinCourse = channel.unary_unary(
                '/CourseProgress.CourseProgress/JoinCourse',
                request_serializer=courseProgress__pb2.CourseProgressData.SerializeToString,
                response_deserializer=courseProgress__pb2.CourseProgressData.FromString,
                _registered_method=True)
        self.UpdateCourseProgress = channel.unary_unary(
                '/CourseProgress.CourseProgress/UpdateCourseProgress',
                request_serializer=courseProgress__pb2.CourseProgressId.SerializeToString,
                response_deserializer=courseProgress__pb2.CourseProgressId.FromString,
                _registered_method=True)


class CourseProgressServicer(object):
    """Missing associated documentation comment in .proto file."""

    def JoinCourse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateCourseProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CourseProgressServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'JoinCourse': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinCourse,
                    request_deserializer=courseProgress__pb2.CourseProgressData.FromString,
                    response_serializer=courseProgress__pb2.CourseProgressData.SerializeToString,
            ),
            'UpdateCourseProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateCourseProgress,
                    request_deserializer=courseProgress__pb2.CourseProgressId.FromString,
                    response_serializer=courseProgress__pb2.CourseProgressId.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CourseProgress.CourseProgress', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('CourseProgress.CourseProgress', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CourseProgress(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def JoinCourse(request,
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
            '/CourseProgress.CourseProgress/JoinCourse',
            courseProgress__pb2.CourseProgressData.SerializeToString,
            courseProgress__pb2.CourseProgressData.FromString,
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
    def UpdateCourseProgress(request,
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
            '/CourseProgress.CourseProgress/UpdateCourseProgress',
            courseProgress__pb2.CourseProgressId.SerializeToString,
            courseProgress__pb2.CourseProgressId.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
