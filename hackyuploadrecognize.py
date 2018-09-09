from clarifai.rest import ClarifaiApp

from math import sqrt

from numpy import linalg

from numpy import array

import requests
from google.cloud import storage

 

# Initalize Clarifai and get the Face Embedding model

app = ClarifaiApp(api_key='74abff9bee1541ddbf19dd104e10d602')

model = app.models.get("d02b4508df58432fbb84e800597b8959")

 

# Dataset

storage_client = storage.Client.from_service_account_json('pennapps-fit.json')

# Make an authenticated API request
buckets = list(storage_client.list_buckets())
##print(buckets)

bucket = storage_client.get_bucket('pennappsfacebucket')


destination_blob_name = 'test2.jpg'
source_file_name = 'test2.jpg'

blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(source_file_name)
blob.make_public()


testPhoto = "https://storage.googleapis.com/pennappsfacebucket/test2.jpg"

peterPhoto = "https://storage.googleapis.com/pennappsfacebucket/peter.jpg"

chrisPhoto = "https://storage.googleapis.com/pennappsfacebucket/chris.jpg"

 

# Function to get embedding from image

def getEmbedding(image_url):

# Call the Face Embedding Model

    jsonTags = model.predict_by_url(url=image_url)

 

# Storage for all the vectors in a given photo

    faceEmbed = []

 

# Iterate through every person and store each face embedding in an array

    for faces in jsonTags['outputs'][0]['data']['regions']:

        for face in faces['data']['embeddings']:

            embeddingVector = face['vector']

            faceEmbed.append(embeddingVector)

    return faceEmbed[0]

 

# Get embeddings and put them in an array format that Numpy can use

testEmbedding = array(getEmbedding(testPhoto))

peterEmbedding = array(getEmbedding(peterPhoto))

chrisEmbedding = array(getEmbedding(chrisPhoto))

 

# Get Distances useing Numpy

peterDistance = linalg.norm(testEmbedding-peterEmbedding)


print ("peter Distance: "+str(peterDistance))

 

chrisDistance = linalg.norm(testEmbedding-chrisEmbedding)

print ("chris Distance: "+str(chrisDistance))

 
flag = 0;
# Print results

print ("")

print ("**************** Results are In: ******************")

if peterDistance < chrisDistance:

    print ("test looks more similar to peter")
    if peterDistance < 0.6:
        print ("#peter$")
    else:
        print ("#none$")

elif peterDistance > chrisDistance:

    print ("test looks more similar to chris")
    
    if chrisDistance < 0.6:
        print ("#chris$")
    else:
        print ("#none$")

else:

    print ("test looks equally similar to both his peter and chris")


print ("")

blob.delete()
