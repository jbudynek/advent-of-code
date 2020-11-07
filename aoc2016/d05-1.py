import hashlib
import sys

#key = "abcdef" #609043
#key = "pqrstuv" #1048970 
key = "wtnhxymk"

i = 1
k=0
o=''
while(True):

	test_me=key+str(i)
	md5_hex = str(hashlib.md5(test_me.encode('utf-8')).hexdigest())

	if (md5_hex.startswith("00000")):
		print(str(i) + " "+md5_hex)
		o = o + md5_hex[5:6]
		k = k + 1
		if k==8:
			print(o)
			sys.exit()
	i = i + 1