import os
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the saved SVM pipeline (scaler + classifier bundled together)
model = pickle.load(open('model.pkl', 'rb'))

# Must match your LabelEncoder from train.ipynb
CLASS_NAMES = ['setosa', 'versicolor', 'virginica']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}

    required_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400

    # Feature order must match iris.feature_names from your notebook:
    # ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
    try:
        features = np.array([[
            float(data['sepal_length']),
            float(data['sepal_width']),
            float(data['petal_length']),
            float(data['petal_width'])
        ]])
    except (TypeError, ValueError):
        return jsonify({
            'error': 'All feature values must be numeric'
        }), 400

    # Pipeline handles scaling automatically — no need to scale manually
    prediction = model.predict(features)
    species = CLASS_NAMES[int(prediction[0])]

    return jsonify({
        'prediction': int(prediction[0]),
        'species': species
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
