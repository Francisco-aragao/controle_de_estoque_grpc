import grpc 
import sys


import estoque_pb2, estoque_pb2_grpc

def AdicionaProduto(stub, quantidade, descricao):
    produto_id = stub.AdicionaProduto(estoque_pb2.ProdutoRequest(quantidade=quantidade, descricao=descricao))

    print(produto_id.id)
   
def AlteraQuantidadeDeProduto(stub, prod_id, valor):
    status = stub.AlteraQuantidadeDeProduto(estoque_pb2.AlteraQuantidadeRequest(prod_id=prod_id, valor=valor))

    print(status.status)
       
def ListaProdutos(stub):
    lista = stub.ListaProdutos(estoque_pb2.EmptyRequest())

    for produto in lista.produtos:
        print(f'{produto.id} - {produto.descricao} - {produto.quantidade}')

def FimDaExecucao(stub):
    status = stub.FimDaExecucao(estoque_pb2.EmptyRequest())

    print(status.status)

def processa_comandos(stub):
    commands = ['P', 'Q', 'L', 'F']

    for line in sys.stdin:
        if not line or not line.strip() or line[0] not in commands:
            continue
        operacao, *args = line.strip().split()
        if operacao == 'P':
            AdicionaProduto(stub, int(args[0]), args[1])
        elif operacao == 'Q':
            AlteraQuantidadeDeProduto(stub, int(args[0]), int(args[1]))
        elif operacao == 'L':
            ListaProdutos(stub)
        elif operacao == 'F':
            FimDaExecucao(stub)
            break

def run():
    _, servidor = sys.argv

    channel = grpc.insecure_channel(servidor)
    stub = estoque_pb2_grpc.EstoqueServiceStub(channel)

    processa_comandos(stub)
    
    channel.close()


if __name__ == '__main__':
    run()