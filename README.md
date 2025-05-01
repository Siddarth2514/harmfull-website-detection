 AI-Powered URL Threat Detection Web App

 A web application that uses **Google Safe Browsing API** and a **custom-trained ML model** to detect malicious URLs in real-time. The system can classify URLs as safe or harmful (phishing/malware) and provides a security dashboard to track scan history.

Features:
- ✅ Real-time threat detection using Google Safe Browsing API  
- ✅ ML model-based prediction using URL features  
- ✅ Scan history with status tracking  
- ✅ Security dashboard with safe/malicious counts  
- ✅ Responsive UI with Flask & Jinja2 templating

 Tech Stack:
- **Frontend**: HTML, CSS (custom styling)  
- **Backend**: Python (Flask)  
- **ML Model**: Pickle-based Scikit-learn classifier  
- **API Integration**: Google Safe Browsing v4 API

 ML Model:
- Trained using basic URL features:
  - URL Length
  - Presence of IP address
- Model: Logistic Regression / Random Forest (customizable)
