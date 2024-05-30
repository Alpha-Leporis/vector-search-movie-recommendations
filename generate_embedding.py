import pymongo
import requests, os
from dotenv import load_dotenv

load_dotenv()

'''
So let's get connected with sample_mflix database In our local environment.
'''

MongoDbUser = os.getenv('MongoDbUser')
MongoDbPass = os.getenv('MongoDbPass')
HF_Token = os.getenv('HF_Token')


client = pymongo.MongoClient("mongodb+srv://"+MongoDbUser+":"+MongoDbPass+"@cluster0.wrhkuhw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") # <Your mongoDB URL>
db = client.sample_mflix
collection = db.movies


embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:

  response = requests.post(
    embedding_url,
    headers={"Authorization": f"Bearer {HF_Token}"}, # {HF_Token} --> #"<Your_HuggingFace_Token>"
    json={"inputs": text})

  if response.status_code != 200:
    raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

  return response.json()

# print(generate_embedding("GenerativeAI"))

for doc in collection.find({'plot':{"$exists": True}}).limit(50):
  doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
  collection.replace_one({'_id': doc['_id']}, doc)