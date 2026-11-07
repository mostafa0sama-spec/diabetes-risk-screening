import streamlit as st
import joblib
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="CDC Diabetes Risk Screening Tool",
    page_icon="🩺",
    layout="centered"
)

# Load the trained model bundle
@st.cache_resource
def load_model():
    return joblib.load("diabetes_screening_model.joblib")

bundle = load_model()
model = bundle["model"]
features = bundle["features"]
threshold = bundle["threshold"]

# App Title & Description
st.title("🩺 CDC Diabetes Risk Screening Tool")
st.write(
    "Answer the following health and lifestyle questions to assess your estimated risk "
    "of prediabetes or diabetes."
)

# Medical Disclaimer (Mandatory Requirement)
st.warning(
    "⚠️ **Disclaimer:** This tool is intended for early population-level screening purposes only. "
    "It is not a medical diagnosis or a substitute for professional clinical advice and lab tests."
)

with st.form("screening_form"):
    st.subheader("Health & Demographic Indicators")
    
    # 1. GenHlth
    gen_hlth_map = {
        "Excellent (1)": 1,
        "Very Good (2)": 2,
        "Good (3)": 3,
        "Fair (4)": 4,
        "Poor (5)": 5
    }
    gen_hlth_choice = st.selectbox(
        "Would you say that in general your health is:",
        list(gen_hlth_map.keys()),
        index=2
    )
    gen_hlth_val = gen_hlth_map[gen_hlth_choice]

    # 2. BMI
    bmi_val = st.slider(
        "Body Mass Index (BMI):",
        min_value=12.0,
        max_value=60.0,
        value=25.0,
        step=0.5
    )

    # 3. Age
    age_categories = {
        "Age 18 - 24": 1,
        "Age 25 - 29": 2,
        "Age 30 - 34": 3,
        "Age 35 - 39": 4,
        "Age 40 - 44": 5,
        "Age 45 - 49": 6,
        "Age 50 - 54": 7,
        "Age 55 - 59": 8,
        "Age 60 - 64": 9,
        "Age 65 - 69": 10,
        "Age 70 - 74": 11,
        "Age 75 - 79": 12,
        "Age 80 or older": 13
    }
    age_choice = st.selectbox("Age Category:", list(age_categories.keys()), index=6)
    age_val = age_categories[age_choice]

    # 4. DiffWalk
    diff_walk_choice = st.radio(
        "Do you have serious difficulty walking or climbing stairs?",
        ["No", "Yes"],
        horizontal=True
    )
    diff_walk_val = 1 if diff_walk_choice == "Yes" else 0

    # 5. HeartDiseaseorAttack
    heart_choice = st.radio(
        "Have you ever had coronary heart disease (CHD) or a heart attack (myocardial infarction)?",
        ["No", "Yes"],
        horizontal=True
    )
    heart_val = 1 if heart_choice == "Yes" else 0

    # 6. PhysHlth (تم تصريح المعاملات بوضوح لتفادي مشاكل الأقواس)
    phys_hlth_val = st.slider(
        "For how many days during the past 30 days was your physical health not good (due to illness or injury)?",
        min_value=0,
        max_value=30,
        value=0,
        step=1
    )

    # 7. Income
    income_categories = {
        "Less than $10,000": 1,
        "$10,000 to $15,000": 2,
        "$15,000 to $20,000": 3,
        "$20,000 to $25,000": 4,
        "$25,000 to $35,000": 5,
        "$35,000 to $50,000": 6,
        "$50,000 to $75,000": 7,
        "$75,000 or more": 8
    }
    income_choice = st.selectbox(
        "Annual Household Income Level:",
        list(income_categories.keys()),
        index=4
    )
    income_val = income_categories[income_choice]

    submit = st.form_submit_button("Assess Diabetes Risk")

if submit:
    user_data = {
        "GenHlth": gen_hlth_val,
        "BMI": bmi_val,
        "Age": age_val,
        "DiffWalk": diff_walk_val,
        "HeartDiseaseorAttack": heart_val,
        "PhysHlth": phys_hlth_val,
        "Income": income_val
    }
    input_df = pd.DataFrame([user_data])[features]
    prob = model.predict_proba(input_df)[0, 1]
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("Estimated Risk Probability", f"{prob * 100:.1f}%")
    
    if prob >= threshold:
        col2.error("Risk Level: HIGH 🔴")
        st.write("### Recommended Next Steps:")
        st.write("- It is strongly advised to schedule a consultation with a healthcare provider.")
        st.write("- Consider taking a fasting blood glucose test and a Glycated Hemoglobin (HbA1c) test.")
        st.write("- Discuss lifestyle modifications, including blood pressure and BMI management.")
    else:
        col2.success("Risk Level: LOW 🟢")
        st.write("### Recommended Next Steps:")
        st.write("- Current survey metrics indicate low risk.")
        st.write("- Maintain a balanced nutritional diet and regular physical activity.")
