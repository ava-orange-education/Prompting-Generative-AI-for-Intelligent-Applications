import chromadb

client = chromadb.Client()
support = client.create_collection(name="support_memory")
support.add(
    ids=["s1", "s2", "s3"],
    documents=[
        "Error 502 occurs when the server is temporarily unavailable.",
        "Error 401 appears when authentication fails.",
        "Version 3.2 improves startup performance and fixes several issues."
    ],
    metadatas=[
        {"component": "server", "version": "3.0"},
        {"component": "auth", "version": "3.1"},
        {"component": "upgrade", "version": "3.2"}
    ]
)

semantic_results = support.query(
    query_texts=["I keep seeing error 502 during login"],
    n_results=3,
    where={"component": "server"}
)

keyword = "502"

ranked = []
for doc in semantic_results["documents"][0]:
    score = 1 if keyword in doc else 0
    ranked.append((doc, score))

ranked = sorted(ranked, key=lambda x: x[1], reverse=True)
print(ranked)
