# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import freq_scrap_pb2 as freq__scrap__pb2


class FreqScrapStub(object):
    """Interface exported by the server.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFreq = channel.unary_unary(
                '/freqscrap.FreqScrap/GetFreq',
                request_serializer=freq__scrap__pb2.Request.SerializeToString,
                response_deserializer=freq__scrap__pb2.Response.FromString,
                )


class FreqScrapServicer(object):
    """Interface exported by the server.
    """

    def GetFreq(self, request, context):
        """A simple RPC.

        Obtains the feature at a given position.

        A feature with an empty name is returned if there's no feature at the given
        position.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FreqScrapServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFreq': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFreq,
                    request_deserializer=freq__scrap__pb2.Request.FromString,
                    response_serializer=freq__scrap__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'freqscrap.FreqScrap', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FreqScrap(object):
    """Interface exported by the server.
    """

    @staticmethod
    def GetFreq(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/freqscrap.FreqScrap/GetFreq',
            freq__scrap__pb2.Request.SerializeToString,
            freq__scrap__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
