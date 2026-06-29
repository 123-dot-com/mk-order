from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


spreadsheet_id = ''

def main(creds, order):
    try:
        service = build("sheets", "v4", credentials=creds)
        spreadsheet = service.spreadsheets()
        spreadsheets = spreadsheet.get(spreadsheetId=spreadsheet_id).execute()
        values = spreadsheet.values().get(spreadsheetId=spreadsheet_id, range="Sheet1").execute()["values"]
        values = []
        body = {"values": values}
        result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range="Sheet1", valueInputOption="RAW", body=body).execute()

        '''
        
        sheets = []
        for i in range(0, len(spreadsheets["sheets"])):
            sheets.append(spreadsheets["sheets"][i]["properties"]["title"])
        '''

    except HttpError as error:
        print (f"An error has occured: {error}")

