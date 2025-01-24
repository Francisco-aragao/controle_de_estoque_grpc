# controle_de_estoque_grpc

Implementação de um sistema de controle de estoque utilizando gRPC.

- estoque.proto: arquivo de definição do serviço gRPC de estoque.
- estoque_server.py: implementação do servidor gRPC de estoque.
- estoque_client.py: implementação do cliente gRPC de estoque.

- pedidos.proto: arquivo de definição do serviço gRPC de pedidos.
- pedidos_server.py: implementação do servidor gRPC de pedidos.
- pedidos_client.py: implementação do cliente gRPC de pedidos.

- Instalar dependências
(pensando nas máquinas do laboratório do DCC -> problemas com o setuptools que está presente no requirements.txt. Basta instalar apenas os dois pacotes abaixo do grpc)
pip install grpcio
pip install grpcio-tools

ou

pip install -r requirements.txt

- Execução estoque:
make run_serv_estoque arg1=porta
make run_cli_estoque arg1=servidorEstoque:porta
(digita comandos para o estoque)

- Execução pedidos:
make run_serv_estoque arg1=porta
make run_cli_estoque arg1=servidorEstoque:porta
(digita comandos para o estoque - para fazer pedidos, é necessário ter produtos no estoque)
make run_serv_pedidos arg1=porta arg2=servidorEstoque:porta
make run_cli_pedidos arg1=servidorEstoque:porta arg2=servidorPedidos:porta
(digita comandos para os pedidos)