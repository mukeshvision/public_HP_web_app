import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import time

# Set page configuration
st.set_page_config(page_title="Health Prediction Hub",
                   layout="wide",
                   page_icon="�")

# --- Load Machine Learning Models ---
working_dir = os.path.dirname(os.path.abspath(__file__))

diabetes_model_path = os.path.join(working_dir, 'saved_models', 'diabetes_model.sav')
heart_disease_model_path = os.path.join(working_dir, 'saved_models', 'heart_disease_model.sav')
parkinsons_model_path = os.path.join(working_dir, 'saved_models', 'parkinsons_model.sav')

try:
    diabetes_model = pickle.load(open(diabetes_model_path, 'rb'))
    heart_disease_model = pickle.load(open(heart_disease_model_path, 'rb'))
    parkinsons_model = pickle.load(open(parkinsons_model_path, 'rb'))
except FileNotFoundError:
    st.error("🚨 **Error:** One or more machine learning model files were not found.")
    st.error(f"Please ensure `diabetes_model.sav`, `heart_disease_model.sav`, and `parkinsons_model.sav` are located in the `{working_dir}/saved_models/` directory.")
    st.stop()

# --- Sidebar Navigation ---
with st.sidebar:
    st.title('🩺 **Wellness Hub** 🧭')
    selected = option_menu('**Wellness Check:**',
                           ['GlycoScan 🩸',
                            'CardioFlow ❤️',
                            'MotionSync ✨'],
                           menu_icon='hospital-fill',
                           icons=['bandaid-fill', 'heart-pulse-fill', 'person-fill'],
                           default_index=0,
                           styles={
                               "container": {"padding": "5!important", "background-color": "#0C2D48", "border-radius": "10px"},
                               "icon": {"color": "#BBE1FA", "font-size": "25px"},
                               "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#1A5276", "color": "#BBE1FA", "border-radius": "8px"},
                               "nav-link-selected": {"background-color": "#2E8BC0", "color": "#FFFFFF", "border-radius": "8px"},
                           }
                           )


# --- GlycoScan (Diabetes Prediction) Page ---
if selected == 'GlycoScan 🩸':
    st.title('🩸 **GlycoScan: Diabetes Risk Analysis**')
    st.markdown("---")

    st.info("💡 **Instructions:** Please provide the following details to assess your potential risk of Diabetes. Ensure all fields are filled with numerical values.")

    col1, col2, col3 = st.columns(3)

    with col1:
        pregnancies = st.number_input('Number of Pregnancies', min_value=0, max_value=20, value=0, step=1,
                                     help="Total number of times pregnant.")

    with col2:
        glucose = st.number_input('Glucose Level (mg/dL)', min_value=0, max_value=300, value=120, step=1,
                                  help="Plasma glucose concentration (2-hour oral glucose tolerance test).")

    with col3:
        blood_pressure = st.number_input('Blood Pressure (mmHg)', min_value=0, max_value=200, value=70, step=1,
                                        help="Diastolic blood pressure reading.")

    with col1:
        skin_thickness = st.number_input('Skin Thickness (mm)', min_value=0, max_value=100, value=20, step=1,
                                        help="Triceps skin fold thickness.")

    with col2:
        insulin = st.number_input('Insulin Level (mu U/ml)', min_value=0, max_value=900, value=80, step=1,
                                 help="2-Hour serum insulin.")

    with col3:
        bmi = st.number_input('BMI (Body Mass Index)', min_value=0.0, max_value=70.0, value=25.0, step=0.1,
                             help="Body Mass Index (weight in kg / height in m^2).")

    with col1:
        diabetes_pedigree_function = st.number_input('Diabetes Pedigree Function', min_value=0.0, max_value=2.5, value=0.5, step=0.01,
                                                    help="A genetic score indicating diabetes likelihood based on family history.")

    with col2:
        age = st.number_input('Age (Years)', min_value=0, max_value=120, value=30, step=1,
                             help="Age of the individual.")

    st.markdown("---")
    diab_diagnosis = ''
    if st.button('✨ **Analyze GlycoScan Result** ✨'):
        with st.spinner('Analyzing data...'):
            time.sleep(1.5)
            try:
                user_input = [pregnancies, glucose, blood_pressure, skin_thickness, insulin,
                              bmi, diabetes_pedigree_function, age]

                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    diab_diagnosis = '⚠️ Based on the provided data, the system indicates a **higher likelihood of Diabetes**. We strongly recommend consulting a healthcare professional for a comprehensive diagnosis and personalized advice.'
                else:
                    diab_diagnosis = '✅ Based on the provided data, the system suggests a **lower likelihood of Diabetes**. Keep up with healthy habits and regular check-ups!'
            except Exception as e:
                diab_diagnosis = f'🚨 An unexpected error occurred during prediction: {e}. Please try again or contact support.'

        if diab_diagnosis:
            st.success(diab_diagnosis)


# --- CardioFlow (Heart Disease Prediction) Page ---
elif selected == 'CardioFlow ❤️':
    st.title('❤️ **CardioFlow: Heart Health Insights**')
    st.markdown("---")

    st.info("💡 **Instructions:** Enter your cardiovascular metrics below to evaluate your potential heart disease risk. All inputs should be numerical.")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input('Age (Years)', min_value=0, max_value=120, value=50, step=1)

    with col2:
        sex = st.number_input('Sex (0: Female, 1: Male)', min_value=0, max_value=1, value=1, step=1)

    with col3:
        cp = st.number_input('Chest Pain Type (0-3)', min_value=0, max_value=3, value=0, step=1,
                             help="Categorical: 0=Typical Angina, 1=Atypical Angina, 2=Non-anginal Pain, 3=Asymptomatic.")

    with col1:
        trestbps = st.number_input('Resting Blood Pressure (mmHg)', min_value=90, max_value=200, value=120, step=1)

    with col2:
        chol = st.number_input('Serum Cholesterol (mg/dL)', min_value=100, max_value=600, value=200, step=1)

    with col3:
        fbs = st.number_input('Fasting Blood Sugar (> 120 mg/dL? 0:No, 1:Yes)', min_value=0, max_value=1, value=0, step=1)

    with col1:
        restecg = st.number_input('Resting ECG Results (0-2)', min_value=0, max_value=2, value=0, step=1,
                                 help="Categorical: 0=Normal, 1=ST-T wave abnormality, 2=Left ventricular hypertrophy.")

    with col2:
        thalach = st.number_input('Maximum Heart Rate Achieved', min_value=60, max_value=220, value=150, step=1)

    with col3:
        exang = st.number_input('Exercise Induced Angina (0:No, 1:Yes)', min_value=0, max_value=1, value=0, step=1)

    with col1:
        oldpeak = st.number_input('ST Depression by Exercise (relative to rest)', min_value=0.0, max_value=7.0, value=1.0, step=0.1)

    with col2:
        slope = st.number_input('Slope of Peak Exercise ST Segment (0-2)', min_value=0, max_value=2, value=1, step=1,
                               help="Categorical: 0=Upsloping, 1=Flat, 2=Downsloping.")

    with col3:
        ca = st.number_input('Number of Major Vessels colored by Fluoroscopy (0-3)', min_value=0, max_value=3, value=0, step=1)

    with col1:
        thal = st.number_input('Thalassemia (0-2)', min_value=0, max_value=2, value=1, step=1,
                              help="Categorical: 0=Normal, 1=Fixed defect, 2=Reversible defect.")

    st.markdown("---")
    heart_diagnosis = ''
    if st.button('✨ **Evaluate CardioFlow Result** ✨'):
        with st.spinner('Analyzing data...'):
            time.sleep(1.5)
            try:
                user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

                heart_prediction = heart_disease_model.predict([user_input])

                if heart_prediction[0] == 1:
                    heart_diagnosis = '⚠️ Based on the input, the system suggests a **potential presence of Heart Disease**. It is highly recommended to consult a cardiologist for further evaluation and a confirmed diagnosis.'
                else:
                    heart_diagnosis = '✅ Based on the input, the system indicates a **low likelihood of Heart Disease**. Keep up with a heart-healthy lifestyle!'
            except Exception as e:
                heart_diagnosis = f'🚨 An unexpected error occurred during prediction: {e}. Please try again or contact support.'

        if heart_diagnosis:
            st.success(heart_diagnosis)


# --- MotionSync (Parkinson's Prediction) Page ---
elif selected == "MotionSync ✨":
    st.title("🚶 **MotionSync: Parkinson's Assessment**")
    st.markdown("---")

    st.info("💡 **Instructions:** Provide the following voice measurement parameters to help assess the likelihood of Parkinson's disease. All fields require numerical input.")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.number_input('MDVP:Fo(Hz)', min_value=50.0, max_value=700.0, value=150.0, step=0.1,
                            help="Average vocal fundamental frequency.")

    with col2:
        fhi = st.number_input('MDVP:Fhi(Hz)', min_value=50.0, max_value=700.0, value=200.0, step=0.1,
                             help="Maximum vocal fundamental frequency.")

    with col3:
        flo = st.number_input('MDVP:Flo(Hz)', min_value=50.0, max_value=700.0, value=100.0, step=0.1,
                             help="Minimum vocal fundamental frequency.")

    with col4:
        jitter_percent = st.number_input('MDVP:Jitter(%)', min_value=0.0, max_value=1.0, value=0.005, format="%.5f", step=0.00001,
                                         help="Measure of variation in fundamental frequency, expressed as a percentage.")

    with col5:
        jitter_abs = st.number_input('MDVP:Jitter(Abs)', min_value=0.0, max_value=0.001, value=0.00005, format="%.5f", step=0.00001,
                                     help="Absolute measure of variation in fundamental frequency.")

    with col1:
        rap = st.number_input('MDVP:RAP', min_value=0.0, max_value=0.1, value=0.002, format="%.5f", step=0.00001,
                             help="Relative Average Perturbation.")

    with col2:
        ppq = st.number_input('MDVP:PPQ', min_value=0.0, max_value=0.1, value=0.003, format="%.5f", step=0.00001,
                             help="Five-point Period Perturbation Quotient.")

    with col3:
        ddp = st.number_input('Jitter:DDP', min_value=0.0, max_value=0.3, value=0.006, format="%.5f", step=0.00001,
                             help="Average absolute difference of differences between consecutive periods.")

    with col4:
        shimmer = st.number_input('MDVP:Shimmer', min_value=0.0, max_value=0.5, value=0.02, format="%.5f", step=0.0001,
                                  help="Measure of amplitude variation.")

    with col5:
        shimmer_dB = st.number_input('MDVP:Shimmer(dB)', min_value=0.0, max_value=5.0, value=0.2, format="%.2f", step=0.01,
                                     help="Shimmer in decibels.")

    with col1:
        apq3 = st.number_input('Shimmer:APQ3', min_value=0.0, max_value=0.05, value=0.01, format="%.5f", step=0.00001,
                              help="Three-point Amplitude Perturbation Quotient.")

    with col2:
        apq5 = st.number_input('Shimmer:APQ5', min_value=0.0, max_value=0.05, value=0.015, format="%.5f", step=0.00001,
                              help="Five-point Amplitude Perturbation Quotient.")

    with col3:
        apq = st.number_input('MDVP:APQ', min_value=0.0, max_value=0.1, value=0.02, format="%.5f", step=0.00001,
                             help="Overall Amplitude Perturbation Quotient.")

    with col4:
        dda = st.number_input('Shimmer:DDA', min_value=0.0, max_value=0.2, value=0.03, format="%.5f", step=0.00001,
                             help="Average absolute difference of differences between consecutive amplitudes.")

    with col5:
        nhr = st.number_input('NHR', min_value=0.0, max_value=0.5, value=0.1, format="%.5f", step=0.00001,
                             help="Noise-to-Harmonic Ratio.")

    with col1:
        hnr = st.number_input('HNR', min_value=0.0, max_value=40.0, value=20.0, step=0.1,
                             help="Harmonic-to-Noise Ratio.")

    with col2:
        rpde = st.number_input('RPDE', min_value=0.0, max_value=1.0, value=0.5, step=0.01,
                              help="Recurrence Period Density Entropy.")

    with col3:
        dfa = st.number_input('DFA', min_value=0.0, max_value=1.0, value=0.7, step=0.01,
                             help="Detrended Fluctuation Analysis.")

    with col4:
        spread1 = st.number_input('Spread1', min_value=-10.0, max_value=0.0, value=-5.0, step=0.01,
                                 help="Nonlinear dynamic complexity measure (first spread).")

    with col5:
        spread2 = st.number_input('Spread2', min_value=-10.0, max_value=0.0, value=-5.0, step=0.01,
                                 help="Nonlinear dynamic complexity measure (second spread).")

    with col1:
        d2 = st.number_input('D2', min_value=0.0, max_value=5.0, value=2.0, step=0.01,
                            help="Correlation Dimension.")

    with col2:
        ppe = st.number_input('PPE', min_value=0.0, max_value=1.0, value=0.2, step=0.01,
                             help="Pitch Period Entropy.")

    st.markdown("---")
    parkinsons_diagnosis = ''
    if st.button("✨ **Assess MotionSync Result** ✨"):
        with st.spinner('Analyzing data...'):
            time.sleep(1.5)
            try:
                user_input = [fo, fhi, flo, jitter_percent, jitter_abs,
                              rap, ppq, ddp, shimmer, shimmer_dB, apq3, apq5,
                              apq, dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe]

                parkinsons_prediction = parkinsons_model.predict([user_input])

                if parkinsons_prediction[0] == 1:
                    parkinsons_diagnosis = "⚠️ Based on the voice parameters, the system suggests a **positive indication for Parkinson's disease**. It's crucial to consult a neurologist for a definitive diagnosis and treatment plan."
                else:
                    parkinsons_diagnosis = "✅ Based on the voice parameters, the system indicates a **low likelihood of Parkinson's disease**."
            except Exception as e:
                parkinsons_diagnosis = f'🚨 An unexpected error occurred during prediction: {e}. Please try again or contact support.'

        if parkinsons_diagnosis:
            st.success(parkinsons_diagnosis)