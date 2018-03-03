import os
import sys
import csv
'''
	Class to hold the helper methods to extract feature values
	The methods in this class are called multiple times to get different features
'''
class feature:
	'''
		returns the number of words in the given list
	'''
	def getLength(self,input):
		return len(input)
	'''
		returns whether all the words in the given list starts with caps
	'''
	def allCaps(self,input):
		for word in input:
			if len(word)>0:
				if not word[0].isupper():
					return 0;
		return 1
	'''
		returns whether the given words words are equla by doing case insensitive check
	'''
	def wordEquals(self,word1,word2):
		if(len(word1)>0 and len(word2)>0):
			if word1.lower() == word2.lower():
				return 1
		return 0
	'''
		returns whether the given words starts with capital letter
	'''
	def wordCaps(self,word):
		if len(word)<=0:
			return 0
		if word[0].isupper():
			return 1
		return 0
	'''
		returns whether the source string contains the target string
	'''
	def containWord(self,source,target):
		if target in source:
			return 1
		return 0
	'''
		returns true if the given input contains any match releated terms
	'''
	def isMatchHelper(self,input):
		matchHelpers = ['ODI','Odis','T20I','ICC','Test','Tests','Internationals','International','Twenty20','World','toss','Time','Credit','wicket','stumps','Scores','score','Presentations','Powerplay','Injuries','Cricket']
		for p in matchHelpers:
			if p.lower() in [word.lower() for word in input]:
				return 1
		return 0
	'''
		returns true if the given input contains cricket playing country names in the input
	'''
	def isCountry(self,input):
		teams = ['India','SA','South','Africans','New','Lanka','Zealand','NewZealand','Australia','Sri','SriLanka','Africa','SouthAfrica','Nation']
		for p in teams:
			if p.lower() in [word.lower() for word in input]:
				return 1
		return 0
	'''
		returns true if the given input contains Venue related names
	'''
	def isVenue(self,input):
		venue = ['Centurion','Durban','Cape','Stadium']
		for p in venue:
			if p.lower() in [word.lower() for word in input]:
				return 1
		return 0
	'''
		returns true if the given related string contains player related pronoun
	'''
	def isPlayerPronoun(self,input):
		playerPronoun = ['Indian','captain','skipper','players','player','batsman','bowlers','Champions','Australian','Srilankan','SouthAfrican','Debutant','Debutants']
		for p in playerPronoun:
			if p.lower() in [word.lower() for word in input]:
				return 1 
		return 0
	'''
		returns True if the given input contains any common words in English related to Cricket
	'''
	def iscommonWords(self,input):
		commonWords = ['a','c','I','they','among','There','High','Not','Three','One','Out','Day','both','full','support','in','back','after','bring','It','this','one',"It's",'We','on','at','He','The','That','With','Who','Once','From','For','been','When','good','if','so','but','his','has','had','off','Amount','And','Have','if','per','two','As','Goodbye',' ','','Asked','Low','Must','while','Big','Co','bash','off','but','lbw','Co','Went','long','asked','However','Drama','Remember']
		for p in commonWords:
			if p.lower() in [word.lower() for word in input]:
				return 1
		return 0
'''
	helper method to get the samples from the given file
'''
def getSample(featureClass,words,doc):
	#UNI,BI,TRI,.. GRAMS
	grams = [1,2,3]
	csvData = []
	numWords = len(words)
	for N in grams:
	    for index in range(numWords-N+1):
	    	inputList = words[index:index+N]
    		row = {}
    		inputList[N-1] = inputList[N-1].replace('.','')
    		inputList[N-1] = inputList[N-1].replace('"','')
    		inputList[0] = inputList[0].replace('.','')
    		inputList[0] = inputList[0].replace('"','')

    		'''
    			check whether the current sample is a person
    		'''
    		if inputList[0].startswith('<person>') and (inputList[N-1].endswith('</person>') or inputList[N-1].endswith('<\person>')):
    			row['person'] = 1
    		else:
    			row['person'] = 0
    		'''
    			clean the unwanted strings in the input
    		'''
    		for i in range(len(inputList)):
    			inputList[i]= inputList[i].replace('<person>','')
    			inputList[i]= inputList[i].replace('</person>','')
    			inputList[i]= inputList[i].replace('<\person>','')
    		inputString = " ".join(inputList)
    		nextWord = ''
    		prevWord = ''
    		if index > 0:
    			prevWord = words[index-1]
    			prevWord = prevWord.replace('<person>','')
    			prevWord = prevWord.replace('</person>','')
    		if (index+N) < numWords:
    			nextWord = words[index+N]
    			nextWord = nextWord.replace('<person>','')
    			nextWord = nextWord.replace('</person>','')

    		'''
    			generate the features using the helper methods in the feature class
    		'''
    		row['input'] = inputString
    		row['doc'] = doc
    		row['length'] =  N
    		row['all_start_with_caps'] =  featureClass.allCaps(inputList)
    		row['next_word_is'] = featureClass.wordEquals(nextWord,'is')
    		row['next_word_are'] = featureClass.wordEquals(nextWord,'are')
    		row['contain_comma'] = featureClass.containWord(inputString,',')
    		row['contain_quote'] = featureClass.containWord(inputString,"'")
    		row['contain_exclaim'] = featureClass.containWord(inputString,'!')
    		row['contain_colon'] = featureClass.containWord(inputString,':')
    		row['contain_hifen'] = featureClass.containWord(inputString,'-')
    		row['contain_pullstop'] = featureClass.containWord(inputString,'.')
    		row['isCountry']= featureClass.isCountry(inputList)
    		row['isMatchHelper']= featureClass.isMatchHelper(inputList)
    		row['isVenue']= featureClass.isVenue(inputList)
    		row['isPlayerPronoun']= featureClass.isPlayerPronoun(inputList)
    		row['iscommonWords']= featureClass.iscommonWords(inputList)
    		row['next_said'] = featureClass.wordEquals(nextWord,'said')
    		row['prev_said'] = featureClass.wordEquals(prevWord,'said')
    		row['next_to'] = featureClass.wordEquals(nextWord,'to')
    		row['prev_to'] = featureClass.wordEquals(prevWord,'to')
    		row['next_word_caps'] = featureClass.wordCaps(nextWord)
    		row['prev_word_caps'] = featureClass.wordCaps(prevWord)
    		row['next_batsman'] =  featureClass.wordEquals(nextWord,'batsman')
    		row['prev_batsman'] =  featureClass.wordEquals(prevWord,'batsman')
    		row['next_skipper'] =  featureClass.wordEquals(nextWord,'skipper')
    		row['prev_skipper'] =  featureClass.wordEquals(prevWord,'skipper')
    		row['next_captain'] =  featureClass.wordEquals(nextWord,'captain')
    		row['prev_captain'] =  featureClass.wordEquals(prevWord,'captain')
    		row['next_bowler'] =  featureClass.wordEquals(nextWord,'bowler')
    		row['prev_bowler'] =  featureClass.wordEquals(prevWord,'bowler')
    		row['prev_and'] =  featureClass.wordEquals(prevWord,'and')
    		row['next_and'] =  featureClass.wordEquals(nextWord,'and')
    		row['next_c'] =  featureClass.wordEquals(nextWord,'c')
    		row['prev_c'] =  featureClass.wordEquals(prevWord,'c')
    		row['next_b'] =  featureClass.wordEquals(nextWord,'b')
    		row['prev_b'] =  featureClass.wordEquals(prevWord,'b')
    		csvData.append(row)
	return csvData

'''
	iterates over the files in the given folder, generates and adds the feature vector to the output file
'''
def main(writer,folder):
	#folder = "train"
	files = os.listdir(folder)
	featureClass = feature()
	for file in files:
		if os.path.isfile(folder+os.sep+file) and not file.startswith('.'):
			words = []
			with open(folder+os.sep+file,'r') as f:
				for line in f:
					for word in line.split():
						words.append(word)
			#print words
			#return
			data = getSample(featureClass,words,file)
			writer.writerows(data)
'''
	creates the csv file for the training data with the features
'''
folder = 'train'
with open('trainSet.csv', 'w') as csvfile:
    fieldnames = ['input','doc','length', 'next_word_is','next_word_are','contain_comma','contain_quote','contain_exclaim','contain_colon','contain_hifen','contain_pullstop','all_start_with_caps','next_said', 'prev_said','next_to','prev_to','next_word_caps','prev_word_caps',
	    		'isCountry','isMatchHelper','isVenue','isPlayerPronoun','iscommonWords','next_batsman','prev_batsman','next_bowler','prev_bowler','next_captain','prev_captain','next_skipper','prev_skipper','prev_and','next_and','next_c','prev_c','next_b','prev_b','person']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
    writer.writeheader()
    main(writer,folder)
'''
 	creates the csv file for the testing data with the features
'''
folder = 'test'
with open('testSet.csv', 'w') as csvfile:
    fieldnames = ['input','doc','length', 'next_word_is','next_word_are','contain_comma','contain_quote','contain_exclaim','contain_colon','contain_hifen','contain_pullstop','all_start_with_caps','next_said', 'prev_said','next_to','prev_to','next_word_caps','prev_word_caps',
	    		'isCountry','isMatchHelper','isVenue','isPlayerPronoun','iscommonWords','next_batsman','prev_batsman','next_bowler','prev_bowler','next_captain','prev_captain','next_skipper','prev_skipper','prev_and','next_and','next_c','prev_c','next_b','prev_b','person']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
    writer.writeheader()
    main(writer,folder)
 
print("writing complete")