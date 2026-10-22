
import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "nr35.db"
ITERACOES = 600_000


def conectar():
    return sqlite3.connect(DB_PATH)


def criar_tabela():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            )
        """)


def gerar_hash(senha):
    salt = secrets.token_bytes(16)

    chave = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        ITERACOES
    )

    return f"{salt.hex()}${chave.hex()}"


def verificar_senha(senha, senha_hash):
    try:
        salt_hex, hash_hex = senha_hash.split("$")

        chave = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            bytes.fromhex(salt_hex),
            ITERACOES
        )

        return hmac.compare_digest(
            chave,
            bytes.fromhex(hash_hex)
        )

    except (ValueError, TypeError):
        return False


def criar_usuario(usuario, senha):
    usuario = usuario.strip()

    if not usuario:
        raise ValueError("Informe um nome de usuário.")

    if len(senha) < 12:
        raise ValueError(
            "A senha deve conter pelo menos 12 caracteres."
        )

    criar_tabela()

    with conectar() as conexao:
        conexao.execute("""
            INSERT INTO usuarios (usuario, senha_hash)
            VALUES (?, ?)
        """, (usuario, gerar_hash(senha)))


def autenticar(usuario, senha):
    criar_tabela()

    with conectar() as conexao:
        registro = conexao.execute("""
            SELECT senha_hash
            FROM usuarios
            WHERE usuario = ?
        """, (usuario.strip(),)).fetchone()

    if registro is None:
        return False

    return verificar_senha(senha, registro[0])
