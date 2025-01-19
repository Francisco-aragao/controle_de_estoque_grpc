import grpc 
import sys


import estoque_pb2, estoque_pb2_grpc, pedidos_pb2, pedidos_pb2_grpc


def CriaPedido(stubPedidos, lista_itens):
    
    lista_itens_pedidos = pedidos_pb2.ListaDeItens()

    for item in lista_itens:
        item_pedido = lista_itens_pedidos.itens.add()
        item_pedido.prod_id = item[0]
        item_pedido.quantidade = item[1]
    
    response = stubPedidos.CriaPedido(lista_itens_pedidos)

    for item in response.par:
        print(f'{item.pedido_id} {item.status}')


def CancelaPedido(stubPedidos, pedido_id):

    response = stubPedidos.CancelaPedido(pedidos_pb2.PedidoId(id=pedido_id))

    print(response.status)
  
def FimDaExecucao(stubPedidos):
    response = stubPedidos.FimDaExecucao(pedidos_pb2.Empty())

    print(f'{response.estoque_status} {response.pedidos_ativos}')


def processa_comandos(stubPedidos):
    commands = ['P', 'X', 'F']

    for line in sys.stdin:
        if not line or not line.strip() or line[0] not in commands:
            continue

        operacao, *args = line.strip().split()
        if operacao == 'P':
            # P prod1 quant1 prod2 quant 2 ...
            # quero ler os produtos e quantidades e armazenar em uma lista
            lista_itens = []
            for i in range(0, len(args), 2):
                lista_itens.append((int(args[i]), int(args[i+1])))
        
            CriaPedido(stubPedidos, lista_itens)
        elif operacao == 'X':
            CancelaPedido(stubPedidos, int(args[0]))
        elif operacao == 'F':
            FimDaExecucao(stubPedidos)
            break
                

def client_pedidos():
    _, servidorEstoque, servidorPedidos = sys.argv

    channel = grpc.insecure_channel(servidorEstoque)
    stubEstoque = estoque_pb2_grpc.EstoqueServiceStub(channel)

    channel = grpc.insecure_channel(servidorPedidos)
    stubPedidos = pedidos_pb2_grpc.PedidosServiceStub(channel)

    processa_comandos(stubPedidos)
    
    channel.close()


if __name__ == '__main__':
    client_pedidos()