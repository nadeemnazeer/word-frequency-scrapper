"""The Python implementation of the gRPC freq scrapper server."""

from concurrent import futures
import time
import math
import logging

import grpc

from grpc_stubs.freq_scrap_pb2 import Response, Result
from grpc_stubs.freq_scrap_pb2_grpc  import FreqScrapServicer, add_FreqScrapServicer_to_server
from core import FreqScrapper


class FreqScrapServicer(FreqScrapServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        pass

    def GetFreq(self, request, context):
        print(request)
        url = request.url
        scrap_domains = request.scrap_domains.split(",")
        ngrams= request.ngrams
        top = request.top
        max_level = request.max_level
        fs = FreqScrapper(url,scrap_domains)
        fw = fs.get_freq_words(ngrams,top,max_level) 
        results = []
        for t in fw:
            results.append(Result(word=" ".join(t[0]), freq=t[1]))

        response = Response()
        response.results.extend(results)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_FreqScrapServicer_to_server(
        FreqScrapServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()