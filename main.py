import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()
import os

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional
from langchain.prompts import PromptTemplate
import re
from products import insurance_products
from retrieval import query_products, product_sentences, product_embeddings, embedding_model
import numpy as np
from tools import (
    save_insurance_recommendation,
    generate_explanation,
    visualize_affordability_chart,
    visualize_coverage_vs_income_chart,
    visualize_coverage_adequacy,
    explain_affordability,
    explain_coverage_adequacy,
    explain_coverage_vs_income,
    parse_money
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def parse_csr_value(csr_value):
    """Parse CSR value from various formats and return numeric value."""
    if csr_value is None:
        return 0

    # Convert to string first
    csr_str = str(csr_value).strip()

    # Try to extract percentage from text like "High persistency, ~88.1% renewals"
    import re
    match = re.search(r'(\d+(?:\.\d+)?)%', csr_str)
    if match:
        return float(match.group(1))

    # Try to extract number with ~ symbol like "~88.1"
    match = re.search(r'~?(\d+(?:\.\d+)?)', csr_str)
    if match:
        return float(match.group(1))

    # Try direct float conversion
    try:
        return float(csr_str)
    except ValueError:
        return 0

def get_matching_products(product_type, user_requirements):
    matches = []

    for company, details in insurance_products.items():
        # Company-level CSR for explanation - try both field names
        csr = details.get("csr") or details.get("claim_settlement_ratio")

        # Handle different product structures
        products = []
        if "products" in details:
            # Structure like ICICI, SBI, Axis
            for prod in details["products"]:
                if prod.get("type") == product_type:
                    products.append(prod)
        elif "plans" in details:
            # Structure like Tata AIA, Kotak, HDFC, LIC, Aditya Birla
            # For these companies, we need to infer the type from the plan name or company offerings
            if product_type == "term" and any("term" in plan.lower() for plan in details["plans"]):
                products = [{"name": plan, "type": product_type, "coverage": details.get("coverage", {})} for plan in details["plans"] if "term" in plan.lower()]
            elif product_type == "health" and any("health" in plan.lower() or "optima" in plan.lower() or "suraksha" in plan.lower() for plan in details["plans"]):
                products = [{"name": plan, "type": product_type, "coverage": details.get("coverage", {})} for plan in details["plans"] if "health" in plan.lower() or "optima" in plan.lower() or "suraksha" in plan.lower()]
            else:
                # For companies with plans structure, include all plans for the product type
                products = [{"name": plan, "type": product_type, "coverage": details.get("coverage", {})} for plan in details["plans"]]

        for product in products:
            score = 0
            matched_criteria = []

            # Check coverage matching
            coverage_info = product.get("coverage", {})
            if isinstance(coverage_info, dict):
                for req_key, req_val in user_requirements.items():
                    if req_key in coverage_info:
                        if str(req_val).lower() in str(coverage_info[req_key]).lower():
                            score += 1
                            matched_criteria.append(req_key)
                    elif req_key == "coverage" and "sum_assured" in coverage_info:
                        # Special case for term insurance coverage
                        if str(req_val).lower() in str(coverage_info).lower():
                            score += 1
                            matched_criteria.append("coverage")
                    elif req_key == "coverage":
                        # Check if the required coverage amount is mentioned in coverage info
                        if str(req_val).lower() in str(coverage_info).lower():
                            score += 1
                            matched_criteria.append("coverage")

            # If no specific coverage match, give a base score for having the right product type
            if score == 0 and product.get("type") == product_type:
                score = 1
                matched_criteria.append("product_type")

            if score > 0:
                plan_name = product.get("name", "Insurance Plan")
                explanation = (
                    f"{company} offers {plan_name} "
                    f"with Claim Settlement Ratio {csr}. "
                    f"It matches your needs for {', '.join(matched_criteria)}."
                )
                matches.append({
                    "company": company,
                    "plans": [plan_name],
                    "score": score,
                    "explanation": explanation,
                    "csr": csr
                })

    # Sort by highest score, then CSR if available - use the new parsing function
    matches.sort(key=lambda x: (x["score"], parse_csr_value(x.get("csr")), x.get("company", "")), reverse=True)

    # Return top matches (increased to 3 for better selection)
    return matches[:3]

def extract_number(coverage_str):
    if not coverage_str:
        return 0
    # Extract numeric value from coverage string
    coverage_str = coverage_str.replace("₹", "").strip().lower()
    match = re.search(r"₹?\s*(\d+)([lcr]?)", coverage_str)
    if not match:
        return 0
    number, unit = match.groups()
    number = int(number)
    return number * 1_00_000 if unit == "l" else number * 1_00_00_000 if unit == "c" else number


class InsuranceDetails(BaseModel):
    coverage: str
    estimated_premium: str
    reason: str
    add_ons: Optional[List[str]] = []
    priority: Optional[str] = None
class InsuranceRecommendation(BaseModel):
    term_insurance: InsuranceDetails
    health_insurance: InsuranceDetails
    vehicle_insurance: Optional[InsuranceDetails] = None
    property_insurance: Optional[InsuranceDetails] = None
    travel_insurance: Optional[InsuranceDetails] = None
    personal_accident_cover: Optional[InsuranceDetails] = None
    premium_affordability_check: Optional[str] = None
    additional_advice: Optional[List[str]] = []
    products_to_avoid: Optional[List[str]] = []

def build_clean_prompt() -> PromptTemplate:
    template = """You are an expert insurance advisor. Analyze the following customer profile and provide personalized insurance recommendations.

{profile_text}

Instructions:
- Consider age, income, family status, occupation, location, and assets.
- Calculate coverage amounts and premiums realistically.
- Recommend add-ons and priorities for each insurance type.
- Include advice on affordability, additional guidance, and products to avoid.

CRITICAL: Your response must be ONLY valid JSON. Do not include any text before or after the JSON. Do not use markdown code blocks. Start directly with {{ and end with }}.

Output format:

{{
  "term_insurance": {{
    "coverage": "",
    "estimated_premium": "",
    "reason": "",
    "add_ons": [],
    "priority": ""
  }},
  "health_insurance": {{
    "coverage": "",
    "estimated_premium": "",
    "reason": "",
    "add_ons": [],
    "priority": ""
  }},
  "vehicle_insurance": null,
  "property_insurance": null,
  "travel_insurance": null,
  "personal_accident_cover": null,
  "premium_affordability_check": "",
  "additional_advice": [],
  "products_to_avoid": []
}}

Fill in all the empty strings and arrays with appropriate values based on the customer's profile. Ensure the JSON is complete and valid."""
    return PromptTemplate(input_variables=["profile_text"], template=template)

parser = PydanticOutputParser(pydantic_object=InsuranceRecommendation)

recommendation_chain = LLMChain(
    llm=llm,
    prompt=build_clean_prompt()
)


def calculate_insurance_recommendations(profile_text: str):
    """Calculate insurance recommendations based on profile data using rules."""

    # Parse profile data
    lines = profile_text.strip().split('\n')
    profile_data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            profile_data[key.strip()] = value.strip()

    age = int(profile_data.get('Age', '35'))
    income = int(profile_data.get('Monthly Income', '₹75000').replace('₹', ''))
    marital_status = profile_data.get('Marital Status', 'Married')
    dependents = int(profile_data.get('Dependents', '2'))
    employment = profile_data.get('Employment', 'Private Job')
    vehicle = profile_data.get('Vehicle', 'Yes')
    owns_property = profile_data.get('Owns Property', 'Yes')

    # Calculate term insurance coverage (typically 10-20x annual income)
    annual_income = income * 12
    term_coverage_multiplier = 15 if dependents > 0 else 10
    term_coverage = min(annual_income * term_coverage_multiplier, 20000000)  # Cap at 2 crores

    # Calculate term premium (rough estimate based on age and coverage)
    term_premium = (term_coverage / 100000) * (age / 100) * 1000  # Rough calculation

    # Calculate health insurance coverage
    health_coverage = 1000000 if age < 40 else 1500000  # 10-15 lakhs based on age

    # Calculate health premium
    health_premium = health_coverage / 100000 * 80  # Rough calculation

    # Format coverage strings
    def format_coverage(amount):
        if amount >= 10000000:  # 1 crore
            return f"₹{amount//10000000} crores"
        else:
            return f"₹{amount//100000} lakhs"

    def format_premium(amount):
        return f"₹{int(amount)}/year"

    # Create recommendation object
    term_insurance = InsuranceDetails(
        coverage=format_coverage(term_coverage),
        estimated_premium=format_premium(term_premium),
        reason=f"Provides financial security for {'family' if dependents > 0 else 'your future'}",
        add_ons=["Critical Illness Rider", "Waiver of Premium"],
        priority="must-have"
    )

    health_insurance = InsuranceDetails(
        coverage=format_coverage(health_coverage),
        estimated_premium=format_premium(health_premium),
        reason="Covers medical expenses and hospitalization",
        add_ons=["Maternity Cover" if dependents > 0 else "OPD Cover", "Critical Illness"],
        priority="must-have"
    )

    vehicle_insurance = InsuranceDetails(
        coverage="₹5 lakhs",
        estimated_premium="₹3,000/year",
        reason="Protects vehicle from damage and theft",
        add_ons=["Zero Depreciation", "Roadside Assistance"],
        priority="recommended"
    ) if vehicle == "Yes" else None

    personal_accident_cover = InsuranceDetails(
        coverage="₹25 lakhs",
        estimated_premium="₹1,000/year",
        reason="Accident protection and disability coverage",
        add_ons=["Permanent Disability", "Temporary Disability"],
        priority="recommended"
    )

    # Calculate affordability
    total_premium = term_premium + health_premium
    if vehicle_insurance:
        total_premium += 3000
    if personal_accident_cover:
        total_premium += 1000

    affordability = "Premiums are affordable" if total_premium < income * 0.1 else "Premiums may be high - consider lower coverage options"

    return InsuranceRecommendation(
        term_insurance=term_insurance,
        health_insurance=health_insurance,
        vehicle_insurance=vehicle_insurance,
        property_insurance=None,
        travel_insurance=None,
        personal_accident_cover=personal_accident_cover,
        premium_affordability_check=affordability,
        additional_advice=["Consider increasing coverage as income grows", "Review coverage annually"],
        products_to_avoid=["High-commission products", "Products with low claim settlement ratio"]
    )

def clean_json_output(output: str) -> str:
    """Clean the LLM output to extract valid JSON."""
    import json
    import re

    # Remove markdown code blocks if present
    output = re.sub(r'```json\s*', '', output)
    output = re.sub(r'```\s*', '', output)

    # Find JSON object in the output
    start = output.find('{')
    end = output.rfind('}') + 1

    if start != -1 and end > start:
        json_str = output[start:end]
        try:
            # Validate it's valid JSON
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            pass

    # If no valid JSON found, return the original output
    return output

def get_recommendation(profile_text: str):
    try:
        # Use LLM for pure predictions
        output = recommendation_chain.run(profile_text=profile_text)
        cleaned_output = clean_json_output(output)
        recommendation = parser.parse(cleaned_output)

      

        # Match insurance products
        matched_products = {}
        term_matches = get_matching_products("term", {"coverage": recommendation.term_insurance.coverage})
        if term_matches:
            matched_products["Term Insurance"] = term_matches

        health_matches = get_matching_products("health", {"coverage": recommendation.health_insurance.coverage})
        if health_matches:
            matched_products["Health Insurance"] = health_matches

        # Save recommendation
        save_path = save_insurance_recommendation(recommendation, matched_products)
        explanation = generate_explanation(recommendation.term_insurance, "Term Insurance")

        # Generate charts
        income = extract_number(profile_text.split("Monthly Income: ₹")[1].split("\n")[0])
        term_val = extract_number(recommendation.term_insurance.estimated_premium)
        health_val = extract_number(recommendation.health_insurance.estimated_premium)
        term_coverage = extract_number(recommendation.term_insurance.coverage)
        health_coverage = extract_number(recommendation.health_insurance.coverage)

        chart_path = visualize_affordability_chart(term_val, health_val, income)

        coverage_chart_path = visualize_coverage_vs_income_chart(
            term_coverage, health_coverage, income
        )

        total_coverage = parse_money(term_coverage) + parse_money(health_coverage)
        coverage_adequacy = visualize_coverage_adequacy(total_coverage, income)

        affordability_tip = explain_affordability(term_val, health_val, income)
        coverage_tip = explain_coverage_vs_income(term_coverage, health_coverage, income)
        adequacy_tip = explain_coverage_adequacy(term_coverage + health_coverage, income)

        return {
            "recommendation": recommendation,
            "products": matched_products,
            "explanation": explanation,  # GenAI explanation
            "chart_path": chart_path,
            "coverage_chart_path": coverage_chart_path,
            "coverage_adequacy": coverage_adequacy,
            "affordability_tip": affordability_tip,
            "coverage_tip": coverage_tip,
            "adequacy_tip": adequacy_tip,
            "save_path": save_path
        }

    except Exception as e:
        return {"error": str(e)}
    
def answer_what_if_question(query: str, profile_text: str) -> str:
    try:
        if llm is None:
            return "Sorry, the AI model is not available. Please try again later."
        if not query.strip():
            return "Please enter a question."

        # --- Step 1: Embed query ---
        query_embedding = embedding_model.encode(query, convert_to_tensor=True)

        # --- Step 2: Compute cosine similarities ---
        scores = np.dot(product_embeddings, query_embedding) / (
            np.linalg.norm(product_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        top_indices = np.argsort(scores)[-3:][::-1]  # top-3 results
        retrieved_facts = [product_sentences[i] for i in top_indices]

        # --- Step 3: Build context ---
        context = "\n".join(retrieved_facts)

        # --- Step 4: Build final prompt ---
        prompt_text = f"""
You are an expert insurance advisor. Use the customer's profile and relevant product facts to guide your answer.

Customer Profile:
{profile_text}

Relevant Insurance Facts:
{context}

Question: {query}

Respond in 2-3 clear sentences. Focus on practical advice about what changes the person should consider in their insurance coverage. 
Keep the answer concise and actionable.
"""

        # --- Step 5: Call LLM ---
        text = llm.invoke(prompt_text).content

        # --- Step 6: Clean ---
        text = text.replace("Answer:", "").replace("###", "").strip()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return '. '.join(sentences[:3]) + '.'

    except Exception as e:
        return f"Error processing question: {str(e)}"