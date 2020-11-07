import hashlib
import sys

#key = "abcdef" #609043
#key = "pqrstuv" #1048970 
key = "bgvyzdsv"

i = 1

while(True):

	test_me=key+str(i)
	md5_hex = str(hashlib.md5(test_me.encode('utf-8')).hexdigest())

	if (md5_hex.startswith("000000")):
		print(str(i) + " "+md5_hex)
		sys.exit()

	i = i + 1