# Library imports
import pandas as pd
from datetime import datetime as dt

# Google api imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SPREADSHEET_ID = ''
RANGE = f"{dt.now().strftime("%b")} \'{dt.now().strftime("%y")}"

def addSheet(current_sheet):
    body = {
    "requests": [
        {
            "addSheet": {
                "properties": {
                    "title": RANGE,
                    "index": 0,
                    "gridProperties": {
                        "rowCount": 1000,
                        "columnCount": 26
                    }
                }
            }
        }
    ]
    }
    current_sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

def addRow(values, order, choice):
    if choice == 1:
        values = [['Order No.', 'Order Date', 'Address', 'Item', 'Weight', 'Texture', 'SKU', 'Price Including GST']]

    if choice == 2:
        for i in range(0, order.shape[0], 1):
            values.append(
                [order.iloc[i]['Order'], 
                order.iloc[i]['Date'], 
                order.iloc[i]['Address'], 
                order.iloc[i]['Item'], 
                order.iloc[i]['Weight'], 
                order.iloc[i]['Texture'], 
                order.iloc[i]['SKU'], 
                order.iloc[i]['Price including GST']]
            )
    return values


def main(creds, order):
    try:
        service = build("sheets", "v4", credentials=creds)
        spreadsheet = service.spreadsheets()

        if dt.now().day == 1:
            addSheet(spreadsheet)
            body = {'values': addRow([], 'a', 1)}
            result = spreadsheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE, valueInputOption="RAW", body=body).execute()

        values = spreadsheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()["values"]
        body = {'values': addRow(values, order, 2)}
        result = spreadsheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE, valueInputOption="RAW", body=body).execute()

    except HttpError as error:
        print (f"An error has occured: {error}")
