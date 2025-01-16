import grpc
import sys
from concurrent import futures # usado na definição do pool de threads
import threading

import estoque_pb2, estoque_pb2_grpc # importa modulos gerados no stub


class Produto:
    def __init__(self, id, descricao, quantidade):
        self.id = id
        self.descricao = descricao
        self.quantidade = quantidade

    def __str__(self):
        return f'{self.id} - {self.descricao} - {self.quantidade}'

class EstoqueService(estoque_pb2_grpc.EstoqueServiceServicer):
    def __init__(self, stop_event):
        self.produtos = []
        self._stop_event = stop_event
       
    def AdicionaProduto(self, request, context):


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

        print("aqui2")
        
        if len(self.produtos) < request.prod_id:
            return estoque_pb2.Status(status=-2)
        
        print(self.produtos[request.prod_id - 1].quantidade)
        print(request.valor)

        print("oi")

        if (self.produtos[request.prod_id - 1].quantidade + request.valor ) < 0:
            return estoque_pb2.Status(status=-1)
        
        self.produtos[request.prod_id - 1].quantidade += request.valor

        return estoque_pb2.Status(status=self.produtos[request.prod_id - 1].quantidade)

    def ListaProdutos(self, request, context):
        lista = estoque_pb2.ListaDeProdutos()

        for produto in self.produtos:
            p = lista.produtos.add()
            p.id = produto.id
            p.descricao = produto.descricao
            p.quantidade = produto.quantidade
           
        return lista
    
    def FimDaExecucao(self, request, context):
        self._stop_event.set()
        return estoque_pb2.Status(status=len(self.produtos))
    
def serve():
    port = sys.argv[1]

    stop_event = threading.Event()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    estoque_pb2_grpc.add_EstoqueServiceServicer_to_server(EstoqueService(stop_event), server)

    server.add_insecure_port(f'0.0.0.0:{port}')

    server.start()
    stop_event.wait()
    server.stop(grace=None)

if __name__ == '__main__':
    serve()
    