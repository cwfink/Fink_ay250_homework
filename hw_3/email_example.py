import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.utils import COMMASPACE, formatdate

def mail(sender, pwd, to, subject, text, files=[]):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = COMMASPACE.join(to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(text))
    for file in files:
        part = MIMEBase("application", "octet-stream")
        part.set_payload( open(file,"rb").read() )
        #Encoders.encode_base64(part)
        encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename='%s'"
                       % os.path.basename(file))
        msg.attach(part)
    # Note that we need to designate the remote SMTP server we want to use.
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.starttls()
    mailServer.login(sender, pwd)
    mailServer.sendmail(sender, to, msg.as_string())
    mailServer.close()

