clean:
	rm -f pedidos_pb2.py
	rm -f pedidos_pb2_grpc.py
	rm -f estoque_pb2.py
	rm -f estoque_pb2_grpc.py

# usando @ so pra não exibir o comando na tela

stub_estoque:
	@if [ ! -f "estoque_pb2.py" ] || [ ! -f "estoque_pb2_grpc.py" ]; then \
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. estoque.proto; \
	fi

# Definindo a regra para gerar os stubs de pedidos
stub_pedidos:
	@if [ ! -f "pedidos_pb2.py" ] || [ ! -f "pedidos_pb2_grpc.py" ]; then \
        python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pedidos.proto; \
	fi

# Regras para gerar todos os stubs
stubs: stub_estoque stub_pedidos

run_serv_estoque: stubs
	@python3 service_estoque.py $(arg1)

run_cli_estoque: stubs
	@python3 client_estoque.py $(arg1)

run_serv_pedidos: stubs
	@python3 service_pedidos.py $(arg1) $(arg2)

run_cli_pedidos: stubs
	@python3 client_pedidos.py $(arg1) $(arg2)
