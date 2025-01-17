import grpc
import sys
from concurrent import futures # usado na definição do pool de threads
import threading

import pedidos_pb2, pedidos_pb2_grpc, estoque_pb2, estoque_pb2_grpc # importa modulos gerados no stub junto com modulos do estoque

#
#
#
#
## ********** POSSO CRIAR UMA CLASSE PRA PRODUTO ************
#
#
#
#

class Pedido:
    def __init__(self, id):
        self.id = id
        self.produtos = []
    
    def AddProduto(self, produto_id, status, quantidade):
        self.produtos.append((produto_id, status, quantidade))

class PedidosService(pedidos_pb2_grpc.PedidosServiceServicer):
    def __init__(self, stop_event, server_rpc_estoque):
        self._stop_event = stop_event
        self.pedidos = []
        self.rpc_estoque = server_rpc_estoque

    def CriaPedido(self, request, context):

        lista = pedidos_pb2.ListaIdStatus()
        
        id = 0
        if len(self.pedidos) == 0:
            id = 1
        else: 
            id = self.pedidos[-1].id + 1

        novo_pedido = Pedido(id)

        for item in request.itens:

            prod_id = item.prod_id

            # valor negativo pois estou retirando do estoque
            status = self.rpc_estoque.AlteraQuantidadeDeProduto(self.rpc_estoque.AlteraQuantidadeRequest(prod_id=prod_id, valor=-item.quantidade))

            p = lista.par.add()
            p.id = prod_id
            p.status = status

            novo_pedido.AddProduto(prod_id, status, item.quantidade)
           
        self.pedidos.append(novo_pedido)
        
        return lista
   
    def CancelaPedido(self, request, context):
        
        if len(self.pedidos) < request.id:
            return pedidos_pb2.Status(status=-1)
        
        pedido_removido = self.pedidos.pop(request.id - 1)

        for prod_id, status, quantidade in pedido_removido.produtos:
               
            if status != 0:
                continue

            self.rpc_estoque.AlteraQuantidadeDeProduto(self.rpc_estoque.AlteraQuantidadeRequest(prod_id=prod_id, valor=quantidade))

        return pedidos_pb2.Status(status=0)

    def FimDaExecucao(self, request, context):
        self._stop_event.set()
        return pedidos_pb2.Status(status=len(self.produtos))
       

    
def service_pedidos():
    port = sys.argv[1]
    identificador_rpc_server_estoque = sys.argv[2]

    stop_event = threading.Event()

    # agora Pedidos é cliente de Estoque
    channel_estoque = grpc.insecure_channel(identificador_rpc_server_estoque)
    stub_estoque = estoque_pb2_grpc.EstoqueServiceStub(channel_estoque)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pedidos_pb2_grpc.add_PedidosServiceServicer_to_server(PedidosService(stop_event, stub_estoque), server)

    server.add_insecure_port(f'0.0.0.0:{port}')


    server.start()
    stop_event.wait()
    
    channel_estoque.close()
    server.stop(grace=None)

if __name__ == '__main__':
    service_pedidos()
    