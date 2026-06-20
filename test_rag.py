from rag_pipeline import get_answer

question = "Why is OSPF not forming adjacency?"

result = get_answer(question)

print("\nANSWER:\n")
print(result["answer"])

print("\nSOURCES:\n")
print(result["sources"])