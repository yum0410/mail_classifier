from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GmailAPI:
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        self._SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

    def ConnectGmail(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self._SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))

        return service

    def GetMessageList(self,DateFrom,DateTo,MessageFrom):

        #APIに接続
        service = self.ConnectGmail()

        MessageList = []

        query = ''
        # 検索用クエリを指定する
        if DateFrom != None and DateFrom !="":
            query += 'after:' + DateFrom + ' '
        if DateTo != None  and DateTo !="":
            query += 'before:' + DateTo + ' '
        if MessageFrom != None and MessageFrom !="":
            query += 'From:' + MessageFrom + ' '

        # メールIDの一覧を取得する(最大100件)
        messageIDlist = service.users().messages().list(userId='me',maxResults=100,q=query).execute()
        #該当するメールが存在しない場合は、処理中断
        if messageIDlist['resultSizeEstimate'] == 0: 
            print("Message is not found")
            return MessageList
        #メッセージIDを元に、メールの詳細情報を取得
        for message in messageIDlist['messages']:
            row = {}
            row['ID'] = message['id']
            MessageDetail = service.users().messages().get(userId='me',id=message['id']).execute()
            for header in MessageDetail['payload']['headers']:
                #日付、送信元、件名を取得する
                if header['name'] == 'Date':
                    row['Date'] = header['value'] 
                elif header['name'] == 'From':
                    row['From'] = header['value']
                elif header['name'] == 'Subject':
                    row['Subject'] = header['value']
            MessageList.append(row)
        return MessageList

if __name__ == '__main__':
    test = GmailAPI()
    #パラメータは、任意の値を指定する
    messages = test.GetMessageList(DateFrom='2019-01-01',DateTo='2020-02-01',MessageFrom='XXXXX@gmail.com')
    #結果を出力
    for message in messages:
        print(message)