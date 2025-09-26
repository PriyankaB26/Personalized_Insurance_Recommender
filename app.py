import streamlit as st
from main import get_recommendation, extract_number, answer_what_if_question
import matplotlib.pyplot as plt

st.set_page_config(page_title="Insurance Advisor", layout="centered")
st.title("Personalized Insurance Recommender")

# -------------------
# Helper function
# -------------------
def show_plan(title, plan):
    st.markdown(f"### {title}")
    st.write(f"- Coverage: {plan.coverage}")
    st.write(f"- Premium: {plan.estimated_premium}")
    st.write(f"- Reason: {plan.reason}")
    st.write(f"- Add-ons: {', '.join(plan.add_ons) if plan.add_ons else 'None'}")

# -------------------
# Profile Form
# -------------------
with st.form("profile_form"):
    st.markdown("### Fill in Customer Profile")
    age_input = st.text_input("Enter Age")
    income_input = st.text_input("Enter Monthly Income (₹)")    
    marital_status = st.selectbox("Marital Status", ["Select...", "Single", "Married", "Divorced"])
    dependents = st.number_input("Dependents", min_value=0)
    employment = st.selectbox("Employment Type", ["Select...", "Private Job", "Government Job", "Self-Employed", "IT Professional"])
    existing_insurance = st.multiselect(
    "Existing Insurance Policies",
    ["Term Insurance", "Health Insurance", "Vehicle Insurance", "Travel Insurance", "None"])
    existing_insurance_dict = {
    "term_insurance": "Term Insurance" in existing_insurance,
    "health_insurance": "Health Insurance" in existing_insurance,
    "vehicle_insurance": "Vehicle Insurance" in existing_insurance,
    "travel_insurance": "Travel Insurance" in existing_insurance
    }
    health_conditions = st.selectbox("Health Conditions", ["Select...", "None", "Diabetes", "Heart Issues", "Other"])
    vehicle = st.radio("Do you have a vehicle?", ["Yes", "No"])
    owns_property = st.radio("Owns Property?", ["Yes", "No"])
    frequent_traveler = st.radio("Frequent Traveler?", ["Yes", "No"])
    submitted = st.form_submit_button("Get Recommendation")

# -------------------
# Processing after submission
# -------------------
if submitted:
    if not age_input.isdigit() or not income_input.isdigit():
        st.error("Please enter valid numeric values for Age and Monthly Income.")
        st.stop()

    age = int(age_input)
    income = int(income_input)
    if marital_status == "Select..." or employment == "Select..." or health_conditions == "Select...":
        st.warning("Please complete all required fields before submitting.")
        st.stop()


    user_input = {
        "age": age,
        "income": income,
        "marital_status": marital_status,
        "dependents": dependents,
        "employment": employment,
        "existing_insurance": existing_insurance_dict,
        "health_conditions": health_conditions,
        "vehicle": vehicle,
        "owns_property": owns_property,
        "frequent_traveler": frequent_traveler
    }


    with st.spinner("Generating recommendations..."):
        # Convert user_input dict to formatted string for get_recommendation
        profile_text = (
            f"Age: {user_input['age']}\n"
            f"Monthly Income: ₹{user_input['income']}\n"
            f"Marital Status: {user_input['marital_status']}\n"
            f"Dependents: {user_input['dependents']}\n"
            f"Employment: {user_input['employment']}\n"
            f"Existing Insurance: {', '.join([k for k, v in user_input['existing_insurance'].items() if v])}\n"
            f"Health Conditions: {user_input['health_conditions']}\n"
            f"Vehicle: {user_input['vehicle']}\n"
            f"Owns Property: {user_input['owns_property']}\n"
            f"Frequent Traveler: {user_input['frequent_traveler']}\n"
        )
        result = get_recommendation(profile_text)
        if "error" in result:
            st.error("Failed to generate recommendation.")
            st.exception(result["error"])
            st.stop()

        recommendation = result["recommendation"]
        matched_products = result["products"]
        explanation = result["explanation"]

    # -------------------
    # Recommendations
    # -------------------
    st.subheader("Prioritized Insurance Recommendation")
    st.markdown("### Must-Have Insurance")
    st.write(f"- Term Insurance: {recommendation.term_insurance.reason}")
    st.write(f"- Health Insurance: {recommendation.health_insurance.reason}")

    st.markdown("### Recommended (if applicable)")
    if recommendation.vehicle_insurance:
        st.write(f"- Vehicle Insurance: {recommendation.vehicle_insurance.reason}")
    if recommendation.travel_insurance:
        st.write(f"- Travel Insurance: {recommendation.travel_insurance.reason}")

    st.markdown("### Optional")
    if recommendation.personal_accident_cover:
        st.write("- Personal Accident Cover: Helps in accidental injuries.")
    if "Critical Illness" in " ".join(recommendation.term_insurance.add_ons):
        st.write("- Critical Illness Rider: For major diseases.")

    # -------------------
    # Show Plans
    # -------------------
    show_plan("Term Insurance", recommendation.term_insurance)
    show_plan("Health Insurance", recommendation.health_insurance)
    if recommendation.vehicle_insurance:
        show_plan("Vehicle Insurance", recommendation.vehicle_insurance)
    if recommendation.travel_insurance:
        show_plan("Travel Insurance", recommendation.travel_insurance)
    if recommendation.personal_accident_cover:
        show_plan("Personal Accident Cover", recommendation.personal_accident_cover)

    # -------------------
    # Advice Sections
    # -------------------
    st.subheader("💰 Affordability Check")
    st.write(recommendation.premium_affordability_check)

    st.subheader("💡 Additional Advice")
    for tip in recommendation.additional_advice:
        st.write("-", tip)

    st.subheader("❌ Products to Avoid")
    for item in recommendation.products_to_avoid:
        st.write("-", item)

    # -------------------
    # Real Products
    # -------------------
    st.subheader("🔎 Suggested Real Insurance Products")
    for category, prods in matched_products.items():
        st.markdown(f"#### {category}")
        for p in prods:
            plans = ", ".join(p["plans"])

            st.markdown(f"- **{p['plans'][0]}** by *{p['company']}* → {p['explanation']}")


    # -------------------
    # Explanations
    # -------------------
    st.subheader("📖 Explanation")
    st.info(explanation)

    # -------------------
    # Charts + Tips (only once)
    # -------------------
    st.subheader("📊 Premium vs Income")
    if result.get("chart_path"):
        st.image(result["chart_path"], caption="Premium distribution vs income", use_container_width=True)
        st.info(result.get("affordability_tip", ""))
    else:
        st.warning("Chart could not be generated due to missing values.")

    st.subheader("📊 Coverage vs Income")
    if result.get("coverage_chart_path"):
        st.image(result["coverage_chart_path"], caption="Coverage vs Annual Income", use_container_width=True)
        st.info(result.get("coverage_tip", ""))
    else:
        st.warning("Coverage chart not available.")

    st.subheader("📊 Coverage Adequacy")
    if result.get("coverage_adequacy"):
        st.image(result["coverage_adequacy"], caption="Adequacy Gauge", use_container_width=True)
        st.info(result.get("adequacy_tip", ""))
    else:
        st.warning("Coverage adequacy chart not available.")

    # -------------------
    # What-if Section
    # -------------------
    st.markdown("---")
    st.subheader("🤔 Ask a What-If Question")

    suggested_qs = [
        "What if my income increases by 20%?",
        "What if I add 2 more dependents?",
        "Which insurance company has the highest claim settlement ratio?",
        "What if I increase my health coverage to ₹15 lakhs?"
    ]

    user_q = st.selectbox(
        "Choose a suggested question (or type your own):",
        ["-- Type your own --"] + suggested_qs,
        key="what_if_dropdown"
    )

    if user_q == "-- Type your own --":
        custom_q = st.text_input(
            "Enter your own What-If question:",
            key="what_if_custom"
        )
    else:
        custom_q = ""

# Container for response
    response_container = st.empty()

    if st.button("Submit Question", key="submit_question"):
        final_q = custom_q if user_q == "-- Type your own --" else user_q
        if not final_q or final_q.strip() == "":
            st.warning("Please enter or select a question first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    st.write(f"Processing question: {final_q}")
                    reply = answer_what_if_question(final_q, profile_text)
                    st.session_state["what_if_reply"] = reply
                except Exception as e:
                    st.error(f"Error processing your question: {str(e)}")
                    st.exception(e)

# Display reply if available
if "what_if_reply" in st.session_state:
    response_container.markdown("**Response:**")
    response_container.write(st.session_state["what_if_reply"])
