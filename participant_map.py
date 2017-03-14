import pandas as pd

participants = pd.read_excel("participant_map.xlsx", header=[1])
female_staff = participants.iloc[1:8][["Email","IMEI"]]
male_staff = participants.iloc[10:16][["Email","IMEI"]]
female_student = participants.iloc[18:23][["Email","IMEI"]]
male_student = participants.iloc[25:32][["Email","IMEI"]]