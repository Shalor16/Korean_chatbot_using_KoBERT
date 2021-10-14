# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import csv

data = pd.read_csv('restaurant_train.csv')

questions = []
answers = []

# +
for i in range(len(data)-1):
    if (data.iloc[i].QA여부=='q' and data.iloc[i+1].QA여부=='a') and (data.iloc[i].QA번호 == data.iloc[i+1].QA번호):
        questions.append(data.iloc[i].발화문)
        answers.append(data.iloc[i+1].발화문)
    
print(questions[0:10], answers[0:10])
# -
f=open('train_label.tsv','w', encoding='utf-8', newline='')
w = csv.writer(f, delimiter='\t')
for i in range(len(questions)):
    w.writerow([questions[i],i])
f.close

f=open('result_answer.tsv','w', encoding='utf-8', newline='')
w = csv.writer(f, delimiter='\t')
for i in range(len(questions)):
    w.writerow([i,answers[i]])
f.close
