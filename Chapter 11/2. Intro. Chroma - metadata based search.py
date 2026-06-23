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
results = collection.query(
    query_texts=["I cannot log in"],
    n_results=2,
    where={"topic": "access"}
)

print(results)