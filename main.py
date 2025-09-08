import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sqlite3
from modulos import(Menu, MenuLogado, Registrar, Login, TranferirDinheiro, SacarDinheiro, DepositarDinheiro, VisualizarUsuarios, ExcluirCliente, ExcluirConta, MenuAdmin, VisualizarTransacoesAdmin)
from time import sleep
import datetime

# Conecta aos dois bancos de dados separadamente
conexao = sqlite3.connect("BancoDeDados.db")
cursor = conexao.cursor()

conexao_logs = sqlite3.connect("LogTransacoes.db")
cursor_logs = conexao_logs.cursor()

# cria as tabelas se nao existirem
cursor.execute("""         
CREATE TABLE IF NOT EXISTS Clientes
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    saldo REAL NOT NULL,
    DataCriacao DATE NOT NULL,
    senha TEXT NOT NULL)""")
conexao.commit()

cursor_logs.execute("""
CREATE TABLE IF NOT EXISTS LogTransacoes
    (tipo TEXT NOT NULL,
    pagador INTEGER NOT NULL,
    recebedor INTEGER NOT NULL,
    quantia REAL NOT NULL,
    data DATE NOT NULL)""")
conexao_logs.commit()

data = datetime.date.today()

print('-='*15)
print(" BEM VINDO AO BANCO MONCORVO")
print("   ONDE VOCE PODE CONFIAR")
print('=-'*15)

funcionando = True
while funcionando:
    menu = Menu()
    match menu:
        case 1: 
            login = Login(cursor)  # PASSA O CURSOR AQUI
            while True:
                menu_logado = MenuLogado()
                match menu_logado:
                    case 1:
                        tranferindo = True
                        while tranferindo:
                            TranferirDinheiro(login, cursor, conexao, cursor_logs, conexao_logs, data)
                            while True:
                                opcao = str(input('Deseja tranferir para mais pessoas? [S/N]')).upper()
                                if opcao == 'S':
                                    break
                                elif opcao == 'N':
                                    tranferindo = False
                                    print('Obrigado por usar nosso Banco...')
                                    print('Volte sempre')
                                    break
                                else:
                                    print('DIGITE UMA OPCAO VALIDA "S" OU "N"')
                                    continue
                    case 2:
                        SacarDinheiro(login, cursor, conexao)
                    case 3:
                        DepositarDinheiro(login, cursor, conexao)
                    case 4:
                        break
                    case 5:
                        funcionando = False
                        print('Obrigado por usar nosso Banco...')
                        print('Volte sempre')
                        break
                    case 6:
                        ExcluirConta(login, cursor, conexao)
                        break
        case 2:
            Registrar(cursor, conexao, data)
            print('VOLTANDO AO MENU')
        case 3:
            while True:
                menuAdmin = MenuAdmin()
                match menuAdmin:
                    case 1:
                        VisualizarUsuarios(cursor)
                        opcao = input('QUER CONTINUAR NO MENU DE ADM OU VOLTAR AO MENU PRINCIPAL? [1/2]')
                        if opcao == '1':
                            continue
                        elif opcao == '2':
                            break
                    case 2:
                        ExcluirCliente(cursor, conexao)
                        opcao = input('QUER CONTINUAR NO MENU DE ADM OU VOLTAR AO MENU PRINCIPAL? [1/2]')
                        if opcao == '1':
                            continue
                        elif opcao == '2':
                            break
                    case 3:
                        VisualizarTransacoesAdmin(cursor_logs)
                        opcao = input('QUER CONTINUAR NO MENU DE ADM OU VOLTAR AO MENU PRINCIPAL? [1/2]')
                        if opcao == '1':
                            continue
                        elif opcao == '2':
                            break
                    case 4:
                        print('EM CONSTRUCAO')
                    case 5:
                        break
                    case _:
                        continue
        case 4:
            print('Obrigado por usar nosso Banco...')
            print('Volte sempre')
            funcionando = False