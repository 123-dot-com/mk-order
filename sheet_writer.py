from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# range value must be updated based on the sheet, which requires a bit more work
spreadsheet_id = '1WdcH4p4ZU3hyOGWI9jb_siPWE_aj8-JPbwjV1nB_fNU'
range_read = 'A1 :E5'


def main(creds):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_read).execute()
    values = result.get('values', [])
    print (values)



