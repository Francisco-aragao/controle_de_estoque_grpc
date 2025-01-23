import grpc
import sys
from concurrent import futures  # usado pra abrir multilpas instancias do servidor
import threading

import estoque_pb2, estoque_pb2_grpc  # importa modulos gerados no stub


class Produto:
    """
    Classe pra gerenciar os produtos que são adicionados
    """

    def __init__(self, id, descricao, quantidade):
        self.id = id
        self.descricao = descricao
        self.quantidade = quantidade


class EstoqueService(estoque_pb2_grpc.EstoqueServiceServicer):
    """
    Classe que lida com as operações do servidor de estoque
    """

    def __init__(self, stop_event):
        self.produtos = []
        self._stop_event = stop_event

    def AdicionaProduto(self, request, context):

        # adicionando produto que já existe (verifico pela descrição)
        for produto in self.produtos:
            if produto.descricao == request.descricao:
                produto.quantidade += request.quantidade
                return estoque_pb2.ProdutoId(id=produto.id)

        id = 0
        if len(self.produtos) == 0:
            id = 1
        else:
            id = self.produtos[-1].id + 1

        produto = Produto(id, request.descricao, request.quantidade)
        self.produtos.append(produto)
        return estoque_pb2.ProdutoId(id=id)

    def AlteraQuantidadeDeProduto(self, request, context):

        # checo se o produto existe
        if len(self.produtos) < request.prod_id:
            return estoque_pb2.StatusEstoque(status=-2)

        # checo se a quantidade do produto é suficiente
        if (self.produtos[request.prod_id - 1].quantidade + request.valor) < 0:
            return estoque_pb2.StatusEstoque(status=-1)

        self.produtos[request.prod_id - 1].quantidade += request.valor

        return estoque_pb2.StatusEstoque(
            status=self.produtos[request.prod_id - 1].quantidade
        )

    def ListaProdutos(self, request, context):
        lista = (
            estoque_pb2.ListaDeProdutos()
        )  # crio lista conforme definido no arquivo .proto

        for produto in self.produtos:
            p = lista.produtos.add()
            p.id = produto.id
            p.descricao = produto.descricao
            p.quantidade = produto.quantidade

        return lista

    def FimDaExecucao(self, request, context):
        self._stop_event.set()
        return estoque_pb2.StatusEstoque(status=len(self.produtos))


def main(port):

    stop_event = threading.Event()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    estoque_pb2_grpc.add_EstoqueServiceServicer_to_server(
        EstoqueService(stop_event), server
    )

    server.add_insecure_port(f"0.0.0.0:{port}")

    server.start()
    stop_event.wait()
    server.stop(grace=None)


if __name__ == "__main__":
    port = sys.argv[1]
    main(port)
