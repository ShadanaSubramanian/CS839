def filter(folder)
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
				data = getSample(featureClass,words)
				writer.writerows(data)
filter('train')