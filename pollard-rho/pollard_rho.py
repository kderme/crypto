#!/usr/bin/python

import sys
import random

def gcd(a, b):
	while b:
		a, b = b, a%b
	return a

def read_file(name):
	array=[]
	with open(name) as f:
		for line in f:
			for x in line.split():
				array.append(int(x))
	return array
	
def two_primes(name):
	array=read_file(name)
	i=random.randint(0,len(array)-1)
	cond=True
	while	cond:
		j=random.randint(0,len(array)-1)
		cond= j==i
	return (array[i],array[j])


def search(n,x):
	ls=[]
	i=1
	y=x
	k=2
	while True:
		i=i+1
		x=(x*x-1) % n
		if x in ls:
			return(0,i)
		ls.append(x)
		d=gcd(y-x,n)
		if d!=1 and d!=n:
			return (d,i)
		if i==k:
			y=x
			k=2*k

def search1(n):
	x=2
	summ=0
	rhos=1
	while True:
		(d,i)=search(n,x)
		summ+=i
		if d!=0:
			print str(n)+"="+str(d)+"*"+str(n/d)
			print "Number of steps: "+str(summ)
			print "Number of rhos: "+str(rhos)
			return (summ,rhos)
		rhos+=1
		x=random.randint(3,n-1)
	

def search_all():
	arr=read_file('primes.txt')
	for i in range(len(arr)):
		for j in range(i):
			n=arr[i]*arr[j]
			search1(n)
#main
n=0
p=q=0
if len(sys.argv)>2 or str(sys.argv[1])=="-help":
	print "Usage:python pollard_rho.py -help      (for this message)"
	print "Usage:python pollard_rho.py            (for a random number)"
	print "Usage:python pollard_rho.py <number>		(for <number>"
	print "Usage:python pollard_rho.py all        (for all products in file primes.txt"
	print "CAUTION: passing all will flood stdout"
	exit()
elif len(sys.argv)==1:
	(p,q)=two_primes('primes.txt')
	n=p*q
	search1(n)
else:
	if sys.argv[1]=='all':
		search_all()
	else:
		n=int(sys.argv[1])
		search1(n)


