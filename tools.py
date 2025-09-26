from datetime import datetime
import os
import matplotlib.pyplot as plt
from typing import List, Dict
from pydantic import BaseModel
import re

# ----------------------------------------
# Insurance Schema (for reference typing)
# ----------------------------------------
class InsuranceDetails(BaseModel):
    coverage: str
    estimated_premium: str
    reason: str
    add_ons: List[str]

class InsuranceRecommendation(BaseModel):
    term_insurance: InsuranceDetails
    health_insurance: InsuranceDetails
    premium_affordability_check: str
    additional_advice: List[str]
    products_to_avoid: List[str]
    vehicle_insurance: InsuranceDetails | None = None
    property_insurance: InsuranceDetails | None = None
    travel_insurance: InsuranceDetails | None = None
    personal_accident_cover: InsuranceDetails | None = None

# ----------------------------------------
# 1. Save recommendation to file
# ----------------------------------------
def save_insurance_recommendation(parsed_output: InsuranceRecommendation, matched_products: Dict = None, filename: str = "insurance_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"--- Recommendation Output ---\nTimestamp: {timestamp}\n"]

    lines.append(" Must-Have Insurance:")
    lines.append(f"- Term Insurance → {parsed_output.term_insurance.reason}")
    lines.append(f"- Health Insurance → {parsed_output.health_insurance.reason}\n")

    lines.append("🚗 Recommended (if applicable):")
    if parsed_output.vehicle_insurance:
        lines.append(f"- Vehicle Insurance → {parsed_output.vehicle_insurance.reason}")
    if parsed_output.travel_insurance:
        lines.append(f"- Travel Insurance → {parsed_output.travel_insurance.reason}")
    if not parsed_output.vehicle_insurance and not parsed_output.travel_insurance:
        lines.append("- None")

    lines.append("\n💡 Optional Coverage:")
    if parsed_output.personal_accident_cover:
        lines.append("- Personal Accident Cover → Covers accidental injuries or death.")
    if "critical illness" in " ".join(parsed_output.term_insurance.add_ons).lower():
        lines.append("- Critical Illness Rider → Protects against major diseases.")
    if not parsed_output.personal_accident_cover:
        lines.append("- None")

    # Detailed plans
    def plan_block(label, plan: InsuranceDetails):
        return (
            f"\n📌 {label}:\n"
            f"- Coverage: {plan.coverage}\n"
            f"- Premium: {plan.estimated_premium}\n"
            f"- Reason: {plan.reason}\n"
            f"- Add-ons: {', '.join(plan.add_ons) if plan.add_ons else 'None'}\n"
        )
    lines.append(plan_block("Term Insurance", parsed_output.term_insurance))
    lines.append(plan_block("Health Insurance", parsed_output.health_insurance))
    if parsed_output.vehicle_insurance:
        lines.append(plan_block("Vehicle Insurance", parsed_output.vehicle_insurance))
    if parsed_output.travel_insurance:
        lines.append(plan_block("Travel Insurance", parsed_output.travel_insurance))
    if parsed_output.personal_accident_cover:
        lines.append(plan_block("Personal Accident Cover", parsed_output.personal_accident_cover))

    # Advice
    lines.append(f"✅ Affordability Check:\n{parsed_output.premium_affordability_check}\n")
    lines.append("💡 Additional Advice:")
    lines.extend(f"- {tip}" for tip in parsed_output.additional_advice)

    lines.append("❌ Products to Avoid:")
    lines.extend(f"- {item}" for item in parsed_output.products_to_avoid)

    # Real-world products
    if matched_products:
        lines.append("\n🔎 Suggested Real Insurance Products:")
        for category, products in matched_products.items():
            lines.append(f"\n📌 {category}:")
            for p in products:
                lines.append(f"- {p['company']} offers {', '.join(p['plans'])} (Score: {p['score']})")
                lines.append(f"  {p['explanation']}")

    # Save to file
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n\n")
    return filename

# ----------------------------------------
# 2. GenAI Explanation Helper
# ----------------------------------------
def generate_explanation(plan: InsuranceDetails, label: str) -> str:
    return f"{label} insurance is recommended because: {plan.reason} It offers {plan.coverage} at {plan.estimated_premium} with add-ons like {', '.join(plan.add_ons)}."

# ----------------------------------------
# 3. Visualize affordability vs income
# ----------------------------------------

def parse_money(value: str) -> int:
    """Convert strings like ₹2 Crore, ₹20L, 2,50,000/month → integer rupees."""
    if isinstance(value, (int, float)):
        return int(value)
    if not value:
        return 0

    # Normalize
    value = str(value).replace(",", "").replace("₹", "").strip().lower()

    # Crore conversion
    if "crore" in value or "cr" in value:
        digits = re.findall(r"\d+\.?\d*", value)
        return int(float(digits[0]) * 1e7) if digits else 0

    # Lakh conversion
    if "lakh" in value or "lac" in value or "l" in value:
        digits = re.findall(r"\d+\.?\d*", value)
        return int(float(digits[0]) * 1e5) if digits else 0

    # Plain number
    digits = re.findall(r"\d+", value)
    return int(digits[0]) if digits else 0

def visualize_affordability_chart(term_premium, health_premium, monthly_income, save_path=None):
    # Convert everything to int
    term_premium = parse_money(term_premium)
    health_premium = parse_money(health_premium)
    monthly_income = parse_money(monthly_income)

    if save_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        save_path = f"affordability_chart_{timestamp}.png"

    remaining_income = max(monthly_income - (term_premium + health_premium), 0)
    labels = ['Remaining Income', 'Term Insurance', 'Health Insurance']
    values = [remaining_income, term_premium, health_premium]
    colors = ['#4caf50', '#f44336', '#2196f3']

    non_zero_labels, non_zero_values, non_zero_colors = [], [], []
    for label, value, color in zip(labels, values, colors):
        if value > 0:
            non_zero_labels.append(label)
            non_zero_values.append(value)
            non_zero_colors.append(color)

    plt.figure(figsize=(8, 6))
    if non_zero_values:
        plt.pie(non_zero_values, labels=non_zero_labels, autopct='%1.1f%%',
                colors=non_zero_colors, startangle=140)
    else:
        plt.text(0.5, 0.5, 'No data to display', ha='center', va='center',
                 transform=plt.gca().transAxes)

    plt.title("Premium vs Monthly Income", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

def visualize_coverage_vs_income_chart(term_coverage, health_coverage, monthly_income, save_path=None):
    """Visualize insurance coverage vs annual income with formatted labels."""

    # ✅ Parse values to integers
    term_coverage = parse_money(term_coverage)
    health_coverage = parse_money(health_coverage)
    monthly_income = parse_money(monthly_income)

    if save_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"coverage_vs_income_chart_{timestamp}.png"

    labels = ['Term Insurance', 'Health Insurance']
    coverage_values = [term_coverage, health_coverage]
    income_value = monthly_income * 12  # Annual income

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, coverage_values, color=['#4caf50', '#2196f3'], alpha=0.8, width=0.6)

    # Add text labels with better formatting for large numbers
    for bar in bars:
        height = bar.get_height()
        if height >= 10000000:  # 1 crore
            label_text = f"₹{height/10000000:.1f}Cr"
        elif height >= 100000:  # 1 lakh
            label_text = f"₹{height/100000:.1f}L"
        else:
            label_text = f"₹{height:,}"

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + max(coverage_values) * 0.02,
            label_text,
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    # Add annual income line with better formatting
    if income_value >= 10000000:
        income_label = f'Annual Income (₹{income_value/10000000:.1f}Cr)'
    elif income_value >= 100000:
        income_label = f'Annual Income (₹{income_value/100000:.1f}L)'
    else:
        income_label = f'Annual Income (₹{income_value:,})'

    plt.axhline(y=income_value, color='red', linestyle='--', linewidth=2, label=income_label)
    plt.ylabel("Amount (₹)", fontsize=12)
    plt.title("Insurance Coverage vs Annual Income", fontsize=14, fontweight='bold')
    plt.ylim(0, max(max(coverage_values), income_value) * 1.3)
    plt.legend(loc='upper right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path
def visualize_coverage_adequacy(actual_coverage, annual_income, multiplier=10, save_path="coverage_adequacy.png"):
    """Visualize how adequate coverage is compared to recommended (annual_income × multiplier)."""

    # ✅ Parse values to integers
    actual_coverage = parse_money(actual_coverage)
    annual_income = parse_money(annual_income)

    recommended = annual_income * multiplier
    adequacy = (actual_coverage / recommended) * 100 if recommended > 0 else 0

    # Clamp value between 0–120% for chart
    adequacy = min(adequacy, 120)

    plt.figure(figsize=(10, 4))

    # Create horizontal bar chart
    bar_color = "green" if adequacy >= 100 else "orange" if adequacy >= 50 else "red"
    bars = plt.barh(["Coverage Adequacy"], [adequacy], color=bar_color, height=0.6, alpha=0.8)

    # Add recommended line
    plt.axvline(x=100, color="black", linestyle="--", linewidth=2, label="Recommended (100%)")

    # Set x-axis limits
    plt.xlim(0, 120)

    # Add percentage text on the bar
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height()/2,
                f"{adequacy:.1f}%", ha='left', va='center', fontsize=12, fontweight='bold')

    # Add coverage amount text
    if actual_coverage >= 10000000:
        coverage_text = f"Current: ₹{actual_coverage/10000000:.1f}Cr"
    elif actual_coverage >= 100000:
        coverage_text = f"Current: ₹{actual_coverage/100000:.1f}L"
    else:
        coverage_text = f"Current: ₹{actual_coverage:,}"

    if recommended >= 10000000:
        recommended_text = f"Recommended: ₹{recommended/10000000:.1f}Cr"
    elif recommended >= 100000:
        recommended_text = f"Recommended: ₹{recommended/100000:.1f}L"
    else:
        recommended_text = f"Recommended: ₹{recommended:,}"

    plt.text(5, 0.3, coverage_text, fontsize=10, style='italic')
    plt.text(5, -0.3, recommended_text, fontsize=10, style='italic')

    plt.xlabel("Coverage Adequacy (%)", fontsize=12)
    plt.title("Insurance Coverage Adequacy Assessment", fontsize=14, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path
def explain_affordability(term_premium, health_premium, monthly_income):
    total_premium = term_premium + health_premium
    percent = (total_premium / monthly_income) * 100
    if percent > 20:
        return f"⚠️ Your premiums take up {percent:.1f}% of your monthly income. Consider reducing coverage or finding lower-cost plans."
    else:
        return f"✅ Your premiums are only {percent:.1f}% of income. This is affordable and manageable."
    

def explain_coverage_vs_income(term_coverage, health_coverage, annual_income):
    total_coverage = term_coverage + health_coverage
    if total_coverage < annual_income * 5:
        return "⚠️ Your total coverage is less than 5× your annual income. You may be underinsured."
    elif total_coverage < annual_income * 10:
        return "ℹ️ Your coverage is reasonable, but you might increase it for better security."
    else:
        return "✅ Your coverage is strong compared to your income."
    

def explain_coverage_adequacy(actual_coverage, annual_income, multiplier=10):
    recommended = annual_income * multiplier
    if actual_coverage < recommended * 0.5:
        return "❌ You are severely underinsured. Increase your coverage immediately."
    elif actual_coverage < recommended:
        return "⚠️ You are underinsured. Consider topping up your policy."
    else:
        return "✅ You are adequately insured."
