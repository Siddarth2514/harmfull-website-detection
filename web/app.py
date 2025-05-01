import requests
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load ML model
model = pickle.load(open("model.pkl", "rb"))

# Google Safe Browsing API Key
GOOGLE_SAFE_BROWSING_API_KEY = "AIzaSyDnzoBZYnW29H4vE6L2he8U1dfPBPtSWAc"

# Store scan history
scan_history = []

def extract_features(url):
    url_length = len(url)
    contains_ip = 1 if any(char.isdigit() for char in url) else 0
    return np.array([[url_length, contains_ip]])

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form["url"]
        features = extract_features(url)
        prediction = model.predict(features)[0]
        result = "Malicious" if prediction == 1 else "Safe"
        
        # Store in scan history
        scan_history.append({"url": url, "verdict": result})

    return render_template("index.html", result=result)

@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/scan-url", methods=["GET"])
def scan_url_page():
    return render_template("virus_scan.html")

@app.route("/scan-url", methods=["POST"])
def scan_url():
    url = request.form["url"]
    safe_browsing_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "client": {
            "clientId": "your-app-name",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(safe_browsing_url, json=payload, headers=headers)

    print("Response Code:", response.status_code)
    print("Response Text:", response.text)  # This prints Google's response in the terminal

    if response.status_code == 200:
        result = response.json()
        if "matches" in result:
            verdict = "⚠️ Malicious URL detected!"
        else:
            verdict = "✅ Safe URL"
    else:
        verdict = f"❌ Error checking Google Safe Browsing: {response.text}"

    # Store in scan history
    scan_history.append({"url": url, "verdict": verdict})

    return render_template("virus_scan.html", result=verdict, scanned_url=url)


@app.route("/security-dashboard")
def security_dashboard():
    # Count malicious & safe websites
    malicious_count = sum(1 for scan in scan_history if "Malicious" in scan["verdict"])
    safe_count = sum(1 for scan in scan_history if "Safe" in scan["verdict"])

    return render_template(
        "security_dashboard.html",
        scan_history=scan_history,
        malicious_count=malicious_count,
        safe_count=safe_count
    )

if __name__ == "__main__":
    app.run(debug=True)
