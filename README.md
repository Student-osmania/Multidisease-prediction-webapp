# Multi-Disease Prediction Web App

This is a web application that predicts various diseases such as **Diabetes**, **Heart Disease**, and **Parkinson's Disease** based on user input. The app uses machine learning models to predict the likelihood of having these diseases based on the provided health metrics.

## Features

- **User Authentication:** Users can log in or sign up to access the app.
- **Disease Prediction:** Users can predict the likelihood of having:
  - Diabetes
  - Heart Disease
  - Parkinson’s Disease
- **Machine Learning Models:** The app uses pre-trained machine learning models for each disease prediction.

## Technologies Used

- **Python**
  - **Streamlit**: For building the interactive web application.
  - **Pickle**: For loading pre-trained machine learning models.
  - **SQLite**: For storing user data and authentication.
  - **Hashlib**: For password encryption.
  - **Scikit-learn**: For the machine learning models.
  - **Pandas, NumPy**: For data manipulation.
- **Libraries**
  - **Streamlit-option-menu**: For building the sidebar navigation menu.

## Setup Instructions

### Prerequisites

- Python 3.x
- Streamlit library
- SQLite library
- Scikit-learn, Pandas, NumPy, and other dependencies.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/your-repository.git
2.Navigate to the project directory:

   ```bash
  cd your-repository
```
3.Install the necessary libraries:

```bash
  pip install -r requirements.txt
```

4.Ensure you have the machine learning models (diabetes_model.sav, heart_model.sav, parkinsons_model.sav) placed in the correct path within the repository. These models can be trained beforehand or you can download pre-trained models.

5.Run the app:

```bash
  streamlit run app/streamlit_app.py
```
### Files Structure

multi-disease-prediction-webapp/
│
├── app/
│   ├── assets/                   # Images for the app
│   ├── streamlit_app.py          # The main app file
│
├── models/                       # Folder to store machine learning models
│   ├── diabetes_model.sav        # Pre-trained diabetes prediction model
│   ├── heart_model.sav           # Pre-trained heart disease model
│   ├── parkinsons_model.sav      # Pre-trained Parkinson's disease model
│
├── data.db                       # SQLite database for storing user data
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation

### Pre-trained Models
The app uses the following pre-trained models:

**Diabetes Prediction Model**: A machine learning model to predict if a person is diabetic based on various health parameters.

**Heart Disease Prediction Model**: A model that predicts the likelihood of heart disease based on user input related to heart health.

**Parkinson’s Disease Prediction Model**: A model to predict whether a person has Parkinson's disease based on certain medical metrics.

You can upload your own models, or train them using datasets from sources like Kaggle.

### Running the Application
Once the app is running, it will be accessible in your browser (usually at http://localhost:8501/). The main features are:

**Login/SignUp**: Users can create an account or log into the app using their credentials. All passwords are hashed for security.

**Disease Prediction**: After logging in, users can navigate through the sidebar and select a disease for prediction:

1.Diabetes Prediction: Based on factors like glucose level, age, BMI, etc.
2.Heart Disease Prediction: Based on heart health metrics like cholesterol, blood pressure, etc.
3.Parkinson’s Disease Prediction: Based on speech and movement-related features.

**App Workflow**
Login/SignUp: The app checks user credentials stored in the SQLite database. If login is successful, the user can proceed to the disease prediction pages.

**Prediction Pages:**
For each disease, the user will fill out a form with health-related inputs.After clicking the "Predict" button, the app will use the respective pre-trained model to predict the disease.

**Results:** The app will display the prediction result (whether the user has the disease or not) and the corresponding message.
