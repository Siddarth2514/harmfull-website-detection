import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("dataset.csv")

# Convert 'type' column to binary labels
df['label'] = df['type'].map({'phishing': 1, 'benign': 0})

# Feature Engineering
df['url_length'] = df['URL'].apply(len)
df['contains_ip'] = df['URL'].apply(lambda x: 1 if any(char.isdigit() for char in x) else 0)

# Selecting Features and Labels
X = df[['url_length', 'contains_ip']]
y = df['label']

# Train Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save Model
pickle.dump(model, open("model.pkl", "wb"))
print("Model trained and saved!")
