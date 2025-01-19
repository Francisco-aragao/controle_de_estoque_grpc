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
        
        id = len(self.pedidos) + 1

        novo_pedido : Pedido = Pedido(id)

        for item in request.itens:

            prod_id = item.prod_id

            # valor negativo pois estou retirando do estoque
            response = self.rpc_estoque.AlteraQuantidadeDeProduto(estoque_pb2.AlteraQuantidadeRequest(prod_id=prod_id, valor=-item.quantidade))
            
            status = response.status
            if status >= 0:
                status = 0 # operação bem sucedida
                novo_pedido.AddProduto(prod_id, status, item.quantidade)
                self.pedidos.append(novo_pedido)

            p = lista.par.add()
            p.pedido_id = id
            p.status = status

        return lista
   
    def CancelaPedido(self, request, context):
        
        if len(self.pedidos) < request.id:
            return pedidos_pb2.StatusPedidos(status=-1)
        
        pedido_removido = self.pedidos.pop(request.id - 1)

        print("Pedido removido: ", pedido_removido.produtos)

        for prod_id, status, quantidade in pedido_removido.produtos:
               
            if status != 0:
                continue

            self.rpc_estoque.AlteraQuantidadeDeProduto(estoque_pb2.AlteraQuantidadeRequest(prod_id=prod_id, valor=quantidade))

        return pedidos_pb2.StatusPedidos(status=0)

    def FimDaExecucao(self, request, context):
        response = self.rpc_estoque.FimDaExecucao(estoque_pb2.EmptyRequest())
        self._stop_event.set()



        return pedidos_pb2.FimExecucaoStatus(estoque_status=response.status, pedidos_ativos=len(self.pedidos))
       

    
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
    