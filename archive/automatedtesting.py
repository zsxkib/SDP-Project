#!/usr/bin/env python
# coding: utf-8

# In[1]:


## recycable and not recycable
## trash, plastic, paper, metal, glass, cardboard
##create two tests 1 for the training dataset and one for the test dataset


# In[ ]:


Classifier() .classify({'image_top': np.array})


# In[153]:


class Classifier:

    def classify(self,inputs):
        ## return function(inputs.get("image_top"))
        return "nonrecycable"
    def name(self):
        return "classifier a"


# In[17]:


classifier = Classifier()


# In[18]:


classifier.classify({"image_top":"hello"})


# In[164]:


import os
import numpy
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import numpy as np
from PIL import Image


# In[28]:


os.listdir('dataset-resized/recycable')


# In[40]:


path = 'dataset-resized'
for folder in os.listdir(path):
    for file in os.listdir(os.path.join(path,folder)):
        Image.open(file)


# In[127]:


def training_test(basewidth,hsize):
    predicted = []
    actual = []
    classifier = Classifier()
    for types in os.listdir(path):
        p = os.path.join(path,types)
        for folder in os.listdir(p):
            i = os.path.join(p,folder)
            for image in os.listdir(i):
                img = os.path.join(i,image)
                photo = Image.open(img)
                photo = photo.resize((basewidth,hsize), Image.ANTIALIAS)
                #print(numpy.asarray(photo).shape)
                #print(types)
                predicted_class = classifier.classify(np.asarray(photo).shape)
                predicted.append(dictionary[predicted_class])
                actual.append(dictionary[types])


    confusionmatrix = confusion_matrix(actual, predicted)
    return confusionmatrix



# In[176]:


def test(classifier, datasetdirectory, datasetname, basewidth,hsize, filename):
    dictionary = {}
    actual = []
    predicted = []
    integer =0
    ##this is to create a dictionary
    for types in os.listdir(datasetdirectory):
        if types not in dictionary:
            dictionary[types]=integer
            integer +=1
    ##this creates the classification
    for types in os.listdir(datasetdirectory):
        directory = os.path.join(datasetdirectory,types)
        for image in os.listdir(directory):
            actual.append(dictionary[types])
            photo = Image.open(os.path.join(directory, image))
            photo = photo.resize((basewidth,hsize), Image.ANTIALIAS)
            predicted_class = classifier.classify(np.asarray(photo).shape)
            predicted.append(dictionary[predicted_class])

    confusionmatrix = confusion_matrix(actual, predicted)
    accuracy = accuracy_score(actual, predicted)

    cr = classification_report(actual, predicted, target_names=list(dictionary.keys()))
    cm = np.array2string(confusion_matrix(actual, predicted))
    string = str(classifier.name()) + " on " + str(datasetname) + " dataset\n\n"
    f = open(filename, 'w')
    f.write(string)
    f.write('Classification Report\n\n{}\n\nConfusion Matrix\n\n{}\n'.format(cr, cm))
    f.close()

    return confusionmatrix



# In[177]:


test(Classifier(),'dataset-resized',"testing",5,5, "testingdataset")


# In[156]:





# In[ ]:





# In[ ]:





# In[ ]:
