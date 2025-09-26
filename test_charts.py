from tools import visualize_affordability_chart, visualize_coverage_vs_income_chart
from main import extract_number

# Test chart generation with different values
print("Testing chart generation...")

# Test values
income = 50000
term_premium = 1000
health_premium = 500
term_coverage = 1000000
health_coverage = 500000

print(f"Test values - Income: {income}, Term Premium: {term_premium}, Health Premium: {health_premium}")
print(f"Coverage values - Term: {term_coverage}, Health: {health_coverage}")

try:
    # Generate charts
    chart1 = visualize_affordability_chart(term_premium, health_premium, income)
    chart2 = visualize_coverage_vs_income_chart(term_coverage, health_coverage, income)
    
    print(f"Charts generated successfully:")
    print(f"Affordability chart: {chart1}")
    print(f"Coverage chart: {chart2}")
    
except Exception as e:
    print(f"Error generating charts: {e}")
    import traceback
    traceback.print_exc() 