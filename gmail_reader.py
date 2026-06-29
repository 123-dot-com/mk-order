import base64
import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

whitelist=[chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)]



def clean(str, choice):
    if choice == 1:
        out=""
        for c in str:
            if c not in whitelist:
                out += 'a'
            else:
                out += c 
        return out
    
    elif choice == 2:
        start = str.find("Order:")
        if start != -1:
            str=str[start:]
            str=str.replace('\\r', '\r')
            str=str.replace('\\n', '\n')
            return str
        else:
            print ("Error in email format...")
            return "-1"

def extract(msg):
    clean_msg = msg[0: msg.find('Delivery charges are distance-based.')]
    order = clean_msg[clean_msg.find("Order:* ")+8: clean_msg.find('  |')]
    date = clean_msg[clean_msg.find("Date:* ")+7: clean_msg.find('\n')]
    address = clean_msg[clean_msg.find('Shipping Address')+18: clean_msg.find("Shipping Method")]
    instructions = clean_msg[clean_msg.find('Special Instructions')+22: clean_msg.find('-')]
    summary = msg[msg.find('Order Summary'):msg.find('Subtotal')-1]

    items = pd.DataFrame(columns=['Item', 'Weight', 'Texture', 'SKU', 'Price including GST'])
    while summary.find('[image:') != -1:
        item = summary[summary.find('<https://millkraft.com/shop/ols/products/')+41: summary.find('>')]
        weight = summary[summary.find('Kgs: ')+5: summary.find('Texture: ')-1]
        texture = summary[summary.find('Texture: ')+9: summary.find('SKU: ')-1]
        sku = summary[summary.find('SKU: ')+5: summary.find('*')-1]
        price = summary[summary.find('\\xe2\\x82\\xb9')+12: summary.find('incl.')-3]
        row = {'Item': item, 'Weight': weight, 'Texture': texture, 'SKU': sku, 'Price including GST': price}
        items.loc[len(items)] = row
        summary = summary[summary.find('incl. 5% GST')+12:]

    final = {'Order': [order], 'Date': [date], 'Address': [address]}
    final = pd.DataFrame.from_dict(final)
    final = pd.concat([final,items], axis=1)
    return final

def markRead(service, msg_id):
    body = {'removeLabelIds': ['UNREAD']}
    message = service.users().messages().modify(userId='me', id=msg_id, body=body).execute()


def main(creds):
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", labelIds=["UNREAD"]).execute()
    messages = results.get("messages", [])

    if not messages:
      print("No messages found.")
      return

    count=0
    output = pd.DataFrame(columns=['Order', 'Date', 'Address', 'Item', 'Weight', 'Texture', 'SKU', 'Price including GST'])
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        if msg['snippet'].find('noreply@mysimplestore.com') != -1:
            clean_msg=clean(msg['payload']['parts'][0]['body']['data'], 1)
            clean_msg=clean_msg.encode('utf-8')
            clean_msg=clean(str(base64.b64decode(clean_msg)), 2)
            output = pd.concat([output, extract(clean_msg)], ignore_index=True)
            markRead(service, msg['id'])

  except HttpError as error:
    print(f"An error occurred: {error}")

  return output
      


