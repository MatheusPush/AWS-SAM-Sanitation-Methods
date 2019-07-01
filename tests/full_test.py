import requests
import json
import pandas as pd

# To start local API
# sam build
# sam local start-api

r = []

numbers = ['3.1', '5,01', '1.234,56', 'zero']
dates = ['1-01-22', '30.2.2020', '31/4/2000', '31/3/2000']
cnjs = ['5008501-82.2019.8.13.0702', '5008501.00.2019.8.13.0702', '8501-82.2019.8.13.0702', '5008501-82.2019.8.1.07']

r.append(requests.get('http://127.0.0.1:3000/format_number', params={'data': json.dumps(numbers)}).content)
r.append(requests.get('http://127.0.0.1:3000/format_date', params={'data': json.dumps(dates)}).content)
r.append(requests.get('http://127.0.0.1:3000/format_cnj', params={'data': json.dumps(cnjs)}).content)

print(r)

# -------------------------------------------------------------------------------------------------------------------- #

df = pd.DataFrame({'col1': ['3.1', '5,01', '1.234,56', 'zero'],
                   'col2': ['1-01-22', '30.2.2020', '31/4/2000', '31/3/2000'],
                   'col3': ['5008501-82.2019.8.13.0702', '5008501.00.2019.8.13.0702', '8501-82.2019.8.13.0702',
                            '5008501-82.2019.8.1.07']})

rules = {'format_number': ['col1'],
         'format_date': ['col2'],
         'format_cnj': ['col3'],
         'filter_number': {'col1': [5, 20]},
         'filter_date': {'col2': ['01/01/2000', '31/12/2000']}}

res = requests.get('http://127.0.0.1:3000/full_sanitization', params={'data': json.dumps(df.to_dict()),
                                                                         'rules': json.dumps(rules)})

r = pd.DataFrame(json.loads(res.content)['Formated Data'])

print(r)
