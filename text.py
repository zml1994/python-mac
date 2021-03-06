import random
import time
import hashlib
import requests
import json
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)  # \0代表空格
    return text.encode('utf-8')


# 加密函数
def encrypt(text, key):
    key = 'appsecret'.encode('utf-8')
    mode = AES.MODE_CBC
    key = key[0:16]
    iv = b'key'  # 偏移量  密钥的前16位
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = '9999999999999999'.encode('utf-8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    idCardNumber = ''
    appsecret = ''
    info = idCardNumber
    e = encrypt(info, appsecret)  # 加密
    d = decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)