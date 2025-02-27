# -*- coding: utf-8 -*-
"""Copy of TriNetX Brain Cancer Process.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ctsnkVV3iHYSBQB_hTjb-iyi98yQxRBY

Place all library importation code in the cell below
"""

import pandas as pd

"""Load data"""

!gdown 1PwDdEQPeBrXmStmlgbCvUGpGolsdaf3M

!gdown 1wjpmrV6KfnSdluYHyoU1egMQf8kXWK6x

"""Put data into pandas dataframe"""

df1 = pd.read_csv("patient.csv")
df2 = pd.read_csv("tumor.csv")

"""Display original data"""

df1

df2

"""Merge data (inner join)"""

df = pd.merge(df1, df2, 'inner', on = "patient_id")

df

"""Drop certain features"""

df = df.drop(["patient_id", "death_date_source_id", 'source_id_x', 'diagnosis_date',
              'observation_date', 'derived_by_TriNetX', 'source_id_y',
              "tumor_site_code_system", "morphology_code_system", "morphology_code",
              "stage_code_system", "stage_code", "tumor_size",
              "number_of_lymph_nodes", "metastatic"], axis = 1)

# Retain only US patients
df = df[df['patient_regional_location'] != "Unknow"]
df = df[df['patient_regional_location'] != "Ex-US"]

df = df.dropna()

df

"""Binarilize Data"""

# Drop unknown
for i in df.columns:
  df = df[df[i] != "Unknown"]

# Sex
df['Male']   = df['sex'] == "M"
df['Female'] = df['sex'] == "F"
df = df.drop('sex', axis = 1)

# Race
df['race_White']  = df['race'] == 'White'
df['race_Asian']  = df['race'] == 'Asian'
df['race_Black']  = df['race'] == 'Black or African American'

temp1 = df['race'] == 'American Indian or Alaska Native'
temp2 = df['race'] == 'Native Hawaiian or Other Pacific Islander'

df['race_Native'] = temp1 ^ temp2

df = df.drop('race', axis = 1)

# Ethnicity
df['hispanic']     = df['ethnicity'] == "Hispanic or Latino"
df['not_hispanic'] = df['ethnicity'] == "Not Hispanic or Latino"
df = df.drop('ethnicity', axis = 1)

# Marital status
df['married'] = df['marital_status'] == "Married"
df['single']  = df['marital_status'] == "Single"
df = df.drop('marital_status', axis = 1)

# Remove patients without age
df = df[df['reason_yob_missing'] == 'Present']
df = df.drop(['reason_yob_missing'], axis = 1)

# Age
df['age'] = (df['month_year_death'] / 100).astype('int') - df['year_of_birth']

df = df.drop(['year_of_birth', 'month_year_death'], axis = 1)

# Binarilize age
df['age_groups'] = pd.cut(df['age'], bins = 10)

for i in df.age_groups.unique():
  df[i] = df['age_groups'] == i

df = df.drop(['age'], axis = 1)
df = df.drop(['age_groups'], axis = 1)

# Region
for i in df.patient_regional_location.unique():
  df[i] = df['patient_regional_location'] == i

df = df.drop(['patient_regional_location'], axis = 1)

# Cancer
temp1 = df['tumor_site_code'].str.contains('C70')
temp2 = df['tumor_site_code'].str.contains('C71')
temp3 = df['tumor_site_code'].str.contains('C72')

df['cancer'] = temp1 ^ temp2 ^ temp3
df = df.drop(['tumor_site_code'], axis = 1)

df.info()

df.to_csv("TNX_BC_B.csv", header = True, index = False)

"""Download results"""

from google.colab import files
files.download('TNX_BC_B.csv')