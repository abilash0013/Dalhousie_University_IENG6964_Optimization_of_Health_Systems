import pandas as pd
import matplotlib.pyplot as plt
from google.colab import drive
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
encoder=LabelEncoder()

drive.mount('/content/drive')

path1 = "/content/drive/My Drive/train_data.csv"
df1 = pd.read_csv(path1) 
df1.tail()

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import math
# %matplotlib inline

fig= plt.figure(figsize=(20,20))
cols=3
rows=math.ceil(float(df1.shape[1])/cols)

for i, column in enumerate(["Ward_Type","Ward_Facility_Code","Bed Grade","Type of Admission","Severity of Illness",
                            "Age","Admission_Deposit","Stay"]):
    ax = fig.add_subplot(rows,cols, i+1)
    ax.set_title(column)
    if df1.dtypes[column] == np.object:
        df1[column].value_counts().plot(kind="bar",axes=ax)
    else:
        df1[column].hist(axes=ax)
        plt.xticks(rotation= 'vertical')
plt.subplots_adjust(hspace=0.7,wspace=0.2)
plt.show()

path2 = "/content/drive/My Drive/test_data.csv"
df2 = pd.read_csv(path2) 
df2.tail()

# Data pre-processing and Feature Engineering

df1.info()

df1.describe()

df1.isna().sum()

df1.describe().T

df1.Stay.value_counts()

df2['Severity of Illness'] .value_counts()

#categorical vaiables in both train and test data are label encoded
# 1) Department
# 2) Hospital_region_code
# 3) Ward_Type
# 4) Admission
# 5) Illness

df1["Department"]=encoder.fit_transform(df1['Department'])
df1["Hospital_region_code"]=encoder.fit_transform(df1['Hospital_region_code'])
df1["Ward_Type"]=encoder.fit_transform(df1['Ward_Type'])
df1["Type of Admission"]=encoder.fit_transform(df1['Type of Admission'])
#df1["Severity of Illness"]=encoder.fit_transform(df1['Severity of Illness'])
df1["Hospital_type_code"]=encoder.fit_transform(df1['Hospital_type_code'])
df1["Ward_Type"]=encoder.fit_transform(df1['Ward_Type'])
df1["Ward_Facility_Code"]=encoder.fit_transform(df1['Ward_Facility_Code'])

df2["Department"]=encoder.fit_transform(df2['Department'])
df2["Hospital_region_code"]=encoder.fit_transform(df2['Hospital_region_code'])
df2["Ward_Type"]=encoder.fit_transform(df2['Ward_Type'])
df2["Type of Admission"]=encoder.fit_transform(df2['Type of Admission'])
#df2["Severity of Illness"]=encoder.fit_transform(df2['Severity of Illness'])
df2["Hospital_type_code"]=encoder.fit_transform(df2['Hospital_type_code'])
df2["Ward_Type"]=encoder.fit_transform(df2['Ward_Type'])
df2["Ward_Facility_Code"]=encoder.fit_transform(df2['Ward_Facility_Code'])

df1.tail()

# Hosp_red_code, Bed Grade, Patient id, City_code_patient are not logically required to predict the LOS.
# Hence removing those features from both train and test data.

df1 = df1.drop(['Hospital_region_code', 'Bed Grade', 'patientid', 'City_Code_Patient'],axis=1)

df2 = df2.drop(['Hospital_region_code', 'Bed Grade', 'patientid', 'City_Code_Patient'],axis=1)

#Features having bins need to be encoded:
# 1) Age
# 2) Stay (Target)

severity_processing = {'Minor':0,'Moderate':1,'Extreme':3}

df1['Severity of Illness']=df1['Severity of Illness'].replace(severity_processing.keys(), severity_processing.values())

df2['Severity of Illness']=df2['Severity of Illness'].replace(severity_processing.keys(), severity_processing.values())

age_preprocessing = {'0-10': 0, '11-20': 1, '21-30': 2, '31-40': 3, '41-50': 4, '51-60': 5, '61-70': 6, '71-80': 7, '81-90': 8, '91-100': 9}

df1['Age'] = df1['Age'].replace(age_preprocessing.keys(), age_preprocessing.values())

df2['Age']= df2['Age'].replace(age_preprocessing.keys(), age_preprocessing.values())

stay_preprocessing = {'0-10': 0, '11-20': 1, '21-30': 2, '31-40': 3, '41-50': 4, '51-60': 5, '61-70': 6, '71-80': 7, '81-90': 8, '91-100': 9, 'More than 100 Days': 10}

df1['Stay'] = df1['Stay'].replace(stay_preprocessing.keys(), stay_preprocessing.values())

# Numerical Variables need to be scaled for better accuracy
# Following Features in "numerical_col" list is Numerical data to be scaled.

numerical_col = ['Type of Admission', 'Available Extra Rooms in Hospital', 'Visitors with Patient', 'Admission_Deposit']

from sklearn.preprocessing import StandardScaler
ss= StandardScaler()

df1[numerical_col]= ss.fit_transform(df1[numerical_col].values)

df2[numerical_col]= ss.fit_transform(df2[numerical_col].values)

plt.figure(figsize=(8,8))
sns.heatmap(df1.corr(), annot=True, cmap='coolwarm')

# Now in corr heat map, The variables are not highly correlated to each other.
# Proceeding to further prediction modelling.

from sklearn.ensemble import RandomForestClassifier

X_train = df1.drop(['case_id', 'Stay'], axis=1)
Y_train = df1["Stay"]
X_test  = df2.drop("case_id", axis=1).copy()



X_train.shape, Y_train.shape, X_test.shape

X_train.columns

X_train.info()

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, Y_train)

Y_pred1=gnb.predict(X_test)
gnb.score(X_train, Y_train)
acc_nbc = round(gnb.score(X_train, Y_train) * 100, 2)
acc_nbc

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train, Y_train)
Y_pred2 = knn.predict(X_test)
acc_knn = round(knn.score(X_train, Y_train) * 100, 2)
acc_knn

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit((X_train), Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_train, Y_train)
acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
acc_random_forest

sns.barplot(x= ['NaiveBayes','KNN','RF'],y= [acc_nbc,acc_knn,acc_random_forest])

result_csv = pd.DataFrame({
        "case_id": df2["case_id"],
       "Severity of Illness": df2["Severity of Illness"],
        "Stay": Y_pred2
})

len(result_csv)

result_csv['Stay'] = result_csv['Stay'].replace(stay_preprocessing.values(), stay_preprocessing.keys())
result_csv['Severity of Illness']=result_csv['Severity of Illness'].replace(severity_processing.values(), severity_processing.keys())

result_csv.to_csv('/content/drive/My Drive/results_LOS.csv', index = False)

result_csv.groupby(['Stay'])['case_id'].count().plot(kind='bar',color='blue')

result_csv.groupby(['Severity of Illness'])['case_id'].count().plot(kind='bar',color='red')

