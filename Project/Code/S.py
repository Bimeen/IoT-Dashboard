import joblib
import pandas as pd
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
import traceback
import time  # Ensure time module is imported for sleep functionality

# Initialize Firebase Admin SDK
cred = credentials.Certificate("iot-firebase-adminsdk.json")  # Update with your Firebase Admin SDK key path
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load the previously saved model from the specified path
model_path = "IOTModel.pkl"  # Update this with your model's path

try:
    loaded_model = joblib.load(model_path)
except Exception as e:
    print("Error loading model:", e)
    print(traceback.format_exc())  # Print detailed traceback for debugging
    loaded_model = None

# Check if the model loaded successfully
if loaded_model is not None:
    # Load X_test and Y_test from files
    # Load X_test and Y_test from files
    X_test = joblib.load('X_test.pkl')
    Y_test = joblib.load('Y_test.pkl')

    # Make predictions with the loaded model
    predictions = loaded_model.predict(X_test)

    # Create a DataFrame to compare predicted and actual labels
    results_df = pd.DataFrame({
        'Predicted': predictions,
        'Actual': Y_test,
        'Features': X_test.tolist()  # Converting to list for easier visualization
    })

    # Group by 'Predicted' and take up to 15 samples from each group
    limited_results_df = results_df.groupby('Predicted').apply(lambda x: x.head(15)).reset_index(drop=True)

    # Initialize an empty dictionary to store results device-wise
    device_results = {}

    # Iterate through each row in the DataFrame
    for _, row in limited_results_df.iterrows():
        device_identifier = row['Features'][-1]  # Adjust this according to your features' structure

        # Create a list to store prediction and actual values for this device (if not already present)
        if device_identifier not in device_results:
            device_results[device_identifier] = []

        # Add the current prediction and actual values to the device's list
        device_results[device_identifier].append({
            "Predicted": row['Predicted'],
            "Actual": row['Actual'],
        })


    # Function to add alerts to Firebase
    def add_alerts_to_firebase():
        for device_identifier, results in device_results.items():
            for result in results:
                alert_data = {
                    "AlertID": str(uuid.uuid4()),  # Generate a unique ID
                    "AlertMessage": "Alert message here...",
                    "AlertSeverity": "low" if result['Predicted'] == 'BENIGN' else 'high',  # Adjust based on your criteria
                    "AlertTimestamp": firestore.SERVER_TIMESTAMP,
                    "AlertType": result['Predicted'],
                    "DeviceIdentifier": f"PC {device_identifier}"  # Fixed concatenation
                }
                db.collection('SecurityAlerts').add(alert_data)
                print(f"PC {device_identifier}")
        print("Alerts have been added to Firebase.")

    # Loop to add alerts every 10 seconds
    while True:
        add_alerts_to_firebase()
        time.sleep(10)