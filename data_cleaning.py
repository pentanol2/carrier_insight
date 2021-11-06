# native python imports
from datetime import datetime
# third party libraries imports
import pandas as pd 


# read data from the csv file
jobs_df = pd.read_csv('glassdoor_jobs.csv')


# data cleaning 

# convert salaries to numnerical format

jobs_df = jobs_df[jobs_df['Salary Estimate'] != '-1']
jobs_df['Salary Estimate'] = jobs_df['Salary Estimate'].apply(lambda s : s.split('(')[0].replace('K','').replace('$',''))
jobs_df['hourly'] = jobs_df['Salary Estimate'].apply(lambda x : 1 if 'per hour' in x.lower() else 0)
jobs_df['employer_provided'] = jobs_df['Salary Estimate'].apply(lambda x : 1 if 'employer provided' in x.lower() else 0)
jobs_df['Salary Estimate'] = jobs_df['Salary Estimate'].apply(lambda x : x.lower().replace('per hour','').replace('employer provided salary:',''))
jobs_df['min_salary'] = jobs_df['Salary Estimate'].apply(lambda x: int(x.split('-')[0]))
jobs_df['max_salary'] = jobs_df['Salary Estimate'].apply(lambda x: int(x.split('-')[1]))
jobs_df['average_salary'] = (jobs_df['min_salary']+jobs_df['max_salary'])/2


# company name as text only
jobs_df['Company Name'] = jobs_df.apply(lambda x : x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)

# state field
jobs_df['same_state'] = jobs_df.apply(lambda x : 1 if  x['Location'] == x['Headquarters'] else 0 ,axis=1)
jobs_df['Location'] = jobs_df['Location'].apply(lambda x : x.split(',')[1])
jobs_df['Location'].value_counts()


# company age
jobs_df['age'] = jobs_df['Founded'].apply(lambda x : x if x < 1 else datetime.now().year - x)

# parsing of job descripiton
# python 
jobs_df['python'] = jobs_df['Job Description'].apply(lambda x : 1 if 'python' in x.lower() else 0)
jobs_df['python'].value_counts()
# R
jobs_df['r'] = jobs_df['Job Description'].apply(lambda x : 1 if 'r studio' in x.lower() else 0)
jobs_df['r'].value_counts()
# spark
jobs_df['spark'] = jobs_df['Job Description'].apply(lambda x : 1 if 'spark' in x.lower() else 0)
jobs_df['spark'].value_counts()
# aws
jobs_df['aws'] = jobs_df['Job Description'].apply(lambda x : 1 if 'aws' in x.lower() else 0)
jobs_df['aws'].value_counts()

# excel
jobs_df['excel'] = jobs_df['Job Description'].apply(lambda x : 1 if 'excel' in x.lower() else 0)
jobs_df['excel'].value_counts()

jobs_df = jobs_df.drop(['Unnamed: 0'],axis=1)
jobs_df.to_csv('salary_data_cleaned.csv',index=False)

jobs_clean_df = pd.read_csv('salary_data_cleaned.csv')

