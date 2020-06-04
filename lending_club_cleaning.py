import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

dataset=pd.read_csv(r'C:\Users\pinup\Desktop\python\lending_club_loans.csv',skiprows=1)
half=len(dataset)/2
data=dataset.dropna(thresh=half,axis=1)

data=data.drop(['url','desc'],axis=1)

data_dictionary = pd.read_csv(r'C:\Users\pinup\Desktop\python\LCDataDictionary.csv')
print(data_dictionary.shape[0])
print(data_dictionary.columns.tolist())

data_dictionary = data_dictionary.rename(columns={'LoanStatNew': 'name', 'Description': 'description'})

loans = pd.DataFrame(data.dtypes,columns=['dtypes'])
loans = loans.reset_index()
loans['name'] = loans['index']
loans = loans[['name','dtypes']]
loans['first value'] = data.loc[0].values
preview = loans.merge(data_dictionary, on='name',how='left')
print(preview)

drop_list = ['id','member_id','funded_amnt','funded_amnt_inv','int_rate','sub_grade','emp_title','issue_d']
data = data.drop(drop_list,axis=1)

drop_cols = [ 'zip_code','out_prncp','out_prncp_inv',
'total_pymnt','total_pymnt_inv']
data = data.drop(drop_cols, axis=1)

drop_cols = ['total_rec_prncp','total_rec_int','total_rec_late_fee','recoveries','collection_recovery_fee', 'last_pymnt_d',
'last_pymnt_amnt']
data=data.drop(drop_cols,axis=1)

data['fico_average'] = (data['fico_range_high'] + data['fico_range_low']) / 2

cols = ['fico_range_low','fico_range_high','fico_average']

drop_cols = ['fico_range_low','fico_range_high','last_fico_range_low', 'last_fico_range_high']
data = data.drop(drop_cols, axis=1)
data.shape

data = data[(data["loan_status"] == "Fully Paid") |
(data["loan_status"] == "Charged Off")]
mapping_dictionary = {"loan_status":{ "Fully Paid": 1, "Charged Off": 0}}
data = data.replace(mapping_dictionary)

data = data.loc[:,data.apply(pd.Series.nunique) != 1]

data = data.drop('pymnt_plan', axis=1)

data.to_csv(r'C:\Users\pinup\Desktop\python/filtered_data.csv',index=False)



data2=pd.read_csv(r'C:\Users\pinup\Desktop\python/filtered_data.csv')
data2 = data2.drop("pub_rec_bankruptcies",axis=1)
data2 = data2.dropna()

data2['revol_util'] = data2['revol_util'].str.rstrip('%').astype('float')

drop_cols = ['last_credit_pull_d','addr_state','title','earliest_cr_line']
data2 = data2.drop(drop_cols,axis=1)

mapping_dict = {
"emp_length": {
"10+ years": 10,
"9 years": 9,
"8 years": 8,
"7 years": 7,
"6 years": 6,
"5 years": 5,
"4 years": 4,
"3 years": 3,
"2 years": 2,
"1 year": 1,
"< 1 year": 0,
"n/a": 0
},
"grade":{
"A": 1,
"B": 2,
"C": 3,
"D": 4,
"E": 5,
"F": 6,
"G": 7
}
}
data2 = data2.replace(mapping_dict)
data2[['emp_length','grade']].head()


nominal_columns = ["home_ownership", "verification_status", "purpose", "term"]
dummy_df = pd.get_dummies(data2[nominal_columns])
data2 = pd.concat([data2, dummy_df], axis=1)
data2 = data2.drop(nominal_columns, axis=1)

data2.to_csv(r"C:\Users\pinup\Desktop\python\clean_data.csv",index=False)




