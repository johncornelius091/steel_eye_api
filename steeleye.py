import requests
#from openpyxl import load_workbook
import xlrd
import json

# download file from the source
'''url = 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls'
r = requests.get(url, allow_redirects=True)
open('ISO10383_MIC.xls', 'wb').write(r.content)
'''

# open workbook
workbook = xlrd.open_workbook('ISO10383_MIC.xls')
#print(workbook.sheet_names())

# find the tab by name 'MICs List by CC'
sheet = workbook.sheet_by_name('MICs List by CC')

heading = sheet.row(0)

# initialize a variable for list
head = list()

# frame the heading into a list
for a in heading:
    print(a)
    head.append(str(a).lstrip("text:'").rstrip("'"))

# initialize counter for looping rows
n = 1

# initialize dict
output = dict()
final = list()

# loop thru the rows and frame a list of dicts(rows)
try:
    while (sheet.cell(n, 0) != xlrd.empty_cell.value):
        row = sheet.row(n)
        i = 0
        for me in row:
            output[head[i]] = str(me).lstrip("text:'").rstrip("'")
            i = i+1
        final.append(output) #[]
        n = n +1
except IndexError:
    temp = 5

# write data to json file
with open('data.json', 'w') as outfile:
    json.dump(final, outfile)

