# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ydb.public.api.protos.draft import ydb_logstore_pb2 as ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2


class LogStoreServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateLogStore = channel.unary_unary(
                '/Ydb.LogStore.V1.LogStoreService/CreateLogStore',
                request_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogStoreRequest.SerializeToString,
                response_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogStoreResponse.FromString,
                )
        self.DescribeLogStore = channel.unary_unary(
                '/Ydb.LogStore.V1.LogStoreService/DescribeLogStore',
                request_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogStoreRequest.SerializeToString,
                response_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogStoreResponse.FromString,
                )
        self.DropLogStore = channel.unary_unary(
                '/Ydb.LogStore.V1.LogStoreService/DropLogStore',
                request_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogStoreRequest.SerializeToString,
                response_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogStoreResponse.FromString,
                )
        self.CreateLogTable = channel.unary_unary(
                '/Ydb.LogStore.V1.LogStoreService/CreateLogTable',
                request_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogTableRequest.SerializeToString,
                response_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogTableResponse.FromString,
                )
        self.DescribeLogTable = channel.unary_unary(
                '/Ydb.LogStore.V1.LogStoreService/DescribeLogTable',
                request_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogTableRequest.SerializeToString,
                response_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogTableResponse.FromString,
                )
        self.DropLogTable = channel.unary_unary(
                '/Ydb.LogStore.V1.LogStoreService/DropLogTable',
                request_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogTableRequest.SerializeToString,
                response_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogTableResponse.FromString,
                )
        self.AlterLogTable = channel.unary_unary(
                '/Ydb.LogStore.V1.LogStoreService/AlterLogTable',
                request_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.AlterLogTableRequest.SerializeToString,
                response_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.AlterLogTableResponse.FromString,
                )


class LogStoreServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateLogStore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DescribeLogStore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DropLogStore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateLogTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DescribeLogTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DropLogTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AlterLogTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogStoreServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateLogStore': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateLogStore,
                    request_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogStoreRequest.FromString,
                    response_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogStoreResponse.SerializeToString,
            ),
            'DescribeLogStore': grpc.unary_unary_rpc_method_handler(
                    servicer.DescribeLogStore,
                    request_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogStoreRequest.FromString,
                    response_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogStoreResponse.SerializeToString,
            ),
            'DropLogStore': grpc.unary_unary_rpc_method_handler(
                    servicer.DropLogStore,
                    request_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogStoreRequest.FromString,
                    response_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogStoreResponse.SerializeToString,
            ),
            'CreateLogTable': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateLogTable,
                    request_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogTableRequest.FromString,
                    response_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogTableResponse.SerializeToString,
            ),
            'DescribeLogTable': grpc.unary_unary_rpc_method_handler(
                    servicer.DescribeLogTable,
                    request_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogTableRequest.FromString,
                    response_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogTableResponse.SerializeToString,
            ),
            'DropLogTable': grpc.unary_unary_rpc_method_handler(
                    servicer.DropLogTable,
                    request_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogTableRequest.FromString,
                    response_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogTableResponse.SerializeToString,
            ),
            'AlterLogTable': grpc.unary_unary_rpc_method_handler(
                    servicer.AlterLogTable,
                    request_deserializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.AlterLogTableRequest.FromString,
                    response_serializer=ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.AlterLogTableResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Ydb.LogStore.V1.LogStoreService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LogStoreService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateLogStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.LogStore.V1.LogStoreService/CreateLogStore',
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogStoreRequest.SerializeToString,
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogStoreResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DescribeLogStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.LogStore.V1.LogStoreService/DescribeLogStore',
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogStoreRequest.SerializeToString,
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogStoreResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DropLogStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.LogStore.V1.LogStoreService/DropLogStore',
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogStoreRequest.SerializeToString,
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogStoreResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateLogTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.LogStore.V1.LogStoreService/CreateLogTable',
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogTableRequest.SerializeToString,
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.CreateLogTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DescribeLogTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.LogStore.V1.LogStoreService/DescribeLogTable',
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogTableRequest.SerializeToString,
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DescribeLogTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DropLogTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.LogStore.V1.LogStoreService/DropLogTable',
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogTableRequest.SerializeToString,
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.DropLogTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AlterLogTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.LogStore.V1.LogStoreService/AlterLogTable',
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.AlterLogTableRequest.SerializeToString,
            ydb_dot_public_dot_api_dot_protos_dot_draft_dot_ydb__logstore__pb2.AlterLogTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)