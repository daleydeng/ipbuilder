import hashlib
import rsa
import base64

def md5(data: str):
    return hashlib.md5(data.encode("utf-8")).hexdigest()

def md5_bytes(data: bytes):
    return hashlib.md5(data).hexdigest()

def sign_str(data: str, app_secret: str):
    return md5(data + app_secret)


def sign_dict(data: dict, app_secret: str):
    data_str = []
    keys = list(data.keys())
    keys.sort()
    for key in keys:
        data_str.append("{}={}".format(key, data[key]))
    data_str = "&".join(data_str)
    data_str = data_str + app_secret
    return md5(data_str)


def encrypt_login_password(password, hash, pubkey):
    return base64.b64encode(rsa.encrypt(
        (hash + password).encode('utf-8'),
        rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode()),
    ))


def av2bv(av: int):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    av = (av ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[av // 58 ** i % 58]
    return ''.join(r)


def bv2av(bv: str):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    r = 0
    for i in range(6):
        r += tr[bv[s[i]]] * 58 ** i
    return (r - add) ^ xor

class Retry:
    def __init__(self, max_retry, check_return):
        self.max_retry = max_retry
        self.check_return = check_return

    def run(self, func, *args, **kwargs):
        status = False
        for i in range(0, self.max_retry):
            try:
                return_value = func(*args, **kwargs)
            except Exception:
                return_value = not self.check_return

            if return_value == self.check_return:
                status = True
                break

        return status
