#!/usr/bin/python

import sys
import gzip
import pickle
if(len(sys.argv) < 3):
	print "./Snap2Metis.py input-file output-file [current version works only on unweighted graph.]"
	sys.exit(0)
if sys.argv[1][-2:] == "gz":
	inFile = gzip.open(sys.argv[1],"r");
else:
	inFile = open(sys.argv[1],"r");
outFile = open(sys.argv[2], "w")
#line = inFile.readline()
directed = False 
#if("Undirected" in line):
#	directed = False
#if(directed):
#	print "The graph is directed."
#else:
#	print "The graph is undirected."
dic = dict()
idMap = dict() #discrete 2 continuous; Or original 2 new. 
nodeNum = 4039
edgeNum = 88234
for line in inFile:
	if("#" in line):
		if("Nodes" in line):
			strSplit = line.strip().split()
			nodeNum = int(strSplit[2])
			edgeNum = int(strSplit[4])
			print nodeNum,edgeNum
		continue
	strSplit = [int(ele) for ele in line.strip().split()]
        if(strSplit[0] == strSplit[1]):
		continue
	if(strSplit[0] in dic):
		dic[strSplit[0]].append(strSplit[1])
	else:
		dic[strSplit[0]] = []
		dic[strSplit[0]].append(strSplit[1])
	if(directed == False):
		if(strSplit[1] in dic):
			dic[strSplit[1]].append(strSplit[0])
		else:
			dic[strSplit[1]] = []
			dic[strSplit[1]].append(strSplit[0])
count = 1 # new ids start from 1...
keySet = [ele for ele in dic]
for ele in keySet:
	idMap[ele] = count
	count += 1
print "Finish reading graph..."
print nodeNum, count-1

edgeCount = 0
for key in keySet:
  tmpSet = set(dic[key]);
  for ele in tmpSet:
		edgeCount += 1
edgeNum = edgeCount/2;

print >> outFile, str(count-1)+" "+str(edgeNum)
print str(max(ele for ele in dic))
truthEdge = 0
for key in keySet:
	outLine = ""
	tmpSet = set(dic[key])
	truthEdge += len(tmpSet)
	for ele in tmpSet:
		outLine += str(idMap[ele])+" "
	outFile.write(outLine.strip()+"\n")
print truthEdge, edgeCount, 2*edgeNum
if(edgeCount != 2*edgeNum):
	print "Wrong edge num: " + str(edgeNum) +" vs. "+str(edgeCount)+" (count)"
print "Output metis file contains edges: " + str(truthEdge/2)
outFile.close()
inFile.close();
objFile = open("map.obj", "wb")
pickle.dump(idMap, objFile)
objFile.close()


