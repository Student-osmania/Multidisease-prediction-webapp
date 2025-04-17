import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import os
import sqlite3
import hashlib

# ---------------------- Security Functions ---------------------- #
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# ---------------------- DB Management ---------------------- #
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable504(username TEXT,email TEXT,password TEXT)')

def add_userdata(username, email, password):
    c.execute('INSERT INTO userstable504(username,email,password) VALUES (?,?,?)', (username, email, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable504 WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

# ---------------------- Page Config ---------------------- #
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

# ---------------------- Session State ---------------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------- Load Models ---------------------- #
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')
diabetes_model = pickle.load(open(os.path.join(MODEL_PATH, 'diabetes_model.sav'), 'rb'))
heart_disease_model = pickle.load(open(os.path.join(MODEL_PATH, 'heart_model.sav'), 'rb'))
parkinsons_model = pickle.load(open(os.path.join(MODEL_PATH, 'parkinsons_model.sav'), 'rb'))

# ---------------------- Login and SignUp ---------------------- #
if not st.session_state.logged_in:
    st.sidebar.image("app/assets/login.jpg", use_container_width=True)
    menu = ["Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.title("Multiple Disease Prediction System")
        st.subheader("Login Section")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            hashed_pswd = make_hashes(password)
            result = login_user(username, hashed_pswd)
            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Logged In as {username}")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    elif choice == "SignUp":
        st.title("Multiple Disease Prediction System")
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        email = st.text_input("Email")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, email, make_hashes(new_password))
            st.success("Account created successfully!")
            st.info("Go to Login to continue.")

# ---------------------- Disease Prediction ---------------------- #
else:
    with st.sidebar:
        selected = option_menu(
            'Multiple Disease Prediction System',
            ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
            menu_icon='hospital-fill',
            icons=['activity', 'heart', 'person'],
            default_index=0
        )

    if selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction using ML')
        st.image("app/assets/diabetes.jpg", use_container_width=True)

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
            try:
                user_input = [float(Pregnancies), float(Glucose), float(BloodPressure),
                              float(SkinThickness), float(Insulin), float(BMI),
                              float(DiabetesPedigreeFunction), float(Age)]
                prediction = diabetes_model.predict([user_input])
                st.success("The person is diabetic" if prediction[0] == 1 else "The person is not diabetic")
            except:
                st.error("Please enter valid numerical inputs.")

    elif selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')
        st.image("app/assets/Heart_Disease.jpg", use_container_width=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')
            cp = st.text_input('Chest Pain types')
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
            thalach = st.text_input('Maximum Heart Rate achieved')
            slope = st.text_input('Slope of the peak exercise ST segment')

        with col2:
            sex = st.text_input('Sex')
            trestbps = st.text_input('Resting Blood Pressure')
            restecg = st.text_input('Resting Electrocardiographic results')
            exang = st.text_input('Exercise Induced Angina')
            ca = st.text_input('Major vessels colored by flourosopy')

        with col3:
            chol = st.text_input('Serum Cholestoral in mg/dl')
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')
            oldpeak = st.text_input('ST depression induced by exercise')

        if st.button('Heart Disease Test Result'):
            try:
                user_input = [float(age), float(sex), float(cp), float(trestbps), float(chol),
                              float(fbs), float(restecg), float(thalach), float(exang),
                              float(oldpeak), float(slope), float(ca), float(thal)]
                prediction = heart_disease_model.predict([user_input])
                st.success("The person has heart disease" if prediction[0] == 1 else "The person does not have heart disease")
            except:
                st.error("Please enter valid numerical inputs.")

    elif selected == "Parkinsons Prediction":
        st.title("Parkinson's Disease Prediction using ML")
        st.image("app/assets/parkinson.jpg", use_container_width=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            fo = st.text_input('MDVP:Fo(Hz)')
            fhi = st.text_input('MDVP:Fhi(Hz)')
            flo = st.text_input('MDVP:Flo(Hz)')
            Jitter_percent = st.text_input('MDVP:Jitter(%)')
            RAP = st.text_input('MDVP:RAP')
            DDP = st.text_input('Jitter:DDP')
            Shimmer = st.text_input('MDVP:Shimmer')
            APQ = st.text_input('MDVP:APQ')
            DDA = st.text_input('Shimmer:DDA')
            NHR = st.text_input('NHR')

        with col2:
            Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
            PPQ = st.text_input('MDVP:PPQ')
            Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
            APQ3 = st.text_input('Shimmer:APQ3')
            APQ5 = st.text_input('Shimmer:APQ5')
            HNR = st.text_input('HNR')
            RPDE = st.text_input('RPDE')
            DFA = st.text_input('DFA')
            spread1 = st.text_input('spread1')
            spread2 = st.text_input('spread2')

        with col3:
            D2 = st.text_input('D2')
            PPE = st.text_input('PPE')

        if st.button("Parkinson's Test Result"):
            try:
                user_input = [float(fo), float(fhi), float(flo), float(Jitter_percent), float(Jitter_Abs),
                              float(RAP), float(PPQ), float(DDP), float(Shimmer), float(Shimmer_dB),
                              float(APQ3), float(APQ5), float(APQ), float(DDA), float(NHR), float(HNR),
                              float(RPDE), float(DFA), float(spread1), float(spread2), float(D2), float(PPE)]
                prediction = parkinsons_model.predict([user_input])
                st.success("The person has Parkinson's disease" if prediction[0] == 1 else "The person does not have Parkinson's disease")
            except:
                st.error("Please enter valid numerical inputs.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
