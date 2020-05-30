from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from tqdm import tqdm
import base64
import pandas as pd


class GmailAPI:
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        self._SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

    def ConnectGmail(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                'credentials.json', self._SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))
        return service

    def GetMessageList(self, service, nextPageToken=None):
        # メールIDの一覧を取得する(最大100件)
        messageIDlist = service.users().messages().list(
            userId='me', pageToken=nextPageToken).execute()
        return messageIDlist

    def crowling_mail_box(self, th):
        #APIに接続
        service = self.ConnectGmail()
        message_list = []
        next_page_token = None
        for i in tqdm(range(0, th)):
            message_list_100 = self.get_message_list(service, next_page_token)
            message_list.extend(message_list_100["message_list"])
            if message_list_100["next_page_token"]:
                    next_page_token = message_list_100["next_page_token"]
            else:
                break
        return message_list

    def get_message_list(self, service, next_page_tolen=None):
        result = {"message_list": [], "next_page_token": None}
        try:
            if next_page_tolen:
                messageIDlist = self.GetMessageList(service, next_page_tolen)
            else:
                messageIDlist = self.GetMessageList(service)                    
            result["next_page_token"] = messageIDlist["nextPageToken"]                    
        except:
            print("API Error")
            raise


        #該当するメールが存在しない場合は、処理中断
        if messageIDlist['resultSizeEstimate'] == 0:
            print("Message is not found")
            return result

        #メッセージIDを元に、メールの詳細情報を取得
        for message in tqdm(messageIDlist['messages']):
            row = {}
            row['ID'] = message['id']
            MessageDetail = service.users().messages().get(
                userId='me', id=message['id']).execute()
            for header in MessageDetail['payload']['headers']:
                #日付、送信元、件名を取得する
                if header['name'] == 'Date':
                    row['Date'] = header['value']
                elif header['name'] == 'From':
                    row['From'] = header['value']
                elif header['name'] == 'Subject':
                    row['Subject'] = header['value']
            # 本文を取得
            # import ipdb; ipdb.set_trace()
            # base64_text = MessageDetail["payload"]["parts"][0]["data"]
            # def base64_dencoder(text):
            #     if len(text)>0:
            #         message = base64.urlsafe_b64decode(text)
            #         message = str(message, 'utf-8')
            #         # message = email.message_from_string(message)
            #     return message
            # row["text"] = base64_dencoder(base64_text)
            result["message_list"].append(row)
        return result


def to_dataframe_from_message(messages):
    messages_dict = {"From": [], "Date": [], "Subject": [], "ID": []}
    for message in tqdm(messages):
        messages_dict["From"].append(message["From"])
        messages_dict["Date"].append(message["Date"])
        messages_dict["Subject"].append(message["Subject"])
        messages_dict["ID"].append(message["ID"])
    message_df = pd.DataFrame(messages_dict)
    return message_df


if __name__ == '__main__':
    test = GmailAPI()
    messages = test.crowling_mail_box(10)
    messages_df = to_dataframe_from_message(messages)
    messages_df.to_pickle("./crowling_data.pkl")
