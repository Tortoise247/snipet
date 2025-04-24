import poplib
from dotenv import load_dotenv
import os
from email.parser import Parser
from datetime import datetime
import re
from email.header import decode_header


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
    print("login success")
    return mailServer

def decode_header_value(header_value):
    decoded_fragments = decode_header(header_value)
    decoded_string = ''.join(
        part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
        for part, encoding in decoded_fragments
    )
    return decoded_string

if __name__ == "__main__":
    pop3_connection = connect_pop3_server()
    if pop3_connection:
        # 必要な操作をここで実行
        # Get the number of messages
        num_messages = len(pop3_connection.list()[1])

        # Iterate through messages
        for i in range(num_messages):
            # Retrieve the message
            response, lines, octets = pop3_connection.retr(i + 1)
            # Parse the message
            msg_content = b"\r\n".join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            # Get the date of the email
            email_date = msg.get("Date")
            
            # Remove the timezone abbreviation (e.g., "(JST)" or "GMT")
            email_date_cleaned = re.sub(r"\s+\(.*\)$", "", email_date)
            
            # # Handle timezone names like "GMT" by removing them
            # email_date_cleaned = re.sub(r"\s+[A-Z]{3,}$", "", email_date_cleaned)
            
            # Parse the cleaned date
            try:
                email_datetime = datetime.strptime(email_date_cleaned, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                # If timezone offset is missing, parse without %z
                email_datetime = datetime.strptime(email_date_cleaned, "%a, %d %b %Y %H:%M:%S")
            
            # Check if the email was received today
            if email_datetime.date() == datetime.now().date():
                # Print the subject of the email
                strSubject = msg.get("Subject")
                

                print(decode_header_value(strSubject), ",", email_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        pop3_connection.quit()