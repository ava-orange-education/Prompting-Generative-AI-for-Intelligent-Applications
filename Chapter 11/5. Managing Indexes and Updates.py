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

collection.add(
    ids=["d3"],
    documents=["Steps to unlock a suspended account"],
    metadatas=[{"topic": "access"}]
)

collection.update(
    ids=["d1"],
    documents=["Updated password reset steps for employees"]
)

collection.delete(ids=["d2"])