#!/usr/bin/python
# given a message encrypted with Vigenere this code
# estimates the length of the key

import sys
import matplotlib.pyplot as plt
import numpy as np
#import plotly.plotly as py

Ieng = 0.065
Irand = 0.038

#finds index from frequencies of letters
def countI(freq):
  sum1=0.0
  for f in freq:
    sum1+=f*(f-1)
  total=sum(freq)
  return sum1/(1.0*total*(total-1))

#find mutual index from frequencies
def IMC(freq1,freq2):
  sum1=0.0
  for i in range(26):
    sum1+=freq1[i]*freq2[i]
  return sum1/(1.0*sum(freq1)*sum(freq2))

#shift r by j
def shift(r,j):
  newr=[]
  for c in r:
    newr.append(chr(((ord(c)-ord('A')+j)%26)+ord('A')))
  return newr

def test(row,freq,k,d):
  r0 = shift(row[0],d)
  freq0=count_freq(r0)
  imc=IMC(freq0,freq[k])
#  print str(d)+"->"+str(imc)
  return imc

def count_freq(r):
  freq=[0 for i in range(26)]
  for c in r:
    if c.isalpha():	#check if its a letter
      i = ord(c)-ord('A')
      freq[i]+=1
  return freq

def findI(r):
  freq=count_freq(r)
  return countI(freq)

#1->shifts of all rows relative to first row
#2->shift of first row
#ret->key
def find_key_from_shifts(rel_shifts,one):
  arr=map(lambda x: (-x+one)%26,rel_shifts)
  g=lambda x:chr(x%26+ord('A'))
  arr2=map(g,arr)
  print "Relative Shifts after manual changes:"
  print rel_shifts
  print "Absolute Shift of first row:"
  print one
  print "Absolute Shifts:"
  print arr
  print arr2
  return ''.join(arr2)

#main
if len(sys.argv)<2:
  print "Usage:python keylength"
  print "Use keylength=0 if you don`t know the key"
  exit()

#read input file
f=open('input1','r')
chars=f.read()
print
print "%%%%%%%%%%%%%%%%%%%%%%%%%%% TEXT  %%%%%%%%%%%%%%%%%%%%%%%%%%%%"
print chars
Itext=findI(chars)
print "Itext:"+str(Itext)

#take key_length from input
key_length=int(sys.argv[1])

print
print "%%%%%%%%%%%%%%%%%%%%%%%% CHECK KEY %%%%%%%%%%%%%%%%%%%%%%%%%%"
print "key length given:"+str(key_length)

r=(Ieng-Irand)/(Itext-Irand)
print "r="+str(r)

krange=[key_length]
if key_length==0:
  krange=[i for i in range(1,15)]
    
print krange
for k in krange:
  #divide into rows: row[key_length][..]
  row=[[] for i in range(k)]
  i=0
  for c in chars:
    if c.isalpha():	#check if its a letter
      row[i%k].append(c)
      i=i+1

  Is=[]
  for r in row:
    Is.append(findI(r))
  print "k= "+str(k)
  print "Index of each row"
  print Is

if key_length==0:
  exit()

print
print "%%%%%%%%%%%%%%%%%%%%%%%%%%% SHIFTS  %%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#count frequencies for every row: freq[key_length][26]
freq=[[]for i in range(key_length)]
for j in range(key_length):
  freq[j]=count_freq(row[j])

#find relative shifts between first and others row,
#by finding the value that maximizes the index
#of mutual coincidence
relative_shifts=[]
#print "row"+"  shift"+"  IMC"

for k in range(key_length):
  max=0.0
  dmax=-1
  for d in range(26):
    mm=test(row,freq,k,d)
    if mm>max:
      max=mm
      dmax=d
#  print " "+str(k)+"    "+str(dmax)+"     "+str(max)
  relative_shifts.append(dmax)

print "relative_shifts which maximize IMC:"
print relative_shifts
#change value of relative shifts manually
if key_length==6:
  #darray[2]=4
  #darray[3]=11 #18
  relative_shifts[4]=19 #15
  relative_shifts[5]=6 #15

#print relative_shifts

shifted_row=[[] for i in range(key_length)]
for k in range(key_length):
  shifted_row[k]=shift(row[k],-relative_shifts[k])
#print shifted_row

#make list of lists, a simple list again
srow1=[]
for i in range(len(chars)-1):
  j=i%key_length
  c=shifted_row[j][0]
  shifted_row[j].pop(0)
  srow1.append(c)


shift_first_row=26-11
srow1=shift(srow1,shift_first_row)
key=find_key_from_shifts(relative_shifts,shift_first_row)
print "key:"+key

print
print "%%%%%%%%%%%%%%%%%%%%%%% MESSAGE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%"
print ''.join(srow1)
print "I of found message:"+str(countI(count_freq(srow1)))
freq=count_freq(srow1)
#print freq

pos=np.arange(26)
width=1.0

alphabeta=map(chr, range(65,91))
ax=plt.axes()
ax.set_xticks(pos+(width/2))
ax.set_xticklabels(alphabeta)
plt.bar(pos,freq)
plt.show()

g=open("output"+str(key_length),'w')
for j in range(26):
  row2=shift(srow1,j)
  g.write(str(row2))
  g.write("\n")


