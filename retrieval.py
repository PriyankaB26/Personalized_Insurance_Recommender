from products import insurance_products

# Simple fallback without sentence-transformers for now
def build_product_sentences():
    sentences = []
    for company, details in insurance_products.items():
        csr = details.get("claim_settlement_ratio", "N/A")
        plans = ", ".join(details.get("plans", []))
        coverage_text = ", ".join(f"{k}: {v}" for k, v in details.get("coverage", {}).items())

        sentence = (
            f"{company} offers insurance. "
            f"Plans: {plans}. Claim Settlement Ratio: {csr}. Coverage: {coverage_text}."
        )
        sentences.append(sentence)
    return sentences

# Build product sentences
product_sentences = build_product_sentences()

# Mock embeddings and model for now
product_embeddings = None
embedding_model = None

def query_products(user_question: str, k: int = 3):
    # Simple keyword matching fallback
    results = []
    for sentence in product_sentences:
        if any(word.lower() in sentence.lower() for word in user_question.split()):
            results.append(sentence)
    return results[:k] if results else product_sentences[:k]
