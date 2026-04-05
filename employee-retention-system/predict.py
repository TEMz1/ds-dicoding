import pickle
import numpy as np
import pandas as pd
import sys

# ─────────────────────────────────────────────────────────────────────────────
# 0. CONSTANTS & CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
MODEL_PATH = "model/attrition_model.pkl"
FEAT_PATH  = "model/feature_columns.pkl"
THRESH_PATH = "model/threshold.pkl"

RISK_HIGH_THRESHOLD = 0.70
LOW_INCOME_BENCHMARK = 3000

# ─────────────────────────────────────────────────────────────────────────────
# 1. UTILITY FUNCTIONS (INPUT VALIDATION)
# ─────────────────────────────────────────────────────────────────────────────
def get_int_input(prompt, min_val=None, max_val=None):
    """Safely get integer input within a specific range."""
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or \
               (max_val is not None and val > max_val):
                print(f"  ⚠ Please enter a number between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("  ⚠ Invalid input! Please enter a numeric value.")

def get_binary_input(prompt):
    """Safely get yes/no input."""
    while True:
        val = input(prompt).strip().lower()
        if val in ['yes', 'y']: return 1
        if val in ['no', 'n']: return 0
        print("  ⚠ Please answer with 'yes' or 'no'.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. LOAD SAVED ARTIFACTS
# ─────────────────────────────────────────────────────────────────────────────
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(FEAT_PATH, "rb") as f:
        feature_columns = pickle.load(f)
    with open(THRESH_PATH, "rb") as f:
        threshold = pickle.load(f)
    
    print(f"✓ System Ready | Threshold: {threshold:.3f}\n")
except FileNotFoundError as e:
    print(f"❌ Critical Error: System artifacts not found!")
    print(f"   Missing file: {e.filename}")
    print("   Ensure 'model/' folder contains: attrition_model.pkl, feature_columns.pkl, threshold.pkl")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# 3. USER INTERFACE
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 55)
print("          HR ATTRITION PREDICTION SYSTEM v3.0")
print("=" * 55)

age                 = get_int_input("Age (18-65): ", 18, 65)
monthly_income      = get_int_input("Monthly Income ($): ", 500, 20000)
total_working_years = get_int_input("Total Working Years (0-40): ", 0, 40)
job_level           = get_int_input("Job Level (1-5): ", 1, 5)
stock_option        = get_int_input("Stock Option Level (0-3): ", 0, 3)
job_involvement     = get_int_input("Job Involvement (1-4): ", 1, 4)
job_satisfaction    = get_int_input("Job Satisfaction (1-4): ", 1, 4)
env_satisfaction    = get_int_input("Environment Satisfaction (1-4): ", 1, 4)
overtime_val        = get_binary_input("Does the employee work OverTime? (yes/no): ")

# ─────────────────────────────────────────────────────────────────────────────
# 4. DATA PREPROCESSING & ROBUST ENCODING
# ─────────────────────────────────────────────────────────────────────────────
# Maksudnya: Kolom yang nggak ditanya, diisi nilai Median agar prediksi akurat
defaults = {
    'Age': 36, 'BusinessTravel': 2, 'DailyRate': 817, 'Department': 1,
    'DistanceFromHome': 7, 'Education': 3, 'EducationField': 2,
    'EnvironmentSatisfaction': 3, 'Gender': 1, 'HourlyRate': 65,
    'JobInvolvement': 3, 'JobLevel': 2, 'JobRole': 5, 'JobSatisfaction': 3,
    'MaritalStatus': 1, 'MonthlyIncome': 4903, 'MonthlyRate': 14201,
    'NumCompaniesWorked': 2, 'OverTime': 0, 'PercentSalaryHike': 14,
    'PerformanceRating': 3, 'RelationshipSatisfaction': 3,
    'StockOptionLevel': 1, 'TotalWorkingYears': 10, 'TrainingTimesLastYear': 3,
    'WorkLifeBalance': 3, 'YearsAtCompany': 5, 'YearsInCurrentRole': 3,
    'YearsSinceLastPromotion': 1, 'YearsWithCurrManager': 3, 'AgeGroup': 1
}

# Gabungkan input user ke dalam satu dictionary
user_input_map = {
    "Age": age,
    "MonthlyIncome": monthly_income,
    "TotalWorkingYears": total_working_years,
    "JobLevel": job_level,
    "StockOptionLevel": stock_option,
    "JobInvolvement": job_involvement,
    "JobSatisfaction": job_satisfaction,
    "EnvironmentSatisfaction": env_satisfaction,
    "OverTime": overtime_val,
    # Jika model kamu punya kolom One-Hot, kita isi juga:
    "OverTime_Yes": overtime_val,
    "OverTime_No": 1 - overtime_val
}

# Timpa nilai default dengan input user
final_features = {**defaults, **user_input_map}

# Buat DataFrame dan pastikan urutan kolom SAMA PERSIS dengan saat training
input_data = pd.DataFrame([final_features])

# CRITICAL: Pastikan semua kolom hasil training ada (jika ada yang kurang, isi 0)
for col in feature_columns:
    if col not in input_data.columns:
        input_data[col] = 0

input_data = input_data[feature_columns]

# ─────────────────────────────────────────────────────────────────────────────
# 5. PREDICTION & CONSISTENT RISK LEVELING
# ─────────────────────────────────────────────────────────────────────────────
probability = model.predict_proba(input_data)[0][1]

# Gunakan variabel 'threshold' yang di-load dari pickle agar sinkron
if probability >= RISK_HIGH_THRESHOLD:
    risk_level = "HIGH   🔴"
elif probability >= threshold:
    risk_level = "MEDIUM 🟡"
else:
    risk_level = "LOW    🟢"

# ─────────────────────────────────────────────────────────────────────────────
# 6. FINAL REPORT
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("                ANALYSIS REPORT")
print("=" * 55)
print(f"Resign Probability : {probability:.1%}")
print(f"Risk Level         : {risk_level}")
# Final Decision sekarang otomatis mengikuti threshold hasil riset kamu
print(f"Final Decision     : {'⚠️  AT RISK' if probability >= threshold else '✅ STABLE'}")
print("-" * 55)

if probability >= threshold:
    print("KEY RISK FACTORS:")
    if monthly_income < LOW_INCOME_BENCHMARK: print("- Salary: Below internal benchmark.")
    if stock_option == 0:     print("- Retention: No stock option incentives.")
    if overtime_val == 1:     print("- Workload: Active Overtime detected.")
    if job_satisfaction <= 2: print("- Engagement: Critical satisfaction level.")
    
    print("\n[ MANAGEMENT ADVICE ]")
    print("• Conduct a 'Stay Interview' to identify specific pain points.")
    print("• Review compensation and non-financial rewards.")
else:
    print("STATUS: Low flight risk. Maintain current engagement.")

print("=" * 55)