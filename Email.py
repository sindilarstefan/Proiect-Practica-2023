import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

EMAIL_ADDRESS = "testproiect2023@gmail.com"
PASSWORD = "uyeeojszslhkyshu"


class SendMail(threading.Thread):
    def __init__(self, to, subject, message):
        threading.Thread.__init__(self)
        self.to = to
        self.subject = subject
        self.message = message

    def run(self):
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.subject
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = self.to
            msg.attach(MIMEText(self.message, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS, PASSWORD)
            server.sendmail(EMAIL_ADDRESS, self.to, msg.as_string())
            server.quit()
            print("Email sent successfully to:", self.to)
        except Exception as e:
            print("An error occurred while sending email to", self.to, ":", str(e))
