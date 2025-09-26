# Personalized Insurance Recommender Agent

## Introduction
The **Personalized Insurance Recommender Agent** is an AI-powered platform that provides customized insurance recommendations based on a user's profile, financial situation, and lifestyle. It helps users understand the types of insurance they need, suggests suitable insurance products, and visualizes affordability and coverage adequacy to aid in informed decision-making.

This system integrates **Google's Gemini AI**, **LangChain**, **Streamlit**, and Python-based analysis tools to deliver personalized recommendations and actionable insights.

---

## Features
- Personalized insurance recommendations for:
  - Term Insurance
  - Health Insurance
  - Vehicle Insurance
  - Travel Insurance
  - Personal Accident Cover
- Affordability analysis against monthly income
- Coverage adequacy assessment
- Visualization of premium distribution and coverage vs. income
- Explanation of recommendations and what-if scenario analysis
- Integration with real insurance products to suggest top matching plans
- User-friendly interactive interface with **Streamlit**
- Automatic JSON output generation for structured recommendation

---

## Tech Stack & Libraries Used
- **Programming & Frameworks:** Python, Streamlit
- **AI & NLP:** `google.generativeai`, `langchain_google_genai`, LLMs (`gemini-2.5-pro`)
- **Data Handling & Modeling:** Pydantic, NumPy
- **Visualization:** Matplotlib
- **Environment Management:** `python-dotenv`
- **Custom Modules:** 
  - `products.py` → Contains structured insurance product data  
  - `retrieval.py` → Handles querying and embeddings for products  
  - `tools.py` → Utility functions for saving recommendations, generating charts, explanations, etc.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/insurance-recommender.git
   cd insurance-recommender
2. Install dependencies:
pip install -r requirements.txt
3. Set up environment variables:
# .env
GEMINI_API_KEY=your_google_gemini_api_key
4. Run the Streamlit app:
streamlit run app.py

## Implementation

## Implementation Details

### AI Recommendation Engine
- Uses **Google Gemini LLM** to analyze customer profiles and generate structured JSON recommendations.
- The JSON output adheres to the **InsuranceRecommendation Pydantic model**.
- Recommendations include:
  - Coverage
  - Estimated premium
  - Reasons for recommendations
  - Add-ons
  - Priority
  - Affordability check
  - Products to avoid

### Rules-Based Calculations
- **Term insurance coverage**: 10–20× annual income
- **Health insurance coverage**: 10–15 lakhs based on age
- **Vehicle & personal accident insurance**: fixed coverage and premiums
- **Affordability**: compared against monthly income
- **Coverage adequacy**: compared against annual income × multiplier (default 10)

### Product Matching
- Suggests real insurance products based on:
  - Coverage match
  - Product type
  - Claim Settlement Ratio (CSR)
  - Score-based ranking

### Visualizations
- **Premium vs Income**: Pie chart showing term, health, and remaining income
- **Coverage vs Annual Income**: Bar chart comparing recommended coverage to user's income
- **Coverage Adequacy**: Horizontal bar displaying coverage adequacy percentage

---

## Future Enhancements
- Integration with more insurance categories and products
- Real-time premium calculations using live insurance provider APIs
- Personalized add-on suggestions leveraging advanced AI models
- Multi-language support for user interface
- Enhanced interactive visualizations
