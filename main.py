import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) #ISSO AQUI TIRA UM AVISO CHATO QUE ESTA DANDO POR CONTA DO PYTHON ANTIGO, EM PROXIMOS COMMITS MUDO ISSO.
import sqlite3
from modulos import(Menu, MenuLogado, Registrar, Login, TranferirDinheiro, SacarDinheiro, DepositarDinheiro, VisualizarUsuarios, ExcluirCliente, ExcluirConta, MenuAdmin)
from time import sleep

conexao = sqlite3.connect("BancoDeDados.db")
cursor = conexao.cursor()


print('-='*15)
print(" BEM VINDO AO BANCO MONCORVO")
print("   ONDE VOCE PODE CONFIAR")
print('=-'*15)

funcionando = True
while funcionando:
    menu = Menu()
    match menu:
        case 1: 
            login = Login() #isso aqui e para salvar o usuario, para indicar as funcoes que e esse usuario que esta fazendo as acoes
            while True: #esse while true mantem o usuario no MENU de logado, que e diferento do menu inicial.
                menu_logado = MenuLogado()
                match menu_logado:
                    case 1:
                        tranferindo = True
                        while tranferindo:
                            TranferirDinheiro(login) 
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
                                    print('DIGITE UMA OPCAO VALIDA "S" OU "N"')#
                                    continue
                    case 2:
                        SacarDinheiro(login)
                    case 3:
                        DepositarDinheiro(login)
                    case 4:
                        break
                    case 5:
                        funcionando = False
                        print('Obrigado por usar nosso Banco...')
                        print('Volte sempre')
                        break
                    case 6:
                        ExcluirConta(login)
                        break
        case 2:
            registrar = Registrar()
            print('VOLTANDO AO MENU')
        case 3:
            while True:
                menuAdmin = MenuAdmin()
                match menuAdmin:
                    case 1:
                        VisualizarUsuarios()
                        opcao = input('QUER CONTINUAR NO MEU DE ADM OU VOLTAR AO MENU PRINCIPAL? [1/2]')
                        if opcao == 1:
                            continue
                        elif opcao == 2:
                            break
                    case 2:
                        Excluir()
                        opcao = input('QUER CONTINUAR NO MEU DE ADM OU VOLTAR AO MENU PRINCIPAL? [1/2]')
                        if opcao == 1:
                            continue
                        elif opcao == 2:
                            break
                    case 3:
                        print('EM CONSTRUCAO')
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