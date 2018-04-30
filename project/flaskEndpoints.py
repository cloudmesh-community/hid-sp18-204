import requests
from flask import Flask
import numpy as np
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.svm import SVC
from os import listdir
from flask import Flask, request
from sklearn.cluster import KMeans
import csv
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import cdist
from sklearn import metrics
from scipy import cluster
import json

from flask import jsonify


app = Flask(__name__)

def download_data(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)

#def get_data(filename, ratio):
 #   data = load_svmlight_file('data/'+filename)
  #  return data[0], data[1]


def data_partition(filename, ratio):
    file = open(filename,'r')
    training_file=filename+'_train_'+str(ratio)
    test_file=filename+'_test_'+ str(ratio)
    data = file.readlines()
    count = 0
    size = len(data)
    ftrain =open(training_file,'w')
    ftest =open(test_file,'w')
    for line in data:
	if(count==0):
	    ftrain.write(line)
	    ftest.write(line)
        elif(count< int(size*ratio)):
            ftrain.write(line)
        else:
            ftest.write(line)
        count = count + 1 


@app.route('/')
def index():
    return "Demo Project!"

@app.route('/api/download/data/output/<output>/')
def download(output):
    output_file =  'data/'+output
    url = 'https://www.dropbox.com/s/cqoklaf6n24s0t3/recipeData.csv?dl=1'
    download_data(url=url, filename=output_file)
    return "Data Downloaded"

@app.route('/api/data/partition/<filename>/ratio/<ratio>/')
def partition(filename, ratio):
    ratio = float(ratio)
    path='data/'+filename
    data_partition(path,ratio)
    return "Successfully Partitioned"

#@app.route('/api/get/data/test/partition/<filename>/ratio/<ratio>/')
#def gettestdata(filename, ratio):
#    Xtest, ytest = get_data(filename+'_test_'+ str(ratio), ratio)
#    testDat = zip(Xtrain, ytrain)
#    return testDat

#@app.route('/api/get/data/train/partition/<filename>/ratio/<ratio>/')
#def gettraindata(filename, ratio):
#    Xtrain, ytrain = get_data(filename+'_train_'+ str(ratio), ratio)
#    trainDat = zip(Xtrain, ytrain)
#    return trainDat

@app.route('/api/experiment/kmeans/clusters/<clusters>/partition/<filename>/')
def kmeans(clusters, filename):
	fields = csv.DictReader(open('data/'+filename))
	#get csv headers for col values
	headers = zip(fields.fieldnames[9], fields.fieldnames[10], fields.fieldnames[8], fields.fieldnames[11], fields.fieldnames[6]) #9 = IBU && 10 = Color && 8=ABV && 11=boil time && 6=FG(Wort fermentation)
	styleNum=[]
	dataContainer=[]
	rawColor=[]
	rawIBU=[]
	rawABV=[]
	rawBT=[]
	rawFG=[]
	newDataContainer=[]
	#parse csv for values
	for row in fields:
		if(row['IBU'] != '.' or int(row['IBU']) < 5):
			if(row['Color']!='.'):
				if(row['ABV']!='.'):
					if(row['BoilTime']!='.'):
						if(row['FG']!='.'):
							abv = row['ABV']
							#print("ABV=" + abv)
							iub = row['IBU']
							#print("IUB=" + iub)
							color = row['Color']
							#print("Color=" + color)
							bt = row['BoilTime']
							#print("boiltime=" + bt)
							fg = row['FG']
							#print("fg=" + fg)

							data=[iub, color, abv, bt, fg]
							
							dataContainer.append(data)
							#print("Appending this:")
							#time.sleep(5)
							newData=[iub, color]
							newDataContainer.append(newData)

							styleNum.append(row['StyleID'])
							rawIBU.append(row['IBU'])
							rawColor.append(row['Color'])
							rawABV.append(row['ABV'])
							rawBT.append(row['BoilTime'])
							rawFG.append(row['FG'])

	#print dataContainer
	#numClusters=100
	means = KMeans(n_clusters=int(clusters), random_state=0).fit(dataContainer)
	vector = means.labels_
	i=0
	returnArr=[]	
	while i < int(clusters):
		entry={}	
		entry['Guess'] = str(vector[i])
		entry['Actual'] = str(styleNum[i])
		entry['CCenter'] = str(means.cluster_centers_[i])
		returnArr.append(entry)
		i+=1
	
	

	return json.dumps(returnArr)




if __name__ == '__main__':
    app.run(debug=True)
