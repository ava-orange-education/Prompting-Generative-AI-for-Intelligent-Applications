import chromadb

client = chromadb.Client()
collection = client.create_collection(name="helpdesk-metadata")

collection.add(
    ids=["d1", "d2"],
    documents=[
        "Password reset instructions",
        "Steps for installing the internal software"
    ],
    metadatas=[
        {"topic": "access", "source": "helpguide"},
        {"topic": "installation", "source": "internalnote"}
    ]
)

results_1 = collection.query(
    query_texts=["Laptop setup"],
    n_results=1,
    where={"source": "internalnote"}
)

results_2 = collection.query(
    query_texts=["How do I reset my credentials"],
    n_results=3,
    where={
        "$and": [
            {"topic": "access"},
            {
                "date": {
                "$in": ["2024-01-01", "2024-01-05", "2024-01-10"]
                } 
            }
        ]
    }
)
print("-----------------------results_1-----------------------")
print(results_1)
print("-----------------------results_2-----------------------")
print(results_2)

