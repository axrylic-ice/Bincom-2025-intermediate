import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Custom pipeline builder (defined in wk5)
from wk5 import build_pipeline

# ======================================================
# PART 1: Decision Tree on Titanic dataset
# ======================================================

# -----------------------------
# Load Titanic dataset
# -----------------------------
dataset = pd.read_csv('Bincom-answers/wk3/Titanic.csv')

# -----------------------------
# Preprocess features and labels
# -----------------------------
# Drop irrelevant columns and encode categorical variables
X = dataset.drop(columns=['survived', 'class', 'embarked']).replace({
    'male': 0, 'female': 1,
    'man': 0, 'woman': 1, 'child': 2,
    'true': 1, 'false': 0
})
y = dataset['survived']

# -----------------------------
# Split dataset
# -----------------------------
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# -----------------------------
# Build and train model
# -----------------------------
model = build_pipeline(DecisionTreeClassifier())
model.fit(x_train, y_train)

# -----------------------------
# Evaluate model
# -----------------------------
predictions = model.predict(x_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Decision Tree Model Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_report(y_test, predictions))
print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))


# ======================================================
# PART 2: Naive Bayes on Spam/Ham dataset
# ======================================================

# -----------------------------
# Load Spam/Ham dataset
# -----------------------------
dataset2 = pd.read_csv('Bincom-answers/wk3/spam_ham_dataset.csv')

X2 = dataset2['text']        # features (raw text)
y2 = dataset2['label_num']   # labels (0 = ham, 1 = spam)

# -----------------------------
# Vectorize text data
# -----------------------------
vectorizer = CountVectorizer()
X2_vectorized = vectorizer.fit_transform(X2)

# -----------------------------
# Split dataset
# -----------------------------
x2_train, x2_test, y2_train, y2_test = train_test_split(
    X2_vectorized, y2, test_size=0.2, random_state=42
)

# -----------------------------
# Build and train Naive Bayes model
# -----------------------------
nb_model = MultinomialNB()
nb_model.fit(x2_train, y2_train)

# -----------------------------
# Evaluate Naive Bayes model
# -----------------------------
y2_predictions = nb_model.predict(x2_test)
nb_accuracy = accuracy_score(y2_test, y2_predictions)

print(f"Naive Bayes Model Accuracy: {nb_accuracy * 100:.2f}%")
print("Naive Bayes Classification Report:")
print(classification_report(y2_test, y2_predictions))
print("Naive Bayes Confusion Matrix:")
print(confusion_matrix(y2_test, y2_predictions))
