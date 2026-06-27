# Millkraft Order Automator
A tool to automate the generation of the daily order sheet.
This is done by pulling data from Millkraft's Gmail inbox, and from the Google Form responses.

## Quickstarting:
Before starting this program, make sure you have your credentials (client secrets) from your [Google Cloud Console](console.cloud.google.com). After that is done, you may follow these steps:

1. Navigate to the directory in which this repo was cloned

```
cd <DIRECTORY-OF-THIS-REPO>
```

2. Copy the client secrets file downloaded from the cloud console and paste it here, renaming it to 'credentials.json'

3. Open the google sheet you want to link to the program, and copy the spreadsheet ID

```
https://docs.google.com/spreadsheets/d/<SPREADSHEET-ID>/edit?gid=0#gid=0
```
4. Open the file named sheet_writer.py in a text editor, and edit the variable named spreadsheet_id and save the file

```
spreadsheet_id = <SPREADSHEET-ID>
```
5. Now, run the 'main.py' file

```
python main.py
```
6. If it's your first time running it, you will be redirected to a Google login page, where it will ask for your authorisation to permit the program to access your Google data. This will only happen the first time, as long as the 'token.json' file remains, and your client secrets do not expire.
