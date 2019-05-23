import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#Reading data
dataset = pd.read_csv('Data.csv')

#Dropping Duplicate Rows
dataset=dataset.drop_duplicates()

data_type=dataset.dtypes

t=dict(data_type)
print(t)

new_dataset=pd.DataFrame()

#Replacing missing data with mean for numeric and mode for string
for k,v in t.items():
    df=pd.DataFrame()
    df[k]=dataset[k]
    #Specially for Tathagat this will replace every random shit character in that column with NaN
    df=df.replace(regex='[?#@!*()+-]',value=np.nan)
    if v=='object' or v=='bool':
        imp_most = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        df=pd.DataFrame(imp_most.fit_transform(df))
        df.columns=[k]
        new_dataset[k]=df[k]
    else:
        imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
        df=pd.DataFrame(imp_mean.fit_transform(df))
        df.columns=[k]
        new_dataset[k]=df[k]

#Encoding Categorical Data
categorical_variables = list(new_dataset.select_dtypes(exclude=['int64','float','bool']).columns.values)
new_dataset= pd.get_dummies(new_dataset, prefix_sep="__",columns=categorical_variables)

#Now all that is left is to LabelEncode the independent variable which is only needed for classification and we can remove this step for regression
'''labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)'''

#Next is Feature Selection
#Can be implemented in two ways
#1)Proposed by Tathagat
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
test = SelectKBest(score_func=f_classif, k=4)
fity = test.fit(X, Y)
global features
features = fity.transform(X)
nm = (X.columns[fity.get_support()]) 
dr = pd.DataFrame(features,columns=nm)
