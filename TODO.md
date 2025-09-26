# TODO List for Fixing Insurance Advisor

## 1. Fix Syntax Errors in main.py
- [ ] Correct indentation for openai.api_key assignment
- [ ] Ensure proper LLM initialization

## 2. Switch to Pure GPT Model Predictions
- [ ] Replace rule-based calculate_insurance_recommendations with LLM-based using recommendation_chain
- [ ] Update get_recommendation to use LLM for recommendations

## 3. Fix What-If Question Function
- [ ] Correct LLM call in answer_what_if_question to use llm.invoke
- [ ] Ensure it uses text vector embeddings correctly

## 4. Update App.py for What-If
- [ ] Modify answer_what_if_question call to pass profile_text

## 5. Verify Matching Products
- [ ] Ensure get_matching_products correctly references products.py

## 6. Test the Changes
- [ ] Run test_debug.py to verify functionality
- [ ] Check charts and recommendations accuracy
