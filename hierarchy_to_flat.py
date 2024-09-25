#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import openpyxl
import numpy as np


# In[22]:


df = pd.read_excel('C:/Users/Владелец/OneDrive/Рабочий стол/Розница/Чекимай.xlsx')
df.columns = df.iloc[0]
df = df.drop(index=0)
df = df.rename(columns={'Магазин': 'Check_Data'})
df['Store'] = ""
df['cash_box'] = ""
df['cashier'] = ""
df = df[['Check_Data', 'Store', 'cash_box', 'cashier'] + df.columns.tolist()[1:-3]]
df = df.drop([1, 2])
df = df.drop(df.index[-1])
df.reset_index(drop = True, inplace = True) 
# Loop to fill values in 'Store', 'cash_box', and 'cashier' columns
previous_datetime = df.at[0, 'Check_Data']
for i in range(len(df)):
    
    if i % 4 == 0:
        
        if str(df.at[i, 'Check_Data'])[0].isdigit():
            previous_datetime = df.at[i, 'Check_Data']
        else:
            duplicate_row_2 = df.loc[i].copy().to_frame().T
            duplicate_row_1 = df.loc[i-3].copy().to_frame().T
            df = pd.concat([df.iloc[:i+1], duplicate_row_2, df.iloc[i+1:]],ignore_index=True)
            df.at[i, 'Check_Data'] = previous_datetime
            
for i in range(len(df)):
               
    if i % 4 == 1:
        df.at[i-1, 'Store'] = df.at[i, 'Check_Data'] if pd.notnull(df.at[i, 'Check_Data']) else previous_datetime
        df.at[i, 'Store'] = df.at[i, 'Check_Data']
        df.at[i+1, 'Store'] = df.at[i, 'Check_Data']
        df.at[i+2, 'Store'] = df.at[i, 'Check_Data']
    elif i % 4 == 2:
        df.at[i-2, 'cash_box'] = df.at[i, 'Check_Data'] if pd.notnull(df.at[i, 'Check_Data']) else previous_datetime
        df.at[i, 'cash_box'] = df.at[i, 'Check_Data']
        df.at[i+1, 'cash_box'] = df.at[i, 'Check_Data']
        df.at[i-1, 'cash_box'] = df.at[i, 'Check_Data']
    elif i % 4 == 3:
        df.at[i-3, 'cashier'] = df.at[i, 'Check_Data'] if pd.notnull(df.at[i, 'Check_Data']) else previous_datetime
        df.at[i, 'cashier'] = df.at[i, 'Check_Data']
        df.at[i-2, 'cashier'] = df.at[i, 'Check_Data']
        df.at[i-1, 'cashier'] = df.at[i, 'Check_Data']
    
for i in range(len(df)):
    if i % 4 == 0:
        df.at[i+1, 'Check_Data'] = df.at[i, 'Check_Data']
        df.at[i+2, 'Check_Data'] = df.at[i, 'Check_Data']
        df.at[i+3, 'Check_Data'] = df.at[i, 'Check_Data']

# Создаем список для хранения индексов строк, которые будем удалять
rows_to_drop = []

# Задаем начальное значение для удаления строк (0-2)
start_row = 0

while start_row < len(df):
    
    if start_row % 4 != 3:
        rows_to_drop.append(start_row)
    start_row += 1

        # Удаляем строки по списку индексов rows_to_drop
df = df.drop(rows_to_drop)

# Сбросим индексы после удаления строк
df = df.reset_index(drop=True)

df.to_excel('C:/Users/Владелец/OneDrive/Рабочий стол/Розница/test.xlsx')


# In[ ]:




