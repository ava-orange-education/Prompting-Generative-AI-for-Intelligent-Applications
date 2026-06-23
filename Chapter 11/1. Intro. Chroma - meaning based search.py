import chromadb

client = chromadb.Client()
collection = client.create_collection(name="helpdesk-meaning")

collection.add(
    ids=["d1", "d2"],
    documents=[
        "Password reset steps for employees",
        "Instructions to install the internal software"
    ]
)
results = collection.query(
    query_texts=["I cannot access my account"],
    n_results=2
)
print(results)
