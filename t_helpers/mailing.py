import smtplib
from email.mime.text import MIMEText


class Mailing(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send(self, to_, subject, body):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_

        server.sendmail(self.username, to_, msg.as_string())
        server.quit()
