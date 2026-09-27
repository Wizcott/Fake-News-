from flask import Flask, request, render_template
import torch
from transformers import BertTokenizer, BertModel
from model_def import BERT_Arch

app = Flask(__name__)

# Load tokenizer and model structure
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert = BertModel.from_pretrained("bert-base-uncased")
model = BERT_Arch(bert)

# Load your saved weights
model.load_state_dict(torch.load("saved_weights.pt", map_location=torch.device('cpu')))
model.eval()

# Prediction function
def predict(text):
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(tokens['input_ids'], tokens['attention_mask'])
        predicted = torch.argmax(outputs, dim=1).item()
        return "FAKE" if predicted == 0 else "REAL"

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = ""
    if request.method == "POST":
        input_text = request.form.get("text")
        if input_text:
            prediction = predict(input_text)
        return render_template("index.html", prediction=prediction, input_text=input_text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
