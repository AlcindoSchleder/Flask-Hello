# -*- coding: utf-8 -*-
import hmac
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

""" 
    unit        : utils
    descritption: Collection of functions used in all projetcts
    author      : Alcindo Schleder
    version     : 1.0.0
"""


def is_number(value) -> bool:
    """
    Função que verifica se o parametro value é um número
    @param value: valor a ser verificado
    @return: Boolean
    """
    try:
        float(value)
    except ValueError:
        return False
    return True


def calc_file_signature(data: str, password: str = None) -> str:
    """
    Função que calcula o has da assinatura de um arquivo
    @param data: string assinada
    @param password: senha da assinatura
    @return: hash da assinatura
    """
    if (password):
        digest  = hmac.new(bytes(password), msg=bytes(data), digestmod=hashlib.sha256).digest()
        res_hash = base64.b64encode(digest).decode()
    else:
        hash = hashlib.sha256()
        hash.update(bytes(data))
        res_hash = hash.hexdigest()
    return res_hash


def encrypt(key: bytes, source: str, encode=True) -> str:
    """
    Função para criptografar uma string
    @param key: Senha para criptografar
    @param source: string a ser criptografada
    @param encode: Flag que indica se o resultado deve ser codificado para base64
    @return: string criptografada
    """
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data


def decrypt(key: bytes, source: str, decode=True) -> str:
    """
    Função que descriptografa uma string criptografada com utils.encrypt
    @param key: Senha para descriptografar
    @param source: string criptografada a ser descriptografada
    @param decode: Flag que indica se a string deve ser decodificado de base64
    @return: string descriptografada
    """
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding


def network_connection(url: str = 'www.google.com.br', to: int = 3) -> bool:
    """
    Função que verifica a conexão com a internet
    @param url: url na rede a ser testado
    @param to: timeout para exceção
    @return: bool
    """
    try:
        import httplib
    except:
        import http.client as httplib
    conn = httplib.HTTPConnection(url, timeout=to)
    try:
        conn.request("HEAD", "/")
        conn.close()
        res = True
    except:
        res = False
    return res
