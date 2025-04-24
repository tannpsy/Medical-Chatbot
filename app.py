from flask import Flask, render_template, request, jsonify
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Flask app setup
app = Flask(__name__, static_folder="static", template_folder="templates")

# Load the dataset
with open("dataset/diseases.json") as file:
    diseases = json.load(file)

# Preprocess dataset
symptoms_data = [d["all_symptoms"] for d in diseases]
labels = [d["disease"] for d in diseases]

# Train the Naive Bayes model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(symptoms_data)
model = MultinomialNB()
model.fit(X, labels)

# Save the model and vectorizer for reuse
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_diagnosis", methods=["POST"])
def get_diagnosis():
    data = request.get_json()
    symptoms = data.get("symptoms", "")
    if not symptoms:
        return jsonify({"error": "Please provide your symptoms."})

    # Load the model and vectorizer
    with open("model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    # Transform user symptoms into vector
    user_symptoms_vector = vectorizer.transform([symptoms])
    prediction = model.predict(user_symptoms_vector)
    predicted_disease = prediction[0]

    # Fetch details of predicted disease
    for disease in diseases:
        if disease["disease"] == predicted_disease:
            response = {
                "disease": disease["disease"],
                "description": disease["description"],
                "treatment": disease["treatment"],
                "prevention": disease["prevention"]
            }
            return jsonify(response)
    
    return jsonify({"error": "Could not identify the disease. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
