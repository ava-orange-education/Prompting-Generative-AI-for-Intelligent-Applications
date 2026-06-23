import chromadb
client = chromadb.Client()

policies = client.create_collection(name="company_policies")

policies.add(
    ids=["p1", "p2", "p3"],
    documents=[
        "Attendance must be regularized within the same month of absence.",
        "Travel reimbursements must be submitted within fifteen days of journey.",
        "Work from home requires prior approval unless covered by emergency rules."
    ],
    metadatas=[
        {"category": "attendance"},
        {"category": "finance"},
        {"category": "remote_work"}
    ]
)

query = "How long do I have to submit reimbursement bills"
results = policies.query(query_texts=[query], n_results=2)
print(results)

