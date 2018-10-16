# Imports for Google APIs
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/presentations'

def getService():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('slides', 'v1', http=creds.authorize(Http()))

# Extact any and all texts from an element.
def getAllText(element):
    textElements = []
    output = ""
    try:
      textElements = element['shape']['text']['textElements']
    except:
      pass

    for text in textElements:
      try:
        output += text['textRun']['content'].encode('utf-8').strip() + "\n"
      except:
        pass
    return output

