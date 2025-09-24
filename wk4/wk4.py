from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from wk5 import build_pipeline
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context



california= fetch_california_housing(as_frame=True)

X= california.data
y= california.target

x_train,x_test,y_train,y_test= train_test_split(X,y,test_size=0.2, random_state=42)

model= build_pipeline(RandomForestRegressor(n_estimators=100, random_state=42))
model.fit(x_train,y_train)
predictions= model.predict(x_test)

mse= mean_squared_error(y_test, predictions)
r2= r2_score(y_test, predictions)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")
