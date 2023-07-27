from pprint import pprint

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('/Users/ghaz/token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/Users/ghaz/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
    
    
SHEETS = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

SHEET_ID = '17hoMu9eifAtqmIK7K2_-K4jIZ1RexU3EZ2H2IJHbpQo'
results = SHEETS.spreadsheets().values().get(spreadsheetId=SHEET_ID,  range='Sheet1', valueRenderOption='FORMULA').execute()


values = results.get('values', [])

for row in values:
    current_formula_string = row[0]
    print(current_formula_string[12:len(current_formula_string)-2])