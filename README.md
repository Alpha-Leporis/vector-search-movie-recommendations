
# Semantic search for movie recommendations

We'll be using a sample movie data set containing over 20,000 documents in MongoDB Atlas. And we'll be using the [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model from HuggingFace for generating the vector embedding during the index time as well as query time.

All the data including our embeddings will be stored in a MongoDB instance.

This project uses the MongoDB Atlas for storing embeddings and hugging face API to get the embeddings.

## Setup Instructions
### 1. Clone the Repository
```bash
$ git clone https://github.com/Alpha-Leporis/vector-search-movie-recommendations.git
$ cd vector-search-movie-recommendations
```

### 2. Install Required Packages
```bash
$ pip install -r requirements.txt
```

### 3. Create a MongoDB Atlas account.
  * Create a deployement with free option.
  * Set up the authentication. And create the user (ID, Pass).

### 4. Load dataset in MongoDB Cluster0.
  * click load sample_data, It will load sample_data to clusterzero.
  * There are quite a few different sample data databases And we're just going to use movies, which is called sample_mflix.

### 5. Create MongoDB connection in local system.
  * Go to `Cluster0` and connect Database using MongoDB's drivers(e.g. python, node.js).
  * copy and paste connection string in code and replace username and password accordingly.

### 6. Load [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) hugging face model using API in local system.
  * login to hugging face go to settings, access tokens.
  * create a new token to generate embeddings.
  * Replace the token in code.

### 7. Run `generate_embedding.py` to generate embedding.
  * In this code, we are storing the vector embedding in the original collection.

### 8. Next step is to create a vector search index,
  * Goto `Cluster0`, Atlas search. create a search index use JSON editor and paste the below code.
  * Select the database "sample_mflix" and collection "movies" on the left, paste index name and below code on the right. 
  * Click next and then click create search index.

> Index Name: PlotSemanticSearch

```
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "plot_embedding_hf": {
        "dimensions": 384,
        "similarity": "dotProduct",
        "type": "knnVector"
      }
    }
  }
}
```

### 9. Run `test_embedding.py` to test the query string.