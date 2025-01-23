import grpc
import sys

import estoque_pb2, estoque_pb2_grpc

# cliente apenas chama as funções e imprime as respostas


def AdicionaProduto(stub, quantidade, descricao):
    produto_id = stub.AdicionaProduto(
        estoque_pb2.ProdutoRequest(quantidade=quantidade, descricao=descricao)
    )

    print(produto_id.id)


def AlteraQuantidadeDeProduto(stub, prod_id, valor):
    status = stub.AlteraQuantidadeDeProduto(
        estoque_pb2.AlteraQuantidadeRequest(prod_id=prod_id, valor=valor)
    )

    print(status.status)


def ListaProdutos(stub):
    lista = stub.ListaProdutos(estoque_pb2.EmptyRequest())

    for produto in lista.produtos:
        print(f"{produto.id} {produto.quantidade} {produto.descricao}")


def FimDaExecucao(stub):
    status = stub.FimDaExecucao(estoque_pb2.EmptyRequest())

    print(status.status)


def main(servidor):

    # criando canal de comunicação com servidor de estoque
    channel = grpc.insecure_channel(servidor)
    stub = estoque_pb2_grpc.EstoqueServiceStub(channel)

    # leio comandos da entrada pra fazer operações
    for command in sys.stdin:
        if not command.strip():
            continue
           
        # quebro a string de entrada no primeiro valor e nos demais argumentos
        procedimentos, *args = command.strip().split()
        if procedimentos == "P":
            # recebendo a descrição que pode conter espaços
            descricao = " ".join(args[1:])
            AdicionaProduto(stub, int(args[0]), descricao)
        elif procedimentos == "Q":
            AlteraQuantidadeDeProduto(stub, int(args[0]), int(args[1]))
        elif procedimentos == "L":
            ListaProdutos(stub)
        elif procedimentos == "F":
            FimDaExecucao(stub)
            break

    channel.close()


if __name__ == "__main__":
    _, servidor = sys.argv
    main(servidor)
