import os
import pickle
import sqlite3
import hashlib
import streamlit as st
from streamlit_option_menu import option_menu

# Security functions
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# DB Management functions
conn = sqlite3.connect('data.db')  # Ensure this path is correct
c = conn.cursor()

# DB Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable504(username TEXT, email TEXT, password TEXT)')

def add_userdata(username, email, password):
    c.execute('INSERT INTO userstable504(username, email, password) VALUES (?, ?, ?)', (username, email, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable504 WHERE username = ? AND password = ?', (username, password))
    return c.fetchall()

# ----------------------- Streamlit Configuration -----------------------
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

# ----------------------- Main Code -----------------------

# Initialize Session State for logged-in status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Loading pre-trained models
diabetes_model = pickle.load(open('C:/Users/chakr/Desktop/multiple Disease prediction system/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('C:/Users/chakr/Desktop/multiple Disease prediction system/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('C:/Users/chakr/Desktop/multiple Disease prediction system/parkinsons_model.sav', 'rb'))

# ----------------------- Login Page -----------------------
if not st.session_state.logged_in:
    # Sidebar with login options
    st.sidebar.image("C:/Users/chakr/Desktop/multiple Disease prediction system/login.jpg", use_container_width=True)
    menu = ["Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Login":
        st.title("Multiple Disease Prediction System")
        st.subheader("Login Section")
        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            hashed_pswd = make_hashes(password)
            result = login_user(username, hashed_pswd)
            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Logged In as {username}")
                st.rerun()  # Reload the page and redirect to the disease prediction page
            else:
                st.error("Invalid Username or Password")

    elif choice == "SignUp":
        st.title("Multiple Disease Prediction System")
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        email = st.text_input("Email")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            add_userdata(new_user, email, make_hashes(new_password))
            st.success("Account created successfully!")
            st.info("Go to Login to continue.")
        
# ----------------------- Disease Prediction Page -----------------------
else:
    # Sidebar navigation menu
    with st.sidebar:
        selected = option_menu('Multiple Disease Prediction System',
                               ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
                               menu_icon='hospital-fill',
                               icons=['activity', 'heart', 'person'],
                               default_index=0)

    # Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction using ML')
        st.image("C:/Users/chakr/Desktop/multiple Disease prediction system/diabetes.jpg", use_container_width=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')
        with col2:
            Glucose = st.text_input('Glucose Level')
        with col3:
            BloodPressure = st.text_input('Blood Pressure value')
        with col1:
            SkinThickness = st.text_input('Skin Thickness value')
        with col2:
            Insulin = st.text_input('Insulin Level')
        with col3:
            BMI = st.text_input('BMI value')
        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
        with col2:
            Age = st.text_input('Age of the Person')

        if st.button('Diabetes Test Result'):
            user_input = [float(x) for x in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                                             BMI, DiabetesPedigreeFunction, Age]]
            diab_prediction = diabetes_model.predict([user_input])
            diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
            st.success(diab_diagnosis)

    # Heart Disease Prediction Page
    elif selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')
        st.image("C:/Users/chakr/Desktop/multiple Disease prediction system/Heart_Disease.jpg", use_container_width=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.text_input('Age')
        with col2:
            sex = st.text_input('Sex')
        with col3:
            cp = st.text_input('Chest Pain types')
        with col1:
            trestbps = st.text_input('Resting Blood Pressure')
        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')
        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')
        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')
        with col3:
            exang = st.text_input('Exercise Induced Angina')
        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')
        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')
        with col3:
            ca = st.text_input('Major vessels colored by flourosopy')
        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        if st.button('Heart Disease Test Result'):
            user_input = [float(x) for x in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang,
                                             oldpeak, slope, ca, thal]]
            heart_prediction = heart_disease_model.predict([user_input])
            heart_diagnosis = 'The person is having heart disease' if heart_prediction[0] == 1 else 'The person does not have any heart disease'
            st.success(heart_diagnosis)

    # Parkinson's Prediction Page
    elif selected == "Parkinsons Prediction":
        st.title("Parkinson's Disease Prediction using ML")
        st.image("C:/Users/chakr/Desktop/multiple Disease prediction system/parkinson.jpg", use_container_width=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            fo = st.text_input('MDVP:Fo(Hz)')
        with col2:
            fhi = st.text_input('MDVP:Fhi(Hz)')
        with col3:
            flo = st.text_input('MDVP:Flo(Hz)')
        with col4:
            Jitter_percent = st.text_input('MDVP:Jitter(%)')
        with col5:
            Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
        with col1:
            RAP = st.text_input('MDVP:RAP')
        with col2:
            PPQ = st.text_input('MDVP:PPQ')
        with col3:
            DDP = st.text_input('Jitter:DDP')
        with col4:
            Shimmer = st.text_input('MDVP:Shimmer')
        with col5:
            Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
        with col1:
            APQ3 = st.text_input('Shimmer:APQ3')
        with col2:
            APQ5 = st.text_input('Shimmer:APQ5')
        with col3:
            APQ = st.text_input('MDVP:APQ')
        with col4:
            DDA = st.text_input('Shimmer:DDA')
        with col5:
            NHR = st.text_input('NHR')
        with col1:
            HNR = st.text_input('HNR')
        with col2:
            RPDE = st.text_input('RPDE')
        with col3:
            DFA = st.text_input('DFA')
        with col4:
            spread1 = st.text_input('spread1')
        with col5:
            spread2 = st.text_input('spread2')
        with col1:
            D2 = st.text_input('D2')
        with col2:
            PPE = st.text_input('PPE')

        if st.button("Parkinson's Test Result"):
            user_input = [float(x) for x in [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer,
                                             Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]]
            parkinsons_prediction = parkinsons_model.predict([user_input])
            parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"
            st.success(parkinsons_diagnosis)

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()  # This will rerun the script and redirect to the login page
