import chromadb

client = chromadb.Client()
role_docs = client.create_collection(name="role_documents")
role_docs.add(
    ids=["r1", "r2", "r3", "r4"],
    documents=[
        "Managers must review team goals every quarter.",
        "Engineers should follow the secure coding guidelines.",
        "HR team must verify employee records before onboarding.",
        "Managers are responsible for performance review discussions."
    ],
    metadatas=[
        {"role": "manager"},
        {"role": "engineer"},
        {"role": "hr"},
        {"role": "manager"}
    ]
)
results = role_docs.query(
    query_texts=["What am I supposed to review as a manager"],
    n_results=3,
    where={"role": "manager"}
)

print(results)
