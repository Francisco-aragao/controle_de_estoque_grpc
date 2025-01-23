import grpc
import sys
from concurrent import futures  # usado pra abrir multilpas instancias do servidor
import threading

import pedidos_pb2, pedidos_pb2_grpc, estoque_pb2, estoque_pb2_grpc  # importa modulos gerados no stub junto com modulos do estoque


class Produto:
    """
    Classe que representa um produto (semelhante ao que está em Estoque). Essa classe é útil para organizar as informações dos produtos que estão em um pedido.
    """

    def __init__(self, produto_id, status, quantidade):
        self.produto_id = produto_id
        self.status = status
        self.quantidade = quantidade


class Pedido:
    """
    Classe que representa um pedido, possui método AddProduto pra adicionar os produtos que estão em um pedido.
    """

    def __init__(self, id):
        self.id = id
        self.produtos = []

    def AddProduto(self, produto):
        self.produtos.append(produto)


class PedidosService(pedidos_pb2_grpc.PedidosServiceServicer):
    """
    Classe que lida com todas as operações do servidor de pedidos
    """

    def __init__(self, stop_event, server_rpc_estoque):
        self._stop_event = stop_event
        self.pedidos = []
        self.rpc_estoque = server_rpc_estoque

    def CriaPedido(self, request, context):
        """
        Cria um pedido, adicionando os produtos ao pedido e retirando do estoque.
        """

        lista = pedidos_pb2.ListaIdStatus()

        id = len(self.pedidos) + 1

        novo_pedido: Pedido = Pedido(id)

        for item in request.itens:

            prod_id = item.prod_id

            # valor negativo pois estou retirando do estoque
            response = self.rpc_estoque.AlteraQuantidadeDeProduto(
                estoque_pb2.AlteraQuantidadeRequest(
                    prod_id=prod_id, valor=-item.quantidade
                )
            )

            # só adiciono o pedido na minha lista de pedidos se a operação no estoque foi bem sucedida
            # >= 0 pois se estoque retornar um número negativo, significa que a operação não foi bem sucedida
            status = response.status
            produto = Produto(prod_id, status, item.quantidade)

            if status >= 0:
                status = 0  # operação bem sucedida
                novo_pedido.AddProduto(produto)

            p = lista.par.add()
            p.pedido_id = id
            p.status = status

        if novo_pedido.produtos:
            self.pedidos.append(novo_pedido)

        return lista

    def CancelaPedido(self, request, context):
        """
        Cancela um pedido, retornando os produtos que foram reservados anteriormente ao estoque.
        """

        if len(self.pedidos) < request.id:
            return pedidos_pb2.StatusPedidos(status=-1)

        pedido_removido = self.pedidos.pop(request.id - 1)

        for produto in pedido_removido.produtos:

            # ignoro produtos que não foram bem sucessidos (teoricamente não deveria acontecer esse caso pois já verifco em CriaPedido, mas deixei por garantia)
            if produto.status != 0:
                continue

            self.rpc_estoque.AlteraQuantidadeDeProduto(
                estoque_pb2.AlteraQuantidadeRequest(
                    prod_id=produto.produto_id, valor=produto.quantidade
                )
            )

        return pedidos_pb2.StatusPedidos(status=0)

    def FimDaExecucao(self, request, context):
        """
        Finalizo servidor de pedidos. Antes de matar o servidor, preciso finalizar o servidor de estoque.
        """
        response = self.rpc_estoque.FimDaExecucao(estoque_pb2.EmptyRequest())
        self._stop_event.set()

        return pedidos_pb2.FimExecucaoStatus(
            estoque_status=response.status, pedidos_ativos=len(self.pedidos)
        )


def main(port, identificador_rpc_server_estoque):

    # evento para finalizar o servidor
    stop_event = threading.Event()

    # agora Pedidos é cliente de Estoque
    channel_estoque = grpc.insecure_channel(identificador_rpc_server_estoque)
    stub_estoque = estoque_pb2_grpc.EstoqueServiceStub(channel_estoque)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pedidos_pb2_grpc.add_PedidosServiceServicer_to_server(
        PedidosService(stop_event, stub_estoque), server
    )

    server.add_insecure_port(f"0.0.0.0:{port}")

    server.start()
    stop_event.wait()

    channel_estoque.close()  # finalizo estoque também ao sair
    server.stop(grace=None)


if __name__ == "__main__":
    port = sys.argv[1]
    identificador_rpc_server_estoque = sys.argv[2]

    main(port, identificador_rpc_server_estoque)
