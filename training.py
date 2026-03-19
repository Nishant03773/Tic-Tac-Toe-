import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("./tic_tac_toe.csv")

"""for training, all the values in the dataset must be a numeric,
in the chosen dataset, the values is alphabetical character. 
So, we need to convert in numberic..
"""
# data is in bytes like b'o', b'x' ....
# we have to convert it into string like o,x ...
for col in data.columns:
    data[col] = data[col].apply(lambda x: x[2:-1])


values = {'x':1,'o':-1,'b':0}

for i in data.columns[:-1]:
    data[i] = data[i].map(values)

data['Class'] = data['Class'].map({'positive':1,'negative':0})

# print(data.isnull().sum()) ----> No null value is found.

# Shows count of 0s and 1s
# sns.countplot(x="Class", data=data)
# plt.title("Class Distribution")
# plt.show() 

#Feature Distribution shows how the values of each feature (column) are spread in the dataset.
# data.iloc[:,:9].hist(figsize=(10,8))
# plt.suptitle("Board Feature Distribution")
# plt.show()

#A Feature Correlation Heatmap is a graphical representation that shows how strongly features (columns) are related to each other using color.
# plt.figure(figsize=(8,6))
# sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
# plt.title("Feature Correlation Heatmap")
# plt.show()

x = data.drop(columns=['Class'])
y = data['Class']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

# model = LogisticRegression() ---> Accuracy of the model slighlty lower than the decision tree
model = DecisionTreeClassifier()
model.fit(x_train,y_train)

accuracy = model.score(x_test, y_test)
print("Accuracy:", accuracy*100)

"""
pickle.dump(model, open("model.pkl", "wb")) 
--- this is correct but will show warnings while using the model 
--- warnings like - UserWarning: X does not have valid feature names, but LogisticRegression was fitted with feature names
  warnings.warn(
"""

pickle.dump((model, x.columns), open("model.pkl", "wb"))