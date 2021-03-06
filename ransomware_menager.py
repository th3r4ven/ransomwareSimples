#  Copyright (c) 2020.
#  This code was designed and created by TH3R4VEN, its use is encouraged for academic and professional purposes.
#  I am not responsible for improper or illegal uses
#  Follow me on GitHub: https://github.com/th3r4ven

from Crypto.Cipher import AES
import base64
import sys
import re


def getKey():
    try:
        if len(sys.argv[1]) == 32:
            return sys.argv[1]
        else:
            exit()
    except IndexError:
        exit()


def crypt(texto_limpo, ext=""):
    # =================================================================================================================
    # ◥◤  CRYPT STEP BY STEP  ◥◤
    # ▶▶▶▶▶ DATA -> CLEAN_DATA -> SYMMETRIC_DATA -> CRYPTED_DATA -> B64ENCODED_DATA -> 64ENCODED_DATA ◀◀◀◀◀
    # =================================================================================================================

    chave = getKey()
    dado64 = base64.b64encode(texto_limpo)
    texto_limpo = dado64.decode('utf-8')
    teste = True
    cont = len(texto_limpo)
    falta = 0
    while teste:
        if (cont % 256) == 0:
            teste = False
        else:
            texto_limpo = texto_limpo + "1"
            falta += 1
            cont += 1
    # SYMMETRIC_DATA
    aes = AES.new(chave, AES.MODE_ECB)
    cryptado = aes.encrypt(texto_limpo)  # CRYPTED_DATA
    cryptado = base64.b64encode(cryptado)  # B64ENCODED_DATA
    cryptado = cryptado + ";;;;;;;".encode('ascii') + str(falta).encode('ascii') + ",,,,,,,".encode('ascii') + str(ext).encode('ascii')
    return cryptado  # 64ENCODED_DATA


def decrypt(texto_crypto):
    # =================================================================================================================
    # ◥◤  DECRYPT STEP BY STEP  ◥◤
    # ▶▶▶▶▶ 64ENCODED_DATA -> B64ENCODED_DATA -> CRYPTED_DATA -> BINARY_DATA -> SYMMETRIC_DATA -> DATA ◀◀◀◀◀
    # =================================================================================================================

    aes = AES.new(getKey(), AES.MODE_ECB)

    if re.search(b';;;;;;;', texto_crypto):

        cryptData = texto_crypto.split(b';;;;;;;')[0]
        preBit = texto_crypto.split(b';;;;;;;')[1]
        bits = preBit.split(b',,,,,,,')[0].decode('ascii')
        ext = preBit.split(b',,,,,,,')[1].decode('ascii')
        cryptData = base64.b64decode(cryptData)
        descriptado = aes.decrypt(cryptData)
        descriptadob64 = descriptado.decode('ascii')
        original = ""
        for x in range(1, (int(bits))):
            original = original + "1"
        original = descriptadob64.split(original)[0]
        original = original.encode('ascii')
        original = base64.b64decode(original)
        return [original, ext]
