import grpc
from concurrent import futures
import grpcCalc_pb2
import grpcCalc_pb2_grpc

class CalculatorServicer(grpcCalc_pb2_grpc.CalculatorServicer):

    def Add(self, request, context):
        if len(request.numbers) < 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('São necessários pelo menos 2 números para adição')
            return grpcCalc_pb2.OperationResponse()
        
        result = sum(request.numbers)
        details = " + ".join(str(n) for n in request.numbers)
        print(f"Adição: {details} = {result}")
        return grpcCalc_pb2.OperationResponse(result=result, operation_details=details)

    def Subtract(self, request, context):
        if len(request.numbers) < 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('São necessários pelo menos 2 números para subtração')
            return grpcCalc_pb2.OperationResponse()
        
        result = request.numbers[0]
        for num in request.numbers[1:]:
            result -= num
        
        details = " - ".join(str(n) for n in request.numbers)
        print(f"Subtração: {details} = {result}")
        return grpcCalc_pb2.OperationResponse(result=result, operation_details=details)

    def Multiply(self, request, context):
        if len(request.numbers) < 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('São necessários pelo menos 2 números para multiplicação')
            return grpcCalc_pb2.OperationResponse()
        
        result = 1
        for num in request.numbers:
            result *= num
        
        details = " × ".join(str(n) for n in request.numbers)
        print(f"Multiplicação: {details} = {result}")
        return grpcCalc_pb2.OperationResponse(result=result, operation_details=details)

    def Divide(self, request, context):
        if len(request.numbers) < 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('São necessários pelo menos 2 números para divisão')
            return grpcCalc_pb2.OperationResponse()
        
        # Verifica se há zero nos denominadores
        for num in request.numbers[1:]:
            if num == 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Divisão por zero não é permitida')
                return grpcCalc_pb2.OperationResponse()
        
        result = request.numbers[0]
        for num in request.numbers[1:]:
            result /= num
        
        details = " ÷ ".join(str(n) for n in request.numbers)
        print(f"Divisão: {details} = {result}")
        return grpcCalc_pb2.OperationResponse(result=result, operation_details=details)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcCalc_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    
    port = 50052
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor Calculadora rodando na porta {port}...")
    print("Aguardando solicitações do cliente...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()