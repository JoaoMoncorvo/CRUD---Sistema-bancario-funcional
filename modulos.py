import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sqlite3
import datetime
from time import sleep

def Menu():
    print('Menu do Banco Moncorvo')
    print('1 - Entrar')
    print('2 - Registrar')
    print('3 - Login(ADMIN)')
    print('4 - SAIR')
    print('-='*12)
    while True:
        opcao = int(input('Digite a acao correspondente ao indice (ex: 1 = Entrar): '))
        if opcao >= 1 and opcao <= 4:
            return opcao
            break
        else:
            print('DIGITE APENAS UMA DAS OPCOES ACIMA: 1, 2 OU 3.')

def Registrar(cursor, conexao, data):
    print('Vamos, comecar o seu processo de registro no Banco Moncorvo, primeiramente')
    nome = str(input('Digite o seu primeiro e ultimo nome: '))
    while True:
        senha = input('Agora digite a senha que voce quer por(6 digitos): ')
        try:
            int(senha)
        except ValueError:
            print('SUA SENHA NAO FOI ESCRITA SOMENTE COM NUMEROS, DIGITE UMA SENHA COM 6 DIGITOS, APENAS NUMEROS, EXEMPLO: 123456')
            continue
        if len(senha) != 6:
            print('SUA SENHA TEVE MENOS OU MAIS DE 6 DIGITOS, DIGITE UMA SENHA COM 6 DIGITOS, APENAS NUMEROS, EXEMPLO: 123456')
            continue
        break
    cursor.execute("""
    INSERT INTO Clientes (nome, saldo, DataCriacao, senha)
    VALUES (?, ?, ?, ?)
    """, (nome, 0, data, senha))
    conexao.commit()
    cursor.execute('SELECT * FROM Clientes')
    clientes = cursor.fetchall() 
    for cliente in clientes:
        if cliente[1] == nome and cliente[4] == senha and cliente[2] == 0:
            print(f'Bem vindo {nome}, ao Banco Moncorvo. Seu ID e {cliente[0]}')

def Login(cursor):
    print('=-'*12)
    print("  TELA DE LOGIN")
    print('-='*12)
    while True:
        identificacao = int(input('me diga o Seu ID:'))
        cursor.execute(F'SELECT * FROM Clientes WHERE id = {identificacao}')
        AnalisarID = cursor.fetchall()
        if AnalisarID == []:
            print('ID NAO ENCONTRADO, DIGITE UM ID VALIDO')
        else:
            break
    parador = False
    while parador == False:
        senhaDada = input('Digite a sua senha de acesso: ')
        cursor.execute(f'SELECT * FROM Clientes')
        clientes = cursor.fetchall()
        for cliente in clientes:
            if cliente[0] == identificacao:
                if cliente[4] == senhaDada:
                    print(f'senha correta, usuario conectado, BEM VINDO {cliente[1]}')
                    return cliente[0]
                    parador = True
                    break
                else:
                    print('senha incorreta, tente novamente.')

def TranferirDinheiro(login, cursor, conexao, cursor_logs, conexao_logs, data):
    cursor.execute(f'SELECT * FROM Clientes WHERE id = {login}')
    cliente = cursor.fetchall()
    print('-='*15)
    print(f'SALDO:R$ {cliente[0][2]}')
    print(f'ID: {cliente[0][0]}')
    print(f'NOME: {cliente[0][1]}')
    print('=-'*15)
    while True:
        valor = float(input('Escreva o valor que quer tranferir: R$'))
        if valor > cliente[0][2]:
            print(f'Nao e possivel fazer essa transacao, saldo insuficiente, lembrando que voce tem exatos R${cliente[0][2]} na conta.')
            continue
        else:
            break
    while True:
        identificador = int(input('Escreva o ID da pessoa que voce quer tranferir o dinheiro: '))
        cursor.execute(f'SELECT * FROM Clientes WHERE id = {identificador}')
        recebedor = cursor.fetchall()
        if recebedor == []:
            print('USUARIO NAO ENCONTRADO, TENTE NOVAMENTE')
        else:
            opcao = str(input((f'voce quer tranferir para o id:{identificador} pertencente ao {recebedor[0][1]}, certo? [S/N]'))).upper()
            if opcao == 'S':
                cursor.execute("""
                UPDATE Clientes
                SET saldo = saldo - ?
                WHERE id = ?""",
                (valor, login))
                cursor.execute("""
                UPDATE Clientes
                SET saldo = saldo + ?
                WHERE id = ?""",
                (valor, identificador))
                conexao.commit()
                
                # AGORA USA O CURSOR_LOGS PARA INSERIR NO BANCO DE LOGS
                cursor_logs.execute("""
                 INSERT INTO LogTransacoes (tipo, pagador, recebedor, quantia, data)
                 VALUES(?, ?, ?, ?, ?)
                 """, ('transferencia', cliente[0][0], identificador, valor, data))
                conexao_logs.commit()
                
                print(f'R${valor} tranferido para {recebedor[0][1]}, agora voce tem R${cliente[0][2] - valor} restantes na conta')
                break
            if opcao == 'N':
                continue

def SacarDinheiro(login, cursor, conexao):
    cursor.execute(f'SELECT * FROM Clientes WHERE id = {login}')
    cliente = cursor.fetchall()
    print('-='*15)
    print(f'SALDO:R$ {cliente[0][2]}')
    print(f'ID: {cliente[0][0]}')
    print(f'NOME: {cliente[0][1]}')
    print('=-'*15)
    while True:
        valor = float(input('Me diga o valor que quer sacar: R$'))
        if valor > cliente[0][2]:
            print(f'Nao e possivel sacar esse dinehiro, saldo insuficiente, lembrando que voce tem exatos R${cliente[0][2]} na conta.')
            continue
        else:
            print(f'sacando {valor} em notas...')
            print(f'agora seu saldo atual e de R${cliente[0][2] - valor}')
            cursor.execute("""
            UPDATE Clientes
            SET saldo = saldo - ?
            WHERE id = ?""",
            (valor, login))
            conexao.commit()
            break

def DepositarDinheiro(login, cursor, conexao):
    cursor.execute(f'SELECT * FROM Clientes WHERE id = {login}')
    cliente = cursor.fetchall()
    print('-='*15)
    print(f'SALDO:R$ {cliente[0][2]}')
    print(f'ID: {cliente[0][0]}')
    print(f'NOME: {cliente[0][1]}')
    print('=-'*15)
    valor = float(input('Quanto deseja Depositar?? R$'))
    print(f'Depositando R${valor}')
    cursor.execute("""
    UPDATE Clientes
    SET saldo = saldo + ?
    WHERE id = ?""",
    (valor, login))
    conexao.commit()

def MenuLogado():
    while True:
        print('-='*15)
        print('BANCO MONCORVO')
        print('1 - Tranferir dinheiro')
        print('2 - Sacar dinheiro')
        print('3 - Depositar dinheiro')
        print('4 - Ver extrato bancario')
        print('5 - Volta ao Menu principal')
        print('6 - SAIR')
        print('7 - EXCLUIR CONTA')
        print('=-'*15)
        opcao = int(input('escreva a razao correspondente ao indice: '))
        if opcao < 1 or opcao > 6:
            print('Digite um numero valido! 1, 2, 3, 4, 5 ou 6')
            continue
        else:
            return opcao
            break

def VisualizarUsuarios(cursor):
    cursor.execute('SELECT * FROM Clientes')
    listagem = cursor.fetchall()
    for cliente in listagem:
        print(f'ID - {cliente[0]} | Nome - {cliente[1]} | Data de criacao - {cliente[3]} | Saldo - R${cliente[2]}')

def ExcluirCliente(cursor, conexao):
    funcionando = True
    while funcionando:
        opcao = str(input('Voce sabe o ID do Cliente que voce quer excluir do sistema[S/N]? se nao souber, sabe o nome[M]? ')).upper()
        if opcao == 'S':
            while True:
                idCliente = int(input('Digite o ID do cliente que voce quer excluir: '))
                cursor.execute(f'SELECT * FROM Clientes WHERE id = {idCliente}')
                clienteEscolhido = cursor.fetchall()
                if clienteEscolhido == []:
                    print('ID nao encontrado, por favor digite um id valido, vou listar pra voce todos os clientes... ')
                    sleep(2)
                    VisualizarUsuarios(cursor)
                else:
                    opcaoFinal = str(input(f'TEM CERTEZA QUE DESEJA EXCLUIR O CLIENTE "{clienteEscolhido[0][1]}" COM ID: {idCliente} ?? [S/N] ')).upper()
                    if opcaoFinal == 'S':
                        cursor.execute("""
                        DELETE FROM Clientes
                        WHERE id = ?""",
                        (idCliente,))
                        conexao.commit()
                        print(f'USUARIO {clienteEscolhido[0][1]} EXCLUIDO COM SUCESSO.' )
                        opcaoFinal2 = int(input('Quer excluir mais um[1] ou voltar ao menu ADMIN[2]? [1/2]'))
                        if opcaoFinal2 == 2:
                            funcionando = False
                        break
                    else:
                        funcionando = False
                        break
        elif opcao == 'N':
            print('Ok, irei listar os clientes pra voce e perguntar denovo o ID')
            VisualizarUsuarios(cursor)
            continue
        elif opcao == 'M':
            clientesLista = []
            nomeCliente = str(input('Me diga exatamente o nome completo do cliente que voce quer Excluir: '))
            cursor.execute(f'SELECT * FROM Clientes')
            clientes = cursor.fetchall()
            for cliente in clientes:
                if cliente[1] == nomeCliente:
                    print(f'{len(clientesLista) + 1} - {cliente}')
                    clientesLista.append(cliente)
            if clientesLista == []:
                print('Nenhum cliente encontrado com esse nome')
                continue
            else:
                escolhaFinal = int(input('Escolha o cliente que quer excluir com base no indice ao lado: '))
                print(f'EXCLUINDO O CLIENTE COM ID: {clientesLista[escolhaFinal-1][0]}')
                cursor.execute(f'DELETE FROM Clientes WHERE id = {clientesLista[escolhaFinal-1][0]}')
                conexao.commit()
                opcao = int(input('Quer excluir mais um[1] ou voltar ao menu ADMIN[2]? [1/2]'))
                if opcao == 2:
                    funcionando = False
                elif opcao == 1:
                    continue
        else:
            print('DIGITE UMA OPCAO VALIDA, "S" se souber o ID, "N" se nao souber, vou listar pra voce todos os clientes e "M" se voce sabe apenas o nome, vou listar todos os clientes com esse nome.')

def ExcluirConta(login, cursor, conexao):
    cursor.execute(f'SELECT * FROM Clientes WHERE id = {login}')
    cliente = cursor.fetchall()
    if cliente[0][2] > 0:
        print('IMPOSSIVEL EXCLUIR UMA CONTA COM SALDO MAIOR QUE 0 (ZERO), TRANSFIRA OU SAQUE ESSE DINHEIRO ANTES.')
    else:
        while True:
            perguntafinal = input(f'{cliente[0][1]} TEM CERTEZA QUE DESEJA EXCLUIR SUA CONTA?? [S/N]').upper()
            if perguntafinal == 'S':
                print('EXCLUINDO A CONTA... OBRIGADO POR USAR NOSSO SERVICOS')
                print('Banco Moncorvo agradece!')
                cursor.execute("""
                DELETE FROM Clientes
                WHERE id = ?""",
                (cliente[0][0],))
                conexao.commit()
                break
            elif perguntafinal == 'N':
                print('OK, voltando ao Menu...')
                break
            else:
                print('DIGITE UMA OPCAO VALIDA!')

def MenuAdmin():
    print('-='*15)
    print('NOVO MENU ADMIN')
    print('1 - Visualizar usuarios')
    print('2 - Excluir Usuario')
    print('3 - Ver logs de transacoes')
    print('4 - Mudar infomacao de alguem (EM BREVE)')
    print('5 - Voltar ao Menu')
    print('=-'*15)
    while True:
        opcao = int(input('Digite a opcao: '))
        if opcao > 0 and opcao < 6:
            return opcao
            break
        else:
            print('digite uma opcao valida')
            continue

def VisualizarTransacoesAdmin(cursor_logs):
    cursor_logs.execute("SELECT * FROM LogTransacoes")

    logs = cursor_logs.fetchall()

    for log in logs:
        print(f'DATA: {log[4]}, TIPO: {log[0]}, QUANTIA: {log[3]}, RECEBEDOR: {log[2]}, PAGADOR: {log[1]}')


def ExtratoBancario(login, cursor, conexao, cursor_logs, conexao_logs):
    print('ACESSANDO SEU EXTRATO BANCARIO')
    cursor_logs.execute(f'SELECT * FROM LogTransacoes WHERE recebedor = {login} OR pagador = {login}')
    extrato = cursor_logs.fetchall()
    for atividade in extrato:
        print(f'TIPO: {atividade[0]}, PAGADOR: {atividade[1]}, RECEBEDOR: {atividade[2]}, QUANTIA: {atividade[3]}, DATA: {atividade[4]}')



