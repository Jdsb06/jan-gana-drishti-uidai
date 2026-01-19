import numpy as np
import pandas as pd

data_1 = pd.read_csv('data/api_data_aadhar_biometric/api_data_aadhar_biometric_0_500000.csv')
data_2 = pd.read_csv('data/api_data_aadhar_demographic/api_data_aadhar_demographic_0_500000.csv')
data_3 = pd.read_csv('data/api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv')

print("-"*100)
print(data_1.columns)

print("-"*100)
print(data_2.columns)

print("-"*100)
print(data_3.columns)

print("-"*100)
print(data_1.shape[0])