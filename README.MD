# Banco Moncorvo 

Um sistema bancário simples feito em **Python** com **SQLite** para gerenciamento de contas, transferências e saques.

## Funcionalidades
- **Registrar Cliente** com nome e senha de 6 dígitos
- **Login** usando ID e senha
- **Consultar saldo**
- **Depositar dinheiro**
- **Sacar dinheiro**
- **Transferir dinheiro** entre contas
- Menu interativo no terminal

## Tecnologias utilizadas
- Python
- SQLite

##  Estrutura do projeto
-main.py # arquivo principal como diz o nome, onde e gerenciado o menu interativo e funcoes mais visuals.
-modulos.py # Funções do sistema bancário, o cerebro do projeto roda todo aqui, onde ficam as funcoes.
-BancoDeDados.db # Banco SQLite 
-README.md # Documentaçao do projeto

## Atualizacoes em um futuro muito proximo, conforme vou atualizando vou marcando um X
- [ ]**Visualizacao completa das logs** quando logado como ADMIN, vai ter a opcao de ver a LOG de todas as tranferencias, aberturas de conta e etc
- [ ]**Historico de transacao** Usuario vai conseguir ver seu extrato
- [ ]**Sistema de autenticacao** vou implementar hashs nas senhas
- [ ]**Manipulacao total dos dados** quando logado como ADMIN, ele vai conseguir manipular oque ele quiser dos bancos de dados
- [ ]**Interface Grafica** pretendo fazer uma interface grafica simples, porem necessito de mais estudo nessa parte.

