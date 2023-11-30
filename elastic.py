import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

def elastic_connect():
    load_dotenv()
    
    HOST_ADDR = os.getenv("HOST_ADDR")
    CA_CERTS = os.getenv("CA_CERTS")
    ELASTIC_USER = os.getenv("ELASTIC_USER")
    ELASTIC_PASS = os.getenv("ELASTIC_PASSWORD")
       
    
    es = Elasticsearch(
    "https://localhost:9200/",
    ca_certs="C:\Elastic\elasticsearch-8.11.1\config\certs\http_ca.crt",
    basic_auth=("elastic", "XY8Pho=MUT4WceKkxV_R")
    )
    
    return es