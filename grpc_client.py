"""The Python implementation of the gRPC freq scrap client."""

from __future__ import print_function

import random
import logging

import grpc

import grpc_stubs.freq_scrap_pb2 as freq_scrap_pb2
import grpc_stubs.freq_scrap_pb2_grpc as freq_scrap_pb2_grpc



def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        url = 'https://www.washingtonpost.com/'
        scrap_domains = ','.join(["washingtonpost.com"])
        ngrams = 2
        top = 10
        max_level = 1
       
        request = freq_scrap_pb2.Request(url=url,scrap_domains=scrap_domains,ngrams= ngrams,top=top,max_level=max_level  )
        stub = freq_scrap_pb2_grpc.FreqScrapStub(channel)

        response = stub.GetFreq(request)
        print(response)



if __name__ == '__main__':
    logging.basicConfig()
    run()