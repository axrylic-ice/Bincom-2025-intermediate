# Import necessary libraries
from sklearn.datasets import fetch_california_housing  # For loading the California housing dataset as boston housing dataset isn't available
from sklearn.model_selection import train_test_split   # For splitting data into training and testing sets
from sklearn.ensemble import RandomForestRegressor    # Regression model
from sklearn.metrics import mean_squared_error, r2_score  # Evaluation metrics
from wk5 import build_pipeline                         # Custom pipeline builder function

# Optional SSL bypass (commented out)
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# Load the California housing dataset as a DataFrame
california = fetch_california_housing(as_frame=True)

# Separate features (X) and target (y)
X = california.data
y = california.target

# Split the dataset into training and testing sets
# 80% for training, 20% for testing, with a fixed random state for reproducibility
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model pipeline with a RandomForestRegressor
model = build_pipeline(RandomForestRegressor(n_estimators=100, random_state=42))

# Train the model
model.fit(x_train, y_train)

# Make predictions on the test set
predictions = model.predict(x_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)  # Mean Squared Error
r2 = r2_score(y_test, predictions)            # R^2 Score

# Print evaluation metrics
print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")
