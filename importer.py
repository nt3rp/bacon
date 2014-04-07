import os
import json
from py2neo import neo4j

DATABASE_URI = 'http://localhost:7474/db/data/'
DIRECTORY = 'films'

db = neo4j.GraphDatabaseService(DATABASE_URI)

# Iterate over all files in a folder
for filename in os.listdir(DIRECTORY):
    contents = None

    full_path = os.path.join(DIRECTORY, filename)
    print full_path

    with open(full_path) as f:
        contents = json.loads(f.read())

    if not contents:
        continue

    # For each file, create necessary nodes