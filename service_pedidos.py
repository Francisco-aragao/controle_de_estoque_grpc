import grpc
import sys
from concurrent import futures # usado na definição do pool de threads
import threading

import pedidos_pb2, pedidos_pb2_grpc # importa modulos gerados no stub


class EstoqueService(estoque_pb2_grpc.EstoqueServiceServicer):
    def __init__(self, stop_event):
        self.produtos = []
        self._stop_event = stop_event
       
    def AdicionaProduto(self, request, context):

    
def service_pedidos():
    port = sys.argv[1]

    stop_event = threading.Event()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    estoque_pb2_grpc.add_EstoqueServiceServicer_to_server(EstoqueService(stop_event), server)

    server.add_insecure_port(f'0.0.0.0:{port}')

    server.start()
    stop_event.wait()
    server.stop(grace=None)

if __name__ == '__main__':
    service_pedidos()
    