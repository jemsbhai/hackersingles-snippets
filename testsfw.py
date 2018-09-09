from clarifai.rest import Image as ClImage
from clarifai.rest import ClarifaiApp
import json

app = ClarifaiApp(api_key='74abff9bee1541ddbf19dd104e10d602')
model = app.models.get('nsfw-v1.0')
image = ClImage(url='https://samples.clarifai.com/nsfw.jpg')
response = model.predict([image])

##print (response)

print ("analysing...")

##jsonout = json.loads(response)

sfw = response['outputs'][0]['data']['concepts'][0]['value']
nsfw = response['outputs'][0]['data']['concepts'][1]['value']
safescore = sfw - nsfw

print (safescore)
