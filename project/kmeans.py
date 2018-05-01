from sklearn.cluster import KMeans
import numpy as np
import csv
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import cdist
from sklearn import metrics
from scipy import cluster
import pylab as pl
#get Data from somewhere(currently the csv file)
filename="./recipeData.csv"
fields = csv.DictReader(open(filename))
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
numClusters=100
means = KMeans(n_clusters=numClusters, random_state=0).fit(dataContainer)
vector = means.labels_
#returnArry=[]
i=0
while i < numClusters:
	print ("Guess of the Type of Beer:" , vector[i], "Actual:", styleNum[i], "\n&& corisponding cluster center:" , means.cluster_centers_[i])
	print("\n")
	#time.sleep(5)	
	#returnArry.append(str("Guess of the Type of Beer:" + str(vector[i]) + "Actual:"+ str(styleNum[i])+ "\n&& corisponding cluster center:" + str(means.cluster_centers_[i])))
	i+=1
#return returnArray

#print(means.labels_)# return this and the centers to the flask service
#print(means.cluster_centers_)

minIBU = min(rawIBU[0:1000])
maxIBU =  max(rawIBU[0:1000])

ibuLin=np.linspace(float(minIBU),float(maxIBU), 1000)

minColor=min(rawColor[0:1000])
maxColor=max(rawColor[0:1000])


minABV=min(rawABV[0:1000])
maxABV=max(rawABV[0:1000])

minBT=min(rawBT[0:1000])
maxBT=max(rawBT[0:1000])


minFG=min(rawFG[0:1000])
maxFG=max(rawFG[0:1000])

colorLin=np.linspace(float(minColor), float(maxColor),1000)
abvLin=np.linspace(float(minABV), float(maxABV),1000)
btLin=np.linspace(float(minBT), float(maxBT),1000)
fgLin=np.linspace(float(minFG), float(maxFG),1000)

plt.scatter(ibuLin, colorLin, label="rawIBU x rawColor") 
plt.legend()
plt.show()

plt.scatter(ibuLin, abvLin, label="rawIBU x rawABV") 
plt.legend()
plt.show()

plt.scatter(ibuLin, btLin, label="rawIBU x rawBT") 
plt.legend()
plt.show()

plt.scatter(ibuLin, fgLin, label="rawIBU x rawFG")
plt.legend()
plt.show()


plt.scatter(abvLin, colorLin, label="rawABV x rawColor")
plt.legend()
plt.show()
plt.scatter(abvLin, btLin, label="rawABV x rawBT") 
plt.legend()
plt.show()
plt.scatter(abvLin, fgLin, label="rawABV x rawFG") 
plt.legend()
plt.show()


plt.scatter(colorLin, btLin, label="rawColor x rawBT")   
plt.legend()
plt.show()
plt.scatter(colorLin, fgLin, label="rawColor x rawFG") 
plt.legend()
plt.show()


plt.scatter(btLin, fgLin, label="rawBT x rawFG")
plt.legend() 
plt.show()

