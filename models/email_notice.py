#!/usr/bin/python3
# coding: utf-8

import base64
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def send_email(address, content):
    from_email = "dumingzhe@126.com"
    from_email_pwd = base64.b64decode(b'Wno5NXNwaXJ0c29uZw==').decode("utf-8")
    to_email = address
    smtp_server = "smtp.126.com"

    print(content)
    msg = MIMEText("<html><body><h3>hello</h3><p>hello, send by python %s </p></body></html>" % content, "html", "utf-8")
    msg["From"] = format_addr("%s" % (from_email))
    msg["To"] = format_addr("%s" % (to_email))
    msg["Subject"] = Header("python email", "utf-8").encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_email, from_email_pwd)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()

if __name__ == "__main__":
    send_email("dumingzhex@gmail.com", "Hello")