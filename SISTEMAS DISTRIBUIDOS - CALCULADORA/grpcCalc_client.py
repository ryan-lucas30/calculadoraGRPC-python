import grpc
import grpcCalc_pb2
import grpcCalc_pb2_grpc

def mostrar_menu():
    print("\n" + "="*60)
    print("                CALCULADORA gRPC AVANÇADA")
    print("="*60)
    print("1. Adição (+)")
    print("2. Subtração (-)") 
    print("3. Multiplicação (×)")
    print("4. Divisão (÷)")
    print("5. Sair")
    print("="*60)

def obter_numeros(operacao):
    try:
        quantidade = int(input(f"\nQuantos números você deseja {operacao}? (mínimo 2): "))
        
        if quantidade < 2:
            print("❌ É necessário pelo menos 2 números!")
            return None
        
        numeros = []
        print(f"\nDigite os {quantidade} números:")
        
        for i in range(quantidade):
            while True:
                try:
                    num = float(input(f"Número {i+1}: "))
                    numeros.append(num)
                    break
                except ValueError:
                    print("❌ Por favor, digite um número válido!")
        
        return numeros
        
    except ValueError:
        print("❌ Por favor, digite um número válido para a quantidade!")
        return None

def executar_operacao(stub, operacao, numeros):
    try:
        # Cria a requisição com a lista de números
        request = grpcCalc_pb2.OperationRequest(numbers=numeros)
        
        if operacao == 1:  # Adição
            response = stub.Add(request)
            if response.operation_details:
                print(f"\n✅ Resultado: {response.operation_details} = {response.result}")
            
        elif operacao == 2:  # Subtração
            response = stub.Subtract(request)
            if response.operation_details:
                print(f"\n✅ Resultado: {response.operation_details} = {response.result}")
            
        elif operacao == 3:  # Multiplicação
            response = stub.Multiply(request)
            if response.operation_details:
                print(f"\n✅ Resultado: {response.operation_details} = {response.result}")
            
        elif operacao == 4:  # Divisão
            response = stub.Divide(request)
            if response.operation_details:
                print(f"\n✅ Resultado: {response.operation_details} = {response.result}")
            
    except grpc.RpcError as e:
        print(f"\n❌ Erro: {e.details()}")

def main():
    print("Conectando ao servidor da calculadora avançada...")
    
    try:
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = grpcCalc_pb2_grpc.CalculatorStub(channel)
            
            while True:
                mostrar_menu()
                
                try:
                    opcao = int(input("\nEscolha uma operação (1-5): "))
                    
                    if opcao == 5:
                        print("\n👋 Saindo da calculadora. Até mais!")
                        break
                    
                    if opcao < 1 or opcao > 5:
                        print("❌ Opção inválida! Escolha entre 1 e 5.")
                        continue
                    
                    # Nomes das operações para exibição
                    nomes_operacoes = {
                        1: "somar",
                        2: "subtrair", 
                        3: "multiplicar",
                        4: "dividir"
                    }
                    
                    numeros = obter_numeros(nomes_operacoes[opcao])
                    if numeros:
                        executar_operacao(stub, opcao, numeros)
                    
                    input("\nPressione Enter para continuar...")
                    
                except ValueError:
                    print("❌ Por favor, digite um número válido!")
                except KeyboardInterrupt:
                    print("\n\n👋 Programa interrompido pelo usuário.")
                    break
                    
    except grpc.RpcError as e:
        print(f"❌ Erro: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que o servidor está rodando na porta 50052")

if __name__ == '__main__':
    main()