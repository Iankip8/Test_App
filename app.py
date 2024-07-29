from flask import Flask, request, jsonify
import joblib
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Construct the relative path to the model file
current_directory = os.path.dirname(__file__)
model_path = os.path.join(current_directory, 'voting_classifier_pipeline2.pkl')

# Load the trained model
try:
    model = joblib.load(model_path)
    logging.info(f"Model loaded successfully from {model_path}")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the model API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the POST request
        data = request.get_json()
        
        # Check if the input key exists in the request data
        if not data or 'input' not in data:
            logging.warning('Input data missing or incorrect format.')
            return jsonify({'error': 'No input data provided'}), 400
        
        # Extract input data
        input_data = data['input']
        
        # Validate input data type
        if not isinstance(input_data, list):
            logging.warning('Input data type is incorrect.')
            return jsonify({'error': 'Input data should be a list'}), 400
        
        # Ensure input data is not empty
        if not input_data:
            logging.warning('Input data list is empty.')
            return jsonify({'error': 'Input data list is empty'}), 400
        
        # Make prediction
        prediction = model.predict(input_data)  # Remove the outer list

        # Return the result as JSON
        return jsonify({'prediction': prediction.tolist()})
    
    except Exception as e:
        logging.error(f"Error during prediction: {e}", exc_info=True)
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    # Get the port from the environment variable, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app, specifying host='0.0.0.0' to accept connections from any IP address
    app.run(host='0.0.0.0', port=port, debug=True)
