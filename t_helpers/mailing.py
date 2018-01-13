import smtplib


class Mailing(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send(self, to_, subject, msg):
        message = (
            'From: {}\nTo: {}\n'
            'Subject:{}\n\n{}'
        ).format(self.username, to_, subject, msg)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.username, to_, message)
        server.close()
