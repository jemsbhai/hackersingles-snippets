import requests
from google.cloud import storage

# Explicitly use service account credentials by specifying the private key
# file.
storage_client = storage.Client.from_service_account_json('pennapps-fit.json')

# Make an authenticated API request
buckets = list(storage_client.list_buckets())
print(buckets)

bucket = storage_client.get_bucket('pennappsfacebucket')

destination_blob_name = 'test.jpg'
source_file_name = 'test.jpg'

blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(source_file_name)
blob.make_public()

print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))


url = "https://vision.googleapis.com/v1/images:annotate"

querystring = {"key":"AIzaSyB6bJCXheYSTBvdJFKzkaanayCVuVhPUfk"}

payload = "{\r\n  \"requests\": [\r\n    {\r\n      \"image\": {\r\n        \"source\": {\r\n          \"imageUri\": \"https://storage.googleapis.com/pennappsfacebucket/test.jpg\"\r\n        }\r\n      },\r\n      \"features\": [\r\n        {\r\n          \"type\": \"LABEL_DETECTION\"\r\n        }\r\n      ]\r\n    }\r\n  ]\r\n}"
headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "90672481-4c25-4381-bf5d-d09d394a67b7"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)

blob.delete()

print('Blob {} deleted.'.format(destination_blob_name))






