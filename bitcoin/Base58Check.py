#!/usr/bin/env python

from utilities import from_long
import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE58_BASE = len(BASE58_ALPHABET)
BASE58_LOOKUP = dict((c, i) for i, c in enumerate(BASE58_ALPHABET))

class EncodingError(Exception):
    pass

def long_to_base58(n):
	ls=[]
	while n>0:
		n, mod = divmod(n, 58)
		ls.append(BASE58_ALPHABET[mod])
	ls.reverse()
	return ''.join(ls)


def base58_to_long(s):
	# converts a string with BASE58 alphabet into a long number
    prefix = 0
    v = 0
    for c in s:
        v *= 58
        try:
	        v += BASE58_LOOKUP[c]
        except Exception:
            raise EncodingError(c+" in "+s+" not found in BASE58 ALPHABET")
        if v == 0:
            prefix += 1
    return v, prefix

def check_address(address,dbg=False):
	#	check if this is a valid bitcoin address
	try:
		v, prefix = base58_to_long(address)
		if dbg:
			print "number of address:"
			print v
			print "with prefix:"
			print prefix
		if prefix==0:
			raise EncodingError("bitcoin addresses must start with 1")
		data1=from_long(v, prefix)
	#	print data1
		data2, the_hash = data1[:-4], data1[-4:]
	#	print data2
		data3 =hashlib.sha256(hashlib.sha256(data2).digest()).digest()
	#	print data3
		data4 =data3[:4]
	#	print data4
		if data4==the_hash:
	#		print "ok: "+data1
			return True
		else:
			raise EncodingError("wrong checksum")
	except EncodingError as error:
		print "ADDRESS ERROR: "+ str(error)
		return False
	return False	

def get_address(which,dbg=False):
	while 1:
		if dbg:
			print "enter the %s address=> " % which+"",
		address = raw_input()
		is_valid = check_address(address,dbg)
		if is_valid:
			return address
		print("invalid address, please try again")

