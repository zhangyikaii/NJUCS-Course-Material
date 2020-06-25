
# coding: utf-8

# In[318]:


#Load the librarys
import pandas as pd #To work with dataset
import numpy as np #Math library
import seaborn as sns #Graph library that use matplot in background
import matplotlib.pyplot as plt #to plot some parameters in seaborn

#Importing the data
df_credit = pd.read_csv("C:/Users/Kai/Desktop/Assignment3/data/credit-g_preproccess.csv",index_col=0)


# In[319]:


# First Look at the data:
## Looking the Type of Data
## Null Numbers
## Unique values

df_credit.head(6)


# In[320]:


#Searching for Missings,type of data and also known the shape of data
print(df_credit.info())

# Let us check if there is any null values
print(df_credit.isnull().sum())

df_credit.shape


# In[321]:


#Looking unique values
print(df_credit.nunique())


# In[322]:


# Transforming the data into Dummy variables (IMPORTANT)
def one_hot_encoder(df, nan_as_category = False):
    original_columns = list(df.columns)
    categorical_columns = [col for col in df.columns if df[col].dtype == 'object']
    df = pd.get_dummies(df, columns= categorical_columns, dummy_na= nan_as_category, drop_first=True)
    new_columns = [c for c in df.columns if c not in original_columns]
    return df, new_columns

df_credit, new_colunms = one_hot_encoder(df_credit)
df_credit.head(6)


# In[323]:


print(df_credit.info())


# In[324]:


new_colunms


# In[325]:


#Purpose to Dummies Variable
# df_credit = df_credit.merge(pd.get_dummies(df_credit.purpose, drop_first=True, prefix='purpose'), left_index=True, right_index=True)


# In[326]:


plt.figure(figsize=(20,18))
sns.heatmap(df_credit.astype(float).corr(),linewidths=0.1,vmax=1.0, 
            square=True,  linecolor='white', annot=True)
plt.show()


# In[327]:


from sklearn.model_selection import train_test_split, KFold, cross_val_score # to split the data
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, fbeta_score #To evaluate our model

from sklearn.model_selection import GridSearchCV

# Algorithmns models to be compared
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


#Creating the X and y variables
X = df_credit.drop('class_good', 1).values
y = df_credit["class_good"].values


# In[328]:


# Spliting X and y into train and test version
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)
# to feed the random state
seed = 7

# prepare models
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('RF', RandomForestClassifier()))
models.append(('SVM', SVC(gamma='auto')))

# evaluate each model in turn
def pltFoldMethodsResult(scor):
    results = []
    names = []
    scoring = scor

    for name, model in models:
            kfold = KFold(n_splits=10, random_state=seed)
            cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)

    # boxplot algorithm comparison
    fig = plt.figure(figsize=(11,6))
    fig.suptitle('Algorithm Comparison')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    plt.ylabel(scor)
    plt.show()
    


# In[329]:


pltFoldMethodsResult('accuracy')


# In[330]:


pltFoldMethodsResult('recall')


# In[331]:


pltFoldMethodsResult('precision')


# In[332]:


pltFoldMethodsResult('f1')


# In[333]:


pltFoldMethodsResult('roc_auc')


# In[334]:


from sklearn.utils import resample
from sklearn.metrics import roc_curve
# Criando o classificador logreg
GNB = GaussianNB()

# Fitting with train data
model = GNB.fit(X_train, y_train)
# Printing the Training Score
print("Training score data: ")
print(model.score(X_train, y_train))

y_pred = model.predict(X_test)

print(accuracy_score(y_test,y_pred))
print("\n")
print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))

#Predicting proba
model.predict_proba(X_test)[:,1]
y_pred_prob = model.predict_proba(X_test)[:,1]

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)

# Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

