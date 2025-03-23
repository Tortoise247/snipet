import poplib
from dotenv import load_dotenv
import os

POP3_PORT = 110  # 通常POP3はポート995を使用（SSL）

# .envファイルを読み込む
load_dotenv()

# 認証情報を環境変数から取得
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
POP3_SERVER=os.getenv('POP3_SERVER')

def connect_pop3_server():
    # Connect to the POP3 server
    mailServer = poplib.POP3(POP3_SERVER, POP3_PORT)
    # Log in to the server
    mailServer.user(USERNAME)
    mailServer.pass_(PASSWORD)
    # List the number of messages
    mailCount = len(mailServer.list()[1])
    print("Total emails: %s" % mailCount)
    return mailServer

if __name__ == "__main__":
    pop3_connection = connect_pop3_server()
    if pop3_connection:
        # 必要な操作をここで実行
        pop3_connection.quit()