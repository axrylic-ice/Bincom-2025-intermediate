# -----------------------------
# Import necessary libraries
# -----------------------------
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -----------------------------
# Load datasets
# -----------------------------
train_data = pd.read_csv('Bincom-answers/Test/train.csv')
test_data = pd.read_csv('Bincom-answers/Test/test.csv')

# Drop unnecessary columns for training and testing
x_train = train_data.drop(columns=['Loan_ID', 'Loan_Status'])
y_train = train_data['Loan_Status']
x_test = test_data.drop(columns=['Loan_ID'])

# -----------------------------
# Encode categorical values
# -----------------------------
# Replace string categories with numeric mappings
mapping = {
    "Male": 1, "Female": 0,
    "No": 0, "Yes": 1,
    "Graduate": 1, "Not Graduate": 0,
    "Urban": 0, "Semiurban": 1, "Rural": 2
}
x_train.replace(mapping, inplace=True)
x_test.replace(mapping, inplace=True)

# -----------------------------
# Clean numerical values
# -----------------------------
# Remove trailing "+" in values (e.g., "3+" → "3")
x_train = x_train.replace(r'^(\d+)\+$', r'\1', regex=True)
x_test = x_test.replace(r'^(\d+)\+$', r'\1', regex=True)

# Ensure all features are floats
x_train = x_train.astype(float)
x_test = x_test.astype(float)

# Encode target variable (Y/N → 1/0)
y_train.replace({"N": 0, "Y": 1}, inplace=True)

# -----------------------------
# Handle missing values
# -----------------------------

x_train.fillna(x_train.mean(), inplace=True)
x_test.fillna(x_test.mean(), inplace=True)
y_train.fillna(y_train.mode()[0], inplace=True)

# -----------------------------
# Split training data for validation
# -----------------------------
X_train, X_val, y_train_split, y_val = train_test_split(
    x_train, y_train, test_size=0.2, random_state=42
)

# -----------------------------
# Create ML pipeline
# -----------------------------
# Pipeline includes scaling and RandomForestClassifier
# Suggestion: Scaling may not be needed for tree-based models like RandomForest.
pipeline = Pipeline([  
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# -----------------------------
# Train the model
# -----------------------------
pipeline.fit(X_train, y_train_split)

# -----------------------------
# Validate the model
# -----------------------------
y_pred = pipeline.predict(X_val)

print("Accuracy:", accuracy_score(y_val, y_pred))
print("Classification Report:\n", classification_report(y_val, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_val, y_pred))

# -----------------------------
# Make predictions on the test set
# -----------------------------
test_predictions = pipeline.predict(x_test)

# -----------------------------
# Save predictions to CSV
# -----------------------------
# Suggestion: You load test.csv again here; reuse test_data instead.
output = pd.DataFrame({
    'Loan_ID': test_data['Loan_ID'],  
    'Loan_Status': test_predictions
})

output.to_csv('predictions.csv', index=False)
