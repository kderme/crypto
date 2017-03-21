from Crypto.Hash.RIPEMD import RIPEMD160Hash as ripemd160

BASE16_ALPHABET = '0123456789abcdef'
BASE16_BASE = len(BASE16_ALPHABET)
BASE16_LOOKUP = dict((c, i) for i, c in enumerate(BASE16_ALPHABET))

class EncodingError(Exception):
    pass

def to_long_Base16(s):
  # converts a string with BASE16 alphabet into a long number
    v = 0
    for c in s:
        v *= 16
        try:
          v += BASE16_LOOKUP[c]
        except Exception:
            raise EncodingError(c+" in "+s+" not found in BASE16 ALPHABET")
    return v

def to_hex(n):
	st=""
	while n>0:
		n,mod=divmod(n,16)
		st += BASE16_ALPHABET[mod]
	return st[::-1]

def from_long(v, prefix):
    l = bytearray()
    while v > 0:
       v, mod = divmod(v, 256)
       l.append(mod)
    l.extend([0] * prefix)
    l.reverse()
    return bytes(l)

def to_bytes(x):
	y=from_long(x,0)
	return (('\0' * 32) + y)[-32:]


def hash160():
	return ripemd160(hashlib.sha256(data).digest()).digest()	
