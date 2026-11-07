# Diabetes Risk Screening Tool

An interactive web application and machine learning model that predicts diabetes risk from population health indicators using the CDC Diabetes dataset (~250K records).

## Problem Framing & Goal
Millions of people live with undiagnosed diabetes or prediabetes. The business goal is population-level early risk screening using a short survey, optimizing specifically for **Recall** to avoid missing at-risk patients (minimizing False Negatives).

## Model Results (Test Set)
| Model | Recall | Precision | ROC-AUC | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline (Majority Class)** | 0.00 | 0.00 | 0.50 | 0.00 |
| **Logistic Regression** | 0.73 | 0.31 | 0.82 | 0.44 |
| **Random Forest** | 0.77 | 0.31 | 0.83 | 0.45 |
| **HistGradientBoosting (Best - 7 Features)** | **0.86** | 0.25 | **0.83** | 0.39 |

## Selected Top 7 Features
1. `GenHlth` (General Health)
2. `BMI` (Body Mass Index)
3. `Age` (Age Category)
4. `DiffWalk` (Difficulty Walking)
5. `HeartDiseaseorAttack`
6. `PhysHlth` (Physical Health Days)
7. `Income` (Household Income Level)

## How to Run Locally
1. Clone this repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
