import json
from time import time
import boto3
from botocore.client import Config
from botocore.vendored import requests
import xlrd

def lambda_handler(event, context):
    url = 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls'
    r = requests.get(url, allow_redirects=True)
    
    # we have write permissions only under /tmp so use the same
    open('/tmp/ISO10383_MIC.xls', 'wb').write(r.content)
    
    # open workbook
    workbook = xlrd.open_workbook('/tmp/ISO10383_MIC.xls')
    #print(workbook.sheet_names())
    
    # find the tab by name 'MICs List by CC'
    sheet = workbook.sheet_by_name('MICs List by CC')
    
    # get first row as heading
    heading = sheet.row(0)
    
    # initialize a variable for list
    head = list()
    
    # frame the heading into a list
    for a in heading:
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
    with open('/tmp/data.json', 'w') as outfile:
        json.dump(final, outfile)
        
        
    ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXX'
    ACCESS_SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    BUCKET_NAME = 'BUCKETNAMEGOESHERE'
    FILE_NAME = "/tmp/data.json"
    
    
    s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
    
    
    new_file_name = str(int(time())) + '.json'
    # Uploaded File
    s3.Bucket(BUCKET_NAME).upload_file(FILE_NAME, new_file_name, ExtraArgs={'ACL':'public-read'})
    
    upload = 'https://s3.ap-south-1.amazonaws.com/' + BUCKET_NAME + '/' + new_file_name
    
    # TODO implement
    out = dict()
    out['status'] = "success"
    out['file_name'] = upload
    
    data = dict()
    data['statusCode'] = 200
    data['isBase64Encoded'] = False
    data['body'] = json.dumps(out)
    data['headers'] = dict()
    
    return data
