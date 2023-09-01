# -*- coding: utf-8 -*-
"""HAPRI Data Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-n5l_Qxkr5E0zcERuqgSTHvGKkS4ETGu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
from scipy import stats
from datetime import datetime

from google.colab import drive
drive.mount('/content/drive')

link = "drive/My Drive/Economics Research/HAPRI/Civil Society in Public Health/Data/Health CSO Dataset (Final).xlsx"
#link = "H:\My Drive\Economics Research\HAPRI\Civil Society in Public Health\Data\Health CSO Dataset.xlsx"
# data = pd.read_csv(r"drive/MyDrive/Colab Notebooks/QR_project_data_Graeme.csv")
data = pd.read_excel(link)
data.drop(data.columns[23:], axis=1, inplace=True)
data

### LABEL VARIABLE IN THE DATA ###
##################################

data.columns.values

### LABEL IN THIS DATASETS
function_label = ["Health Services", "Health Promotion and Information", "Policy Setting", "Resource Mobilization", "Monitoring Quality"]
definition_label = ["VNGO", "INGO", "Mass organization", "Professional associations and umbrella organisations", "Charities/Fund", "Research/training institute"]
columns_name = list(data.columns.values)

### LABEL FOR HEADER
cso = data["CSO"]
year = data["Year established"]
defi = data["Definition (5 groups)"]
func1 = data["Functionality (WHO)"]
func2 = data["Unnamed: 4"]
func3 = data["Unnamed: 5"]
func4 = data["Unnamed: 6"]
func5 = data["Unnamed: 7"]
status = data["Status"]
scope = data["Scope"]
audience1 = data["Target Audience"]
audience2 = data["Unnamed: 15"]
audience3 = data["Unnamed: 16"]
audience4 = data["Unnamed: 17"]
audience5 = data["Unnamed: 18"]

### CHECKING AND CLEARNING DATA ###
##################################

import math
check_funcCol = [func1, func2, func3, func4, func5]
for col in check_funcCol:
  for i in func2:
    if i not in function_label and math.isnan(i) == False:
      print("Typing Error {var}".format(var = i))

defi.unique()

print(year[213].year)
check = type(year[213]) is datetime
print(int(year[213].year))
check

def count_yearEsta():
  for index in range(0, len(year)):
    y = year[index]
    # check_in = type(y) is int
    # check_nan = math.isnan(y)
    check_date = type(y) is datetime
    # if check_in == True:
    #   pass
    # if check_nan == True:
    #   pass
    if check_date == True:
      year[index] = int(y.year)

count_yearEsta()

vnData_CSO_yearEstablished = []
vnData_CSO_countEstablished = []
def count_yearInt():
  vnData_CSO = {}
  for index in range(0, len(year)):
    if type(year[index]) is int:
      if year[index] not in list(vnData_CSO.keys()):
        vnData_CSO[year[index]] = 1
      else:
        vnData_CSO[year[index]] += 1
  myKeys = list(vnData_CSO.keys())
  myKeys.sort()
  new_dict = {i: vnData_CSO[i] for i in myKeys}

  for index in range(0, len(myKeys)):
    if index != 0:
      key = myKeys[index]
      preKey = myKeys[index-1]
      new_dict[key] += new_dict[preKey]

  return new_dict
print(count_yearInt())

a = []
for i in year:
  # if type(i) is not int and math.isnan(i) == False:
  #   print("not!")
  if type(i) is int:
    a.append(type(i))

# a = set(a)
print(len(a))

### RUNNING DATA ###
##################################

#có bao nhiêu CSO là professional group, ...
def count_CSODefinition():
  #result_definition = {"VNGO": 0, "INGO":0, "Mass Organization":0, "Professional group":0, "Charities/Fund":0, "Research/training institute":0, "Social Enterprise":0, "Popular association":0}
  result_definition = {}
  for definition in data["Definition (5 groups)"]:
    for label in definition_label:
      if definition == label:
        if result_definition.get(label) == None:
          result_definition[label] = 1
        else:
          result_definition[label] += 1
  return result_definition

cnt_defi = count_CSODefinition()
cnt_defi

#có bao nhiêu CSO trong từng loại chức năng, thành phần, chức năng nào ít nhiều tham gia
def count_CSOFunctionality():
  result_functionality = {}
  columns_ord = ['Functionality (WHO)', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7']
  for col in columns_ord:
    for func in data[col]:
      for label in function_label:
        if func == label :
          if result_functionality.get(label) == None:
            result_functionality[label] = 1
          else:
            result_functionality[label] += 1
  return result_functionality

cnt_func = count_CSOFunctionality()
cnt_func

#số CSO làm chỉ 1 chức năng, 2 chức năng, nhiều chức năng
# for i in
def count_GroupFunctionality():
  result_grFunc = [
      {'num': 0, 'index': []}, #1
      {'num': 0, 'index': []}, #2
      {'num': 0, 'index': []},#3
      {'num': 0, 'index': []},#4
      {'num': 0, 'index': []} #5
  ]
  for i in range(0, len(data)):
    amt = 0
    if data.iloc[i]['Functionality (WHO)'] not in function_label:
      amt +=1
    if data.iloc[i]['Unnamed: 4'] not in function_label:
      amt +=1
    if data.iloc[i]['Unnamed: 5'] not in function_label:
      amt +=1
    if data.iloc[i]['Unnamed: 6'] not in function_label:
      amt +=1
    if data.iloc[i]['Unnamed: 7'] not in function_label:
      amt +=1
    index = amt - 1
    result_grFunc[index]['num'] += 1
    result_grFunc[index]['index'].append(i)
  return result_grFunc

cnt_GrFunc = count_GroupFunctionality()
for nums in cnt_GrFunc:
  print(nums['num'])

# Các chức năng nào đc làm chung với nhau
def count_FuncCrossTab():
  resultCrossTab = {
      "Health Services": {
          "Health Services": 0,
          "Health Promotion and Information": 0,
          "Monitoring Quality": 0,
          "Policy Setting": 0,
          "Resource Mobilization": 0
      },
      "Health Promotion and Information": {
          "Health Promotion and Information": 0,
          "Health Services": 0,
          "Monitoring Quality": 0,
          "Policy Setting": 0,
          "Resource Mobilization": 0
      },
      "Monitoring Quality": {
          "Monitoring Quality" : 0,
          "Health Services": 0,
          "Health Promotion and Information": 0,
          "Policy Setting": 0,
          "Resource Mobilization": 0
      },
      "Policy Setting": {
          "Policy Setting": 0,
          "Health Services": 0,
          "Health Promotion and Information": 0,
          "Monitoring Quality": 0,
          "Resource Mobilization": 0,
      },
      "Resource Mobilization": {
          "Resource Mobilization": 0,
          "Health Services": 0,
          "Health Promotion and Information": 0,
          "Monitoring Quality": 0,
          "Policy Setting": 0,
      }
  }

  for i in range(0, len(data)):
    data1 = data.iloc[i]['Functionality (WHO)']
    data2 = data.iloc[i]['Unnamed: 4']
    data3 = data.iloc[i]['Unnamed: 5']
    data4 = data.iloc[i]['Unnamed: 6']
    data5 = data.iloc[i]['Unnamed: 7']

    func_order = [data2, data3, data4, data5]

    for e in func_order:
      if data1 != e:
        if e in function_label:
          resultCrossTab[data1][e] += 1
          resultCrossTab[e][data1] += 1
  print(resultCrossTab)
  raw_data_df = pd.DataFrame(resultCrossTab,columns= function_label)
  raw_data_df = raw_data_df.reindex(function_label, fill_value=0)
  return raw_data_df

cntCrosFunc = count_FuncCrossTab()
cntCrosFunc

# Bảng chéo 2 biến giữa functionality x definition
def crosstabDefFunc():
  result_func4 = pd.crosstab(defi, func4).reindex(definition_label, columns = ["Health Promotion and Information", "Health Services", "Monitoring Quality", "Policy Setting", "Resource Mobilization"], fill_value=0)
  result_func5 = pd.crosstab(defi, func5).reindex(definition_label, columns = ["Health Promotion and Information", "Health Services", "Monitoring Quality", "Policy Setting", "Resource Mobilization"], fill_value=0)
  result = pd.crosstab(defi, func1).reindex(definition_label, fill_value=0) + pd.crosstab(defi, func2).reindex(definition_label, fill_value=0) + pd.crosstab(defi, func3).reindex(definition_label, fill_value=0) + result_func4 + result_func5
  return result

crosstabDefFunc()

# crosstab definition x target audience
pd.crosstab(defi, audience3)

### VISUALIZATION ###

import numpy as np
import matplotlib.pyplot as plt

cso_key = list(cnt_defi.keys())
cso_values = list(cnt_defi.values())

fig, ax = plt.subplots(figsize =(16, 9))
ax.barh(cso_key, cso_values)

for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)

# Add x, y gridlines
ax.grid( color ='grey',linestyle ='-.', linewidth = 0.5, alpha = 0.2)

# Show top values
ax.invert_yaxis()

# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')

# Add Plot Title
ax.set_title('Number of CSOs',
             loc ='left', )

# Add Text watermark
fig.text(0.9, 0.15, 'authors: Trinh Nguyen & Phu Nguyen', fontsize = 12,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)

# Show Plot
plt.show()

import numpy as np
import matplotlib.pyplot as plt

cnt_func = count_CSOFunctionality()
cso_key = list(cnt_func.keys())
cso_values = list(cnt_func.values())

fig, ax = plt.subplots(figsize =(10, 5))
ax.barh(cso_key, cso_values)

for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)

# Add x, y gridlines
ax.grid( color ='grey',linestyle ='-.', linewidth = 0.5, alpha = 0.2)

# Show top values
ax.invert_yaxis()

# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')

# Add Plot Title
ax.set_title('Number of CSOs functionality',
             loc ='left', )

# Add Text watermark
fig.text(0.9, 0.15, 'authors: Trinh Nguyen & Phu Nguyen', fontsize = 12,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)

# Show Plot
plt.show()

sns.heatmap(crosstabDefFunc(), annot = True, cmap = 'RdYlGn')

sns.heatmap(count_FuncCrossTab(), annot = True, cmap = 'RdYlGn')

fig, ax = plt.subplots()
stack_plot = crosstabDefFunc()
stack_plot.plot(kind="bar", stacked = True, ax = ax)

ax.set_title("Đồ thị phân phối từng lĩnh vực của CSOs")
plt.xlabel("CSOs")
plt.ylabel("Functionality")

fig.tight_layout()
fig.set_size_inches(10, 90)
plt.show()

fig, ax = plt.subplots()
stack_plot = crosstabDefFunc()
stack_plot = stack_plot.transpose()
stack_plot.plot(kind="bar", stacked = True, ax = ax)

ax.set_title("Đồ thị phân phối CSOs trong tung linh vuc")
plt.xlabel("CSOs")
plt.ylabel("Functionality")

fig.tight_layout()
fig.set_size_inches(10, 20)
plt.show()

vnData_healthExpenditure_year = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

vnData_healthExpenditure_values = [3.81915736, 4.51130629, 3.59967446, 3.66619396, 3.79920292, 4.01387405, 4.24659491, 4.30235767, 4.05425692, 4.16906166, 4.69927311, 4.6128521, 5.00178242, 5.07556248, 4.6127553, 4.56543732, 4.51853609, 4.71283484, 5.04966736, 5.03395176, 4.68066788]

plt.plot(vnData_healthExpenditure_year, vnData_healthExpenditure_values)
plt.title('Health Expenditure shared of GDP, source: World Bank')
plt.xlabel('Years')
plt.ylabel('Shared of GDP')
plt.show()

csoDataYear = count_yearInt()
plt.plot( list(csoDataYear.keys()), list(csoDataYear.values()) )
plt.title('Number of CSOs base on time')
plt.xlabel('Years')
plt.ylabel('Number of CSOs')
plt.show()

newDataYear = {}
for key in list(csoDataYear.keys()):
  if key > 2000:
    newDataYear[key] = csoDataYear[key]
newDataYear

plt.plot( list(newDataYear.keys()), list(newDataYear.values()) )
plt.title('Number of CSOs base on time from 2000 to 2022')
plt.xlabel('Years')
plt.ylabel('Number of CSOs')
plt.show()

result_grFunc = []
cnt_GrFunc = count_GroupFunctionality()
for nums in cnt_GrFunc:
  result_grFunc.append(nums['num'])
x_axis = [1,2,3,4,5]

fig = plt.figure(figsize = (10, 5))

# creating the bar plot
plt.bar(x_axis, result_grFunc, color ='maroon',
        width = 0.4)

plt.xlabel("Số lượng chức năng mà một CSOs có thể đảm nhận")
plt.ylabel("Số lượng CSOs")
plt.title("Các CSOs thường đảm nhận bao nhiêu chức năng?")
plt.show()

import matplotlib.pyplot as plt
import numpy as np

#y = np.array([35, 25, 25, 15])
y = np.array([26, 87, 99, 102, 6])
mylabels = ["1 Function", "2 Functions", "3 Functions", "4 Functions", "5 Functions"]
myexplode = [0.2, 0, 0, 0, 0]

plt.pie(y, labels = mylabels, explode = myexplode, shadow = True, autopct='%1.0f%%')
plt.show()

