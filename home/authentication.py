import pickle
import base64
import googleapiclient.discovery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


creds = pickle.load(open('gmail.pickle', 'rb'))
service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
def sendotp(receiver,otp):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Otp for the youthblog'
    msg['From'] = f'theyouthblog@gmail.com'
    msg['To'] = receiver
    msgPlain =  "The one time password (OTP) to sign up at THE YOUTH BLOG is " +str(otp)
    msg.attach(MIMEText(msgPlain, 'plain'))

    # msgHtml = '<b>This is my first email!</b>'
    # msg.attach(MIMEText(msgHtml, 'html'))

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}


    message = (
        service.users().messages().send(
            userId="me", body=body).execute())
    print('Message Id: %s' % message['id'])







