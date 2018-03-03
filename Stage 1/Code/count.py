import os
import sys
files = os.listdir(sys.argv[1])
print "No of file:"+str(len(files))
count = 0
for file in files:
	if os.path.isfile(sys.argv[1]+os.sep+file) and ".py" not in file:
		with open(sys.argv[1]+os.sep+file,'r') as f:
		    contents = f.read()
		    c = contents.count("<person>")
		    c1 = contents.count("</person>")
		    if c != c1:
		    	print file
		    count+=c
print "No of mentions:"+str(count)
