
import getpass
import sqlite3

from database.auth import criar_tabela, criar_usuario, conectar


def main():
    criar_tabela()

    with conectar() as conexao:
        quantidade = conexao.execute(
            "SELECT COUNT(*) FROM usuarios"
        ).fetchone()[0]

    if quantidade > 0:
        print("Já existe um usuário cadastrado.")
        return

    print("=== CONFIGURAÇÃO INICIAL DO DEZFOR ===")

    usuario = input("Nome do administrador: ").strip()
    senha = getpass.getpass("Senha (mínimo 12 caracteres): ")
    confirmacao = getpass.getpass("Confirme a senha: ")

    if senha != confirmacao:
        print("As senhas não coincidem.")
        return

    try:
        criar_usuario(usuario, senha)
        print("Administrador criado com sucesso!")
    except ValueError as erro:
        print(f"Erro: {erro}")
    except sqlite3.IntegrityError:
        print("Esse nome de usuário já está cadastrado.")


if __name__ == "__main__":
    main()
