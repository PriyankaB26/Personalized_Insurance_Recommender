insurance_products = {
    "Tata AIA Life Insurance": {
        "plans": ["Tata AIA Term Insurance", "Tata AIA ULIP Plan", "Tata AIA Savings Plan", "Tata AIA Combo Plan"],
        "coverage": {
            "sum_assured": "Provided upon death of policyholder",
            "maturity_benefit": True,
            "guaranteed_returns": True,
            "riders": ["Critical Illness", "Education Secure"]
        },
        "premium": {
            "payment_options": ["Single", "Annual", "Semi-annual", "Monthly"],
            "discounts": ["Digital Discount", "Female Lives Discount"]
        },
        "tenure_eligibility": {
            "entry_age_min": 18,
            "policy_term_range": "5-40 years",
            "maturity_age": 70
        },
        "claim_settlement_ratio": "High persistency, ~88.1% renewals",
        "waiting_period": {
            "standard": "12 months (suicidal deaths)",
            "guaranteed_plans": "2-3 years",
            "benefit_during_period": "Return of premium"
        }
    },

    "ICICI Prudential Life Insurance": {
        "claim_settlement_ratio": 95.30,  # FY 2023-24
        "products": [
            {
                "name": "ICICI Term Insurance",
                "type": "term",
                "coverage": "Varies (increasing on life events, riders available)",
                "premium": {"min": 2400, "mode": ["single", "limited", "regular"]},
                "tenure": {"min": 5, "max": 81},
                "eligibility": {"min_age": 18, "max_age": 65, "health_required": True},
                "riders": ["critical illness", "terminal illness", "accidental death"],
                "waiting_period": None
            },
            {
                "name": "ICICI Return of Premium (ROP) Term Plan",
                "type": "term + return_of_premium",
                "coverage": "Refund of premiums on survival",
                "premium": {"min": 2400, "mode": ["regular", "limited"]},
                "tenure": {"min": 10, "max": 70},
                "eligibility": {"min_age": 18, "max_age": 60},
                "riders": ["accidental death"],
                "waiting_period": None
            },
            {
                "name": "ICICI All-in-One Plan",
                "type": "life + critical_illness",
                "coverage": "Life cover + Critical illness benefits",
                "premium": {"min": 5000, "mode": ["regular"]},
                "tenure": {"min": 10, "max": 81},
                "eligibility": {"min_age": 18, "max_age": 60},
                "riders": ["terminal illness", "accidental death"],
                "waiting_period": {"health_riders": "1-2 years"}
            }
        ]
    },

    "SBI Life Insurance": {
        "claim_settlement_ratio": 98.39,
        "products": [
            {
                "name": "SBI Protection Plan",
                "type": "term",
                "coverage": {
                    "death_benefit": True,
                    "critical_illness_cover": False,
                    "hospitalization_cover": True
                },
                "premium": {
                    "mode": ["yearly", "monthly"],
                    "variable": True
                },
                "tenure": {"min": 5, "max": 80},
                "eligibility": {"min_age": 18, "max_age": 65},
                "waiting_period": {
                    "initial": "30-45 days",
                    "critical_illness": "1-2 years",
                    "survival_period": "14 days"
                }
            },
            {
                "name": "SBI Savings Plan",
                "type": "savings",
                "coverage": {"death_benefit": True},
                "premium": {"mode": ["yearly", "monthly"], "variable": True},
                "tenure": {"min": 10, "max": 30},
                "eligibility": {"min_age": 0.1, "max_age": 60},
                "waiting_period": {"initial": "30-45 days"}
            },
            {
                "name": "SBI Wealth Creation Plan",
                "type": "investment",
                "coverage": {"death_benefit": True},
                "premium": {"mode": ["yearly", "monthly"], "variable": True},
                "tenure": {"min": 10, "max": 40},
                "eligibility": {"min_age": 18, "max_age": 65},
                "waiting_period": {"initial": "30-45 days"}
            },
            {
                "name": "SBI Retirement Plan",
                "type": "retirement",
                "coverage": {"death_benefit": True, "pension_income": True},
                "premium": {"mode": ["yearly", "monthly"], "variable": True},
                "tenure": {"min": 10, "max": 40},
                "eligibility": {"min_age": 18, "max_age": 65},
                "waiting_period": {"initial": "30-45 days"}
            }
        ]
    },

    "Axis Max Life Insurance": {
        "claim_settlement_ratio": 99.70,
        "products": [
            {
                "name": "Axis Max Term Plan",
                "type": "term",
                "coverage": {
                    "death_benefit": True,
                    "critical_illness_rider": True,
                    "income_protection": True,
                    "sum_assured_min": 2500000,
                    "sum_assured_max": "no_limit"
                },
                "premium": {
                    "mode": ["monthly", "quarterly", "semi-annual", "annual"],
                    "options": ["regular", "limited", "till_60", "single"]
                },
                "tenure": {"min": 10, "max": 82},
                "eligibility": {"min_age": 18, "max_age": 65, "max_maturity_age": 100},
                "waiting_period": {
                    "free_look": "15-30 days",
                    "claim_process": "standard (no fixed waiting period)"
                }
            },
            {
                "name": "Axis Max TROP Plan",
                "type": "return_of_premium",
                "coverage": {"death_benefit": True, "premium_return": True},
                "premium": {
                    "mode": ["monthly", "quarterly", "semi-annual", "annual"],
                    "options": ["regular", "limited", "single"]
                },
                "tenure": {"min": 10, "max": 50},
                "eligibility": {"min_age": 18, "max_age": 60, "max_maturity_age": 85},
                "waiting_period": {"free_look": "15-30 days"}
            },
            {
                "name": "Axis Max Savings Plan",
                "type": "savings",
                "coverage": {"death_benefit": True, "investment_component": True},
                "premium": {
                    "mode": ["monthly", "quarterly", "semi-annual", "annual"],
                    "variable": True
                },
                "tenure": {"min": 10, "max": 30},
                "eligibility": {"min_age": 18, "max_age": 60, "max_maturity_age": 85},
                "waiting_period": {"free_look": "15-30 days"}
            }
        ]
    },

    "Kotak Life Insurance": {
        "plans": ["Kotak Term Plan", "Kotak Guaranteed Savings Plan", "Kotak e-Invest"],
        "coverage": {
            "sum_assured": "Varies by plan, paid to nominee on death",
            "maturity_benefit": "Available in savings & investment plans",
            "riders": ["Critical Illness Cover", "Accidental Death Benefit"]
        },
        "premium": {
            "payment_options": ["Single", "Monthly", "Multi-year"],
            "factors": ["Sum Assured", "Policy Tenure", "Entry Age", "Health Status"]
        },
        "tenure": {
            "policy_duration": "5 years to long-term (up to 99-100 years maturity)",
            "maturity_age": "Up to 99 or 100 years"
        },
        "eligibility": {
            "entry_age": "18 to ~65 years depending on plan",
            "health": "Medical history and health status required"
        },
        "csr": "Customer Service handled by Kotak CSRs; claim ratio not explicitly stated",
        "waiting_period": {
            "free_look": "15 to 30 days",
            "health_related": "30-day waiting period for certain illnesses (varies by policy)"
        }
    },

    "HDFC ERGO": {
        "plans": ["Health Insurance (Optima Secure, Health Suraksha)", "General Insurance"],
        "coverage": {
            "sum_insured": "₹5 lakhs to ₹2 crores",
            "options": ["Individual", "Family Floater"],
            "specific_illnesses": "Covers illnesses like internal tumors, cysts (after waiting period)"
        },
        "premium": {
            "payment_structure": ["Variable, based on age, location, sum insured, policy type"],
            "installments": "No-cost installment options available"
        },
        "tenure": {"policy_duration": "1, 2, or 3 years (flexible)"},
        "eligibility": {
            "entry_age": "18+ years for adults; dependent limits vary by plan",
            "pre_existing_conditions": "Covered after waiting period, disclosure required"
        },
        "csr": "98.59% (2023-24)",
        "waiting_period": {
            "initial": "30 days (excluding accidents)",
            "specific_illnesses": "24 months for listed illnesses/surgeries",
            "pre_existing": "36 to 48 months",
            "enhancements": "Fresh exclusions apply to increased sum insured"
        }
    },

    "LIC India": {
        "plans": ["LIC New Tech-Term", "LIC New Jeevan Amar", "LIC Digi Term"],
        "coverage": {"death_benefit": "Lump-sum paid to nominee upon death of policyholder"},
        "premium": {
            "payment_options": ["Single", "Limited", "Regular"],
            "payment_modes": ["Yearly", "Half-yearly"],
            "factors": ["Age", "Gender", "Smoking status", "Policy term", "Sum assured"]
        },
        "tenure": {"policy_duration": "10 to 40 years"},
        "eligibility": {
            "entry_age": "Minimum 18 years, maximum varies by plan (e.g., up to 65 years)",
            "maturity_age": "Around 75 to 80 years depending on plan"
        },
        "csr": "98.65% (FY 2024-25, Policybazaar report)",
        "waiting_period": {
            "grace_period": "30 days for missed premiums (policy remains in force)",
            "claims": "Specific waiting periods may apply depending on benefit"
        }
    },

    "Aditya Birla Sun Life Insurance": {
        "plans": ["Term Insurance Plans (e.g., ABSLI Super Term Plan)", "Savings Plans", "Income Plans"],
        "coverage": {
            "sum_assured": "Varies by plan; minimum a few lakhs, no upper limit for some products"
        },
        "premium": {
            "payment_options": ["Single Pay", "Limited Pay", "Regular Pay"],
            "premium_paying_terms": ["5, 10, 15 years (limited)", "Regular for policy term"]
        },
        "tenure": {"policy_term": "10 to 40+ years depending on plan"},
        "eligibility": {
            "entry_age": "Minimum 4 years to 18 years depending on plan; maximum varies",
            "criteria": ["Income", "Health status", "Plan-specific requirements"]
        },
        "csr": "98.65% (FY 2024-25, Policybazaar report)",
        "waiting_period": {
            "general": "Varies by plan; standard waiting periods apply",
            "forfeiture": "Policy may lapse if premiums are not paid within grace period",
            "revival": "Lapsed policies can be revived by paying outstanding premiums with interest within the revival window"
        }
    }
}
