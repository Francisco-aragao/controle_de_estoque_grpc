import grpc
import sys

import estoque_pb2, estoque_pb2_grpc

# cliente apenas chama as funções e imprime as respostas


class EstoqueClient:
    def __init__(self, servidorEstoque):
        # cria um canal de comunicação com o servidor de estoque
        self.channel = grpc.insecure_channel(servidorEstoque)
        self.stub = estoque_pb2_grpc.EstoqueServiceStub(self.channel)

    def AdicionaProduto(self, quantidade, descricao):
        produto_id = self.stub.AdicionaProduto(
            estoque_pb2.ProdutoRequest(quantidade=quantidade, descricao=descricao)
        )

        print(produto_id.id)

    def AlteraQuantidadeDeProduto(self, prod_id, valor):
        status = self.stub.AlteraQuantidadeDeProduto(
            estoque_pb2.AlteraQuantidadeRequest(prod_id=prod_id, valor=valor)
        )

        print(status.status)

    def ListaProdutos(self):
        lista = self.stub.ListaProdutos(estoque_pb2.EmptyRequest())

        for produto in lista.produtos:
            print(f"{produto.id} {produto.quantidade} {produto.descricao}")

    def FimDaExecucao(self):
        status = self.stub.FimDaExecucao(estoque_pb2.EmptyRequest())

        print(status.status)

        self.channel.close()


def main(servidorEstoque):
    client = EstoqueClient(servidorEstoque)

    # leio comandos da entrada pra fazer operações
    for command in sys.stdin:
        if not command.strip():
            continue

        # quebro a string de entrada no primeiro valor e nos demais argumentos
        procedimentos, *args = command.strip().split()
        if procedimentos == "P":
            # recebendo a descrição que pode conter espaços
            descricao = " ".join(args[1:])
            client.AdicionaProduto(int(args[0]), descricao)
        elif procedimentos == "Q":
            client.AlteraQuantidadeDeProduto(int(args[0]), int(args[1]))
        elif procedimentos == "L":
            client.ListaProdutos()
        elif procedimentos == "F":
            client.FimDaExecucao()
            break


if __name__ == "__main__":
    _, servidorEstoque = sys.argv
    main(servidorEstoque)
