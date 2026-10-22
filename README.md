
# DEZFOR — Gestão Inteligente

Sistema desktop desenvolvido em Python para o gerenciamento de colaboradores, equipamentos e movimentações de estoque.

O projeto foi desenvolvido com o objetivo de aplicar conhecimentos de programação, banco de dados e desenvolvimento de interfaces gráficas na criação de uma solução prática para o ambiente corporativo, auxiliando no gerenciamento de equipamentos utilizados no dia a dia de uma empresa.

O DEZFOR busca facilitar o controle de estoque, o registro de retiradas e devoluções e o acompanhamento das movimentações, proporcionando maior organização, eficiência e rastreabilidade aos processos internos.

## Funcionalidades

- Autenticação de usuários com proteção de senhas
- Dashboard com indicadores gerenciais e movimentações recentes
- Cadastro, consulta, edição e exclusão de colaboradores
- Cadastro e gerenciamento de equipamentos
- Controle de estoque com retiradas e devoluções
- Validação de quantidades e disponibilidade em estoque
- Histórico de movimentações com pesquisa
- Geração de relatórios em PDF
- Proteção administrativa para exclusão do histórico

## Tecnologias utilizadas

- **Python** — Linguagem principal de programação
- **CustomTkinter** — Desenvolvimento da interface gráfica
- **Tkinter/ttk** — Componentes de interface
- **SQLite** — Banco de dados relacional
- **ReportLab** — Geração de relatórios em PDF
- **Git e GitHub** — Versionamento e hospedagem do código

## Estrutura do projeto

    DEZFOR/
    ├── assets/
    │   └── theme/
    │       └── theme.py
    ├── database/
    │   ├── auth.py
    │   └── database.py
    ├── reports/
    │   └── pdf_generator.py
    ├── ui/
    │   ├── colaboradores.py
    │   ├── components.py
    │   ├── configuracoes.py
    │   ├── dashboard.py
    │   ├── equipamentos.py
    │   ├── estoque.py
    │   ├── historico.py
    │   ├── login.py
    │   ├── main_window.py
    │   └── relatorios.py
    ├── .gitignore
    ├── criar_admin.py
    ├── main.py
    ├── README.md
    └── requirements.txt

## Como executar

### Pré-requisitos

- Python 3 instalado
- Git instalado (para clonar o repositório)

### 1. Clonar o repositório

Clone o repositório pelo GitHub e acesse a pasta do projeto.

### 2. Instalar as dependências

No terminal, execute:

    python -m pip install -r requirements.txt

### 3. Configurar o primeiro acesso

Antes de iniciar o sistema pela primeira vez, crie uma conta de administrador executando:

    python criar_admin.py

O programa solicitará:

- Nome do administrador
- Senha com pelo menos 12 caracteres
- Confirmação da senha

Por segurança, a senha não será exibida durante a digitação.

**Importante:** o cadastro inicial só é permitido quando ainda não existe nenhum usuário registrado no banco de dados.

### 4. Iniciar o sistema

Após criar a conta, execute:

    python main.py

Utilize o nome de usuário e a senha cadastrados para acessar o DEZFOR.

O banco de dados SQLite é criado automaticamente durante a configuração inicial.

## Segurança

O DEZFOR implementa mecanismos de segurança e integridade dos dados, incluindo:

- Armazenamento de senhas com PBKDF2-HMAC-SHA256 e salt aleatório
- Senhas com no mínimo 12 caracteres
- Consultas SQL parametrizadas
- Validação de movimentações de estoque
- Prevenção de retiradas superiores à quantidade disponível
- Registro de movimentações e atualização de estoque na mesma transação
- Confirmação de senha administrativa para exclusão do histórico
- Exclusão do banco de dados local do controle de versão por meio do `.gitignore`

O sistema não utiliza credenciais administrativas padrão.

## Objetivo do projeto

Desenvolver uma aplicação desktop para auxiliar empresas no gerenciamento de equipamentos, permitindo organizar cadastros, controlar quantidades disponíveis e registrar movimentações realizadas pelos colaboradores.

Além da aplicação prática, o projeto tem como objetivo consolidar conhecimentos em:

- Lógica de programação
- Desenvolvimento de software com Python
- Interfaces gráficas
- Bancos de dados relacionais
- Autenticação e proteção de senhas
- Validação e integridade de dados
- Organização e manutenção de código
- Versionamento com Git

## Melhorias futuras

- Aprimoramento da interface e experiência do usuário
- Ampliação dos filtros e relatórios gerenciais
- Implementação de diferentes níveis de permissão
- Criação de testes automatizados
- Melhorias no processo de instalação e distribuição

## Status do projeto

**Em desenvolvimento e aprimoramento.**

O sistema possui funcionalidades implementadas de cadastro, gerenciamento de equipamentos, controle de estoque, histórico de movimentações e geração de relatórios.

Atualmente, o projeto está em fase de revisão, documentação e preparação para publicação no GitHub.

## Autor

**Ryan Silva Yuey**

Projeto desenvolvido para aplicação prática de conhecimentos em Tecnologia da Informação e composição de portfólio profissional na área de desenvolvimento de software.
