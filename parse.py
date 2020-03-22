import re
from datetime import datetime
import sys

def timeSpliter(TimeString):
	TimeStringSplit = TimeString.split("-->")
	start = TimeStringSplit[0].strip()[0:12]
	end = TimeStringSplit[1].strip()[0:12]
	startT = datetime.strptime(start, '%H:%M:%S.%f')
	endT = datetime.strptime(end, '%H:%M:%S.%f')
	return startT,endT

def fileParse(filename):
	fEn = open(filename)

	currentLineNo = 1
	timeLine = False
	scriptLine = False
	FinalScript = {}

	timeLineStr = ""

	for line in fEn.readlines()[1:]:                            
	    line = line.strip() 
	    if line[0:4] != "NOTE":
	    	strCurrentLineNo = str(currentLineNo)
	    	
	    	if timeLine == True:
	    		timeLineStr = line[0:29]
	    		#timeLineStrSplit = timeLineStr.split("-->")
	    		#start = timeLineStrSplit[0].strip()[0:8]
	    		#end = timeLineStrSplit[1].strip()[0:8]
	    		#timeLineStr = start + "," + end
	    		#print("%s" % timeLineStr)
	    		timeLine = False
	    		scriptLine = True
	    		continue
	    	elif scriptLine == True:
	    		if line == "":
	    			currentLineNo += 1
	    			scriptLine = False
	    			continue
	    		scriptLineText = re.sub('<[^<]+?>', '', line)
	    		if FinalScript.get(timeLineStr) == None :
	    			FinalScript[timeLineStr] = scriptLineText.replace('&lrm;','').replace('&amp;','&')
	    		else:
	    			FinalScript[timeLineStr] += " " + scriptLineText.replace('&lrm;','').replace('&amp;','&')
	    		
	    		#print("%s" % FinalScript[timeLineStr])
	    		#scriptLine = False
	    		
	    		continue
	    	if line[0:len(strCurrentLineNo)] == strCurrentLineNo and len(line) == len(strCurrentLineNo) :
	    		timeLine = True
	    		#print("%s" % line)
	    		continue

	fEn.close()
	return FinalScript

'''
enFileName = "./subtitle/婚外情事.S04E05.WEBRip.Netflix.en[cc].vtt"
chtFileName = "./subtitle/婚外情事.S04E05.WEBRip.Netflix.zh-Hant.vtt"


enFileName = "./subtitle/婚外情事.S04E06.WEBRip.Netflix.en[cc].vtt"
chtFileName = "./subtitle/婚外情事.S04E06.WEBRip.Netflix.zh-Hant.vtt"


enFileName = "./subtitle/圖卡和柏蒂.S01E01.WEBRip.Netflix.en[cc].vtt"
chtFileName = "./subtitle/圖卡和柏蒂.S01E01.WEBRip.Netflix.zh-Hant.vtt"

'''


# python parse.py "./subtitle/獵魔士.S01E01.WEBRip.Netflix.en[cc].vtt" "./subtitle/獵魔士.S01E01.WEBRip.Netflix.zh-Hant.vtt"
# python parse.py "./subtitle/蓋酷家庭.S12E12.WEBRip.Netflix.en[cc].vtt" "./subtitle/蓋酷家庭.S12E12.WEBRip.Netflix.zh-Hant.vtt"
enFileName = sys.argv[1]
chtFileName = sys.argv[2]

#enFileName = "./subtitle/獵魔士.S01E01.WEBRip.Netflix.en[cc].vtt"
#chtFileName = "./subtitle/獵魔士.S01E01.WEBRip.Netflix.zh-Hant.vtt"


enFinalScript = fileParse(enFileName)
chtFinalScript = fileParse(chtFileName)

#FinalScript = enFinalScript.copy()
#FinalScript.update(chtFinalScript)


FinalScript = {}
lastIdx = 0

for key in sorted(enFinalScript):
	startT,endT = timeSpliter(key)
	#find cht script
	chtGroupScript = ""
	for i in range(lastIdx,len(chtFinalScript)):
		chtkey = sorted(chtFinalScript)[i]
		chstartT,chendT = timeSpliter(chtkey)
		if (startT <= chendT) and (chstartT <= endT):
			chtGroupScript +=  chtFinalScript[chtkey]
			lastIdx = i + 1 
		if (chstartT > endT):
			break
			#print("en: " + enFinalScript[key] + ",cht: " + chtFinalScript[chtkey])
	FinalScript[key] = enFinalScript[key] 
	if chtGroupScript != "":
		FinalScript[key] += " [" + chtGroupScript + "]"

FinalScriptOutput = ""
for key in sorted(FinalScript):
	print(key + " " + FinalScript[key])
	FinalScriptOutput += FinalScript[key] + "\r\n"

with open('script.txt','w') as data:
    data.write(FinalScriptOutput) 

'''

for key in chtFinalScript:
	if FinalScript.get(key) == None :
		FinalScript[key] = chtFinalScript[key]
	else:
		#FinalScript[key] += " " + chtFinalScript[key]
		
		newkey = key[0:26] + (str(int(key[26:29]) + 1)).zfill(3)
		FinalScript[newkey] = chtFinalScript[key]

FinalScriptSort = {}
FinalScriptOutput = ""

for key in sorted(FinalScript):
#	timeLineStr = key.split("-->")[1].strip()
#	FinalScriptSort[timeLineStr] = FinalScript[key]
	FinalScriptOutput += FinalScript[key] + "\r\n"
	#print(key + " " + FinalScript[key])
	#print(FinalScript[key])

#SScript = sorted(FinalScript)

#for i in range(0,len(SScript)):
#	print(FinalScript[SScript[i]])

with open('script.txt','w') as data:
    data.write(FinalScriptOutput) 
'''

