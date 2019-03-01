import hashlib
def AwareHash(x, n):
    md5 = hashlib.md5(str(hash(x)))
    md5.update(str(n))
    return md5.hexdigest()
