import pymongo
import requests, os
from generate_embedding import generate_embedding
from dotenv import load_dotenv

load_dotenv()

MongoDbUser = os.getenv('MongoDbUser')
MongoDbPass = os.getenv('MongoDbPass')
HF_Token = os.getenv('HF_Token')


client = pymongo.MongoClient("mongodb+srv://"+MongoDbUser+":"+MongoDbPass+"@cluster0.wrhkuhw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") # <Your mongoDB URL>
db = client.sample_mflix
collection = db.movies

embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

query = "imaginary characters from outer space at war"

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100, # Optimiztion Parameter
    "limit": 4, # Limit result to top 4 matches
    "index": "PlotSemanticSearch", # Index is used for search
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')