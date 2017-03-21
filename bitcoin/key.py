#!/usr/bin/env python

import ecdsa
import random
import os 
import time
import re

from ecdsa.util import string_to_number, number_to_string
from utilities import to_long_Base16, to_hex, from_long, to_bytes
import Base58Check
import hashlib

P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
#N is the order of Generator G, or the order of the group
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)
A = 0
B = 7

def random_key():
    entropy = os.urandom(32) \
        + str(random.randrange(2**256)) \
        + str(int(time.time() * 1000000))
    return hashlib.sha256(entropy).hexdigest()


def hash160(b):
	intermed = hashlib.sha256(b).digest()
	digest = ''
	try:
		digest = hashlib.new('ripemd160', intermed).digest()
	except:
		digest = RIPEMD160(intermed).digest()
	return digest

def from_bytes_to_long(bins):
  prefix = 0
  y = 0
  for b in bins:
    y *= 256
    y += ord(b)
    if y == 0:
       prefix += 1
  return y, prefix

def to_b58check(b):
	leadingzbytes = len(re.match('^\x00*', b).group(0))
	x=hashlib.sha256(hashlib.sha256(b).digest()).digest()
	checksum = (x)[:4]
	return '1' * leadingzbytes + changebase(b+checksum, 256, 58)


curve=ecdsa.ellipticcurve.CurveFp(P,A,B)
Generator = ecdsa.ellipticcurve.Point(curve, Gx, Gy, N)

#New Private Key
while 1:
  priv_key= random_key()
# example 3aba4162c7251c891207b747840551a71939b0de081f85c4e44cf7c13e41daa6
  print
  print "PRIVATE KEY"
  print "hex: "+priv_key
  long_priv_key=to_long_Base16(priv_key)
  print "dec: "+str(long_priv_key)
  isok = 0<long_priv_key<N
  if isok:
      break
  print "Invalid Private Key-it should be smaller than:"
  print N

#Find public key 
public_key=long_priv_key*Generator
(pubkey_x,pubkey_y)=(public_key.x(),public_key.y())
if pubkey_y % 2==0:
  prefix='02'
else:
  prefix='03'
compressed_pub_key=prefix+to_hex(pubkey_x)
uncompr_pub_key= '04' + to_hex(pubkey_x)+ to_hex(pubkey_y)
print
print "PUBLIC KEY"
print "coordinates: ",
print "("+str(pubkey_x)+","
print "               "+str(pubkey_y)+")"
print "compresses hex:",
print compressed_pub_key
print "uncompressed hex:",
print uncompr_pub_key
print

#Find Address
pair=(pubkey_x,pubkey_y)
bin_x=to_bytes(pubkey_x)
bin_y=to_bytes(pubkey_y)

bin={}
bin_uncompressed='\4'+bin_x+bin_y
bin_compressed=to_bytes(to_long_Base16(compressed_pub_key))

def find_addr (bin_key):
	hashed160=hash160(bin_key)
	with_prefix='\0'+hashed160
	teal =hashlib.sha256(hashlib.sha256(with_prefix).digest()).digest()[:4]
	ready=with_prefix+teal
	y, prefix = from_bytes_to_long(ready)
	s=Base58Check.long_to_base58(y)
	return '1'+s

address=find_addr(bin_uncompressed)
address_compressed=find_addr(bin_compressed)

print 'ADDRESS'
print 'uncompressed b58: '+address
print 'compressed b58:   '+address_compressed
if not Base58Check.check_address(address,False):
	print 'Invalid address'
if not Base58Check.check_address(address_compressed,False):
	print 'Invalid address'
exit()
