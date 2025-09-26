from main import get_recommendation

# Test with a sample profile
profile_text = """Age: 35
Monthly Income: ₹75000
Marital Status: Married
Dependents: 2
Employment: Private Job
Existing Insurance: None
Health Conditions: None
Vehicle: Yes
Owns Property: Yes
Frequent Traveler: No
"""

print("Testing get_recommendation with sample profile...")
result = get_recommendation(profile_text)

if "error" in result:
    print(f"Error: {result['error']}")
else:
    print("Recommendation generated successfully!")
    print(f"Term Coverage: {result['recommendation'].term_insurance.coverage}")
    print(f"Term Premium: {result['recommendation'].term_insurance.estimated_premium}")
    print(f"Health Coverage: {result['recommendation'].health_insurance.coverage}")
    print(f"Health Premium: {result['recommendation'].health_insurance.estimated_premium}")
