clean:
    rm -f *.pyc
    rm -f *_pb2.py
    rm -f *_pb2_grpc.py

stubs:
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. estoque.proto
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pedidos.proto

run_serv_estoque:
    python3 service_estoque.py $(arg1)

run_cli_estoque:
    python3 client_estoque.py $(arg1)

run_serv_pedidos:
    python3 service_pedidos.py $(arg1) $(arg2)

run_cli_pedidos:
    python3 client_pedidos.py $(arg1) $(arg2)
