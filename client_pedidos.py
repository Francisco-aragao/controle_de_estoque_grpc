import grpc
import sys


import estoque_pb2, estoque_pb2_grpc, pedidos_pb2, pedidos_pb2_grpc

# cliente apenas chama as funções e imprime as respostas


def print_listar_produtos_estoque(stubEstoque):
    """
    Essa função envolve diretamente o servidor de estoque. Pelo enunciado do trabalho, ao iniciar o cliente de pedidos, todos os produtos do estoque devem ser listados.
    """

    lista = stubEstoque.ListaProdutos(estoque_pb2.EmptyRequest())

    for produto in lista.produtos:
        print(f"{produto.id} {produto.quantidade} {produto.descricao}")


class PedidosClient:
    def __init__(self, servidorPedidos, servidorEstoque):
        # criando canal de comunicação com servidor de estoque
        channel = grpc.insecure_channel(servidorEstoque)
        stubEstoque = estoque_pb2_grpc.EstoqueServiceStub(channel)

        # imprimo todos os produtos do estoque -> feito antes de iniciar o cliente de pedidos
        print_listar_produtos_estoque(stubEstoque)

        channel.close()

        # cria um canal de comunicação com o servidor de pedidos
        self.channel = grpc.insecure_channel(servidorPedidos)
        self.stub = pedidos_pb2_grpc.PedidosServiceStub(self.channel)

    def CriaPedido(self, lista_itens):
        # criando lista conforme definição no arquivo proto
        lista_itens_pedidos = pedidos_pb2.ListaDeItens()

        for item in lista_itens:
            item_pedido = lista_itens_pedidos.itens.add()
            item_pedido.prod_id = item[0]
            item_pedido.quantidade = item[1]

        response = self.stub.CriaPedido(lista_itens_pedidos)

        for item in response.par:
            print(f"{item.prod_id} {item.status}")

    def CancelaPedido(self, pedido_id):
        response = self.stub.CancelaPedido(pedidos_pb2.PedidoId(id=pedido_id))

        print(response.status)

    def FimDaExecucao(self):
        response = self.stub.FimDaExecucao(pedidos_pb2.Empty())

        print(f"{response.estoque_status} {response.pedidos_ativos}")

        self.channel.close()


def main(servidorEstoque, servidorPedidos):

    client = PedidosClient(servidorPedidos, servidorEstoque)

    # leio comandos da entrada pra fazer operações
    for command in sys.stdin:
        if not command.strip():
            continue

        # quebro a string de entrada no primeiro valor e nos demais argumentos
        procedimentos, *args = command.strip().split()
        if procedimentos == "P":
            # leio cada um dos produtos passados no terminal
            lista_itens = []
            for i in range(0, len(args), 2):
                lista_itens.append((int(args[i]), int(args[i + 1])))

            client.CriaPedido(lista_itens)
        elif procedimentos == "X":
            client.CancelaPedido(int(args[0]))
        elif procedimentos == "T":
            client.FimDaExecucao()
            break


if __name__ == "__main__":
    _, servidorEstoque, servidorPedidos = sys.argv
    main(servidorEstoque, servidorPedidos)
