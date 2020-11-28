#
# Dockerfile to use as a base for python
FROM python

RUN mkdir /app
WORKDIR /app
COPY driver.py driver.py
COPY grpc_stubs grpc_stubs
COPY grpc_stubs/freq_scrap_pb2_grpc.py freq_scrap_pb2_grpc.py
COPY grpc_stubs/freq_scrap_pb2.py freq_scrap_pb2.py
COPY grpc_server.py grpc_server.py
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD python grpc_server.py
EXPOSE 50051