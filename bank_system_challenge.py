from abc import ABC, abstractmethod
from datetime import date, datetime

# FUNÇÕES AUXILIARES DE FORMATAÇÃO

def formatar_moeda(valor: float) -> str:
    """Transforma um float (250.55) na string formatada (R$ 250,55)"""
    return f"R$ {valor:.2f}".replace('.', ',')

def ler_valor_usuario(mensagem: str) -> float:
    """Lê a entrada do usuário aceitando tanto ponto quanto vírgula"""
    entrada = input(mensagem).strip().replace(',', '.')
    return float(entrada)


# INTERFACE E CLASSES DE TRANSAÇÃO

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta) -> bool:
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta) -> bool:
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        return sucesso_transacao


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta) -> bool:
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        return sucesso_transacao

# CLASSE HISTÓRICO

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append({
            "tipo": "saque" if transacao.__class__.__name__ == "Saque" else "deposito",
            "valor": transacao.valor,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


# CLASSES DE CLIENTE

class Cliente:
    def __init__(self, address: str):
        self.endereco = address
        self.contas = []

    def realizar_transacao(self, conta, transacao: Transacao) -> bool:
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# CLASSES DE CONTA

class Conta:
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0.0
        self._saldo_inicial = 0.0  
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def saldo_inicial(self):
        return self._saldo_inicial

    @property
    def numero(self):
        return self._numero

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float) -> bool:
        excedeu_saldo = valor > self.saldo

        if excedeu_saldo:
            print("\n  @@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("\n  @@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            print("\n  @@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == "saque"]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(f"\n  @@@ Operação falhou! O valor excede o limite de {formatar_moeda(self.limite)} por saque. @@@")
            return False

        elif excedeu_saques:
            print("\n  @@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        else:
            return super().sacar(valor)


# FLUXO INTERATIVO

def iniciar_sistema():
    print("==================================================")
    print("           BEM-VINDO AO BANCO PYTHON              ")
    print("==================================================")
    print('')
    nome_usuario = input("  Para iniciar, digite o seu nome: ").strip()
    
    cliente = PessoaFisica(
        cpf="123.456.789-00", 
        nome=nome_usuario, 
        data_nascimento=date(2000, 1, 1), 
        endereco="Av. Paulista, 1000"
    )
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=1)
    cliente.adicionar_conta(conta)

    while True:
        # Menu bem espaçado e com bordas
        print("\n==================================================")
        print(f"  Oi, {cliente.nome}, sua conta corrente tem {formatar_moeda(conta.saldo)}")
        print("  O que gostaria de fazer hoje?")
        print("==================================================")
        print('')
        print("  [1] Sacar")
        print("  [2] Depositar")
        print("  [3] Histórico")
        print("  [0] Sair")
        print('')
        print("--------------------------------------------------")
        print('')
        
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                valor_saque = ler_valor_usuario("\n  --> Informe o quanto deseja sacar: R$ ")
                saque = Saque(valor_saque)
                
                sucesso = cliente.realizar_transacao(conta, saque)
                
                if sucesso:
                    print("\n--------------------------------------------------")
                    print(f"  Você sacou {formatar_moeda(valor_saque)}, agora você tem {formatar_moeda(conta.saldo)}")
                    print("--------------------------------------------------")
            except ValueError:
                print("\n  @@@ Erro! Digite um valor numérico válido (ex: 250,55). @@@")

        elif opcao == "2":
            try:
                valor_deposito = ler_valor_usuario("\n  --> Informe o quanto quer depositar: R$ ")
                deposito = Deposito(valor_deposito)
                
                sucesso = cliente.realizar_transacao(conta, deposito)
                
                if sucesso:
                    print("\n--------------------------------------------------")
                    print(f"  Você depositou {formatar_moeda(valor_deposito)}, agora você tem {formatar_moeda(conta.saldo)}")
                    print("--------------------------------------------------")
            except ValueError:
                print("\n  @@@ Erro! Digite um valor numérico válido (ex: 250,55). @@@")

        elif opcao == "3":
            print("\n  -- Extrato - -")
            print(f"  Seu total era de: {formatar_moeda(conta.saldo_inicial)}")
            print("  ----------------------------------------------")
            
            if not conta.historico.transacoes:
                print("  Nenhuma movimentação realizada.")
            else:
                for t in conta.historico.transacoes:
                    # Alinhamento visual da data, tipo e valor
                    print(f"  {t['data_hora']}  {t['tipo'].ljust(8)}  {formatar_moeda(t['valor'])}")
            
            print("  ----------------------------------------------")
            print(f"  Saldo atual: {formatar_moeda(conta.saldo)}")
            print("  --------------")

        elif opcao == "0":
            print(f"\n  Obrigado por utilizar nosso banco, {cliente.nome}. Até logo!\n")
            break
        else:
            print("\n  @@@ Opção inválida! Tente novamente. @@@")


if __name__ == "__main__":
    iniciar_sistema()