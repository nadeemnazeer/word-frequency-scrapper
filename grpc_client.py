"""The Python implementation of the gRPC freq scrap client."""

from __future__ import print_function

import random
import logging

import grpc

import grpc_stubs.freq_scrap_pb2 as freq_scrap_pb2
import grpc_stubs.freq_scrap_pb2_grpc as freq_scrap_pb2_grpc
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool to scrap any website and fetch top ngrams with their frequency. e.g: python grpc_client.py --url="https://www.washingtonpost.com/" --scrap_domains="washingtonpost.com"  --ngram=1 --top=10 --max_level=4')

    parser.add_argument('--url',type=str, help='Base url to scrap.', required=True)
    parser.add_argument('--scrap_domains',type=str,help='Comma seperated list of domains to restrict scraping and cralwing to.', required=True)
    parser.add_argument('--ngrams',type=int, help='ngrams value', required=True)
    parser.add_argument('--top',type=int, help='Top limit', required=True)
    parser.add_argument('--max_level',type=int, help='Max level to cralw & scrap', required=True)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    arguments = parser.parse_args()
    url = arguments.url
    scrap_domains = arguments.scrap_domains
    ngrams = arguments.ngrams
    top = arguments.top
    max_level = arguments.max_level
    
    with grpc.insecure_channel('localhost:50051') as channel:
        url = url
        scrap_domains = scrap_domains
        ngrams =ngrams
        top = top
        max_level =max_level
       
        request = freq_scrap_pb2.Request(url=url,scrap_domains=scrap_domains,ngrams= ngrams,top=top,max_level=max_level  )
        stub = freq_scrap_pb2_grpc.FreqScrapStub(channel)

        response = stub.GetFreq(request)
        print(response)