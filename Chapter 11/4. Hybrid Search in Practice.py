import chromadb

client = chromadb.Client()
collection = client.create_collection(name="helpdesk-hybrid")

collection.add(
    ids=["d1", "d2", "d3", "d4"],
    documents=[
        "Users may see error 502 during login when the authentication service is down",
        "Password reset steps for employees using the internal portal",
        "Error 404 occurs when the requested page does not exist",
        "Login failures caused by temporary server issues or gateway timeouts"
    ],
    metadatas=[
        {"topic": "login"},
        {"topic": "access"},
        {"topic": "error"},
        {"topic": "login"}
    ]
)

query = "error 502 during login"

# Step 1: check manually if keyword exists
keyword = "502"

# Step 2: semantic search
results = collection.query(
    query_texts=[query],
    n_results=3
)

# Step 3: prioritize documents containing the keyword
ranked = []
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    score = 0
    if keyword in doc:
        score += 1
    ranked.append((doc, score))

ranked = sorted(ranked, key=lambda x: x[1], reverse=True)
print(ranked)
