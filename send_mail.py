import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from helpers import get_db_connection
import sqlite3
from datetime import date

date = str(date.today())
print(date)
    
# Get data from DB
with get_db_connection() as conn:
    data = conn.execute(f"SELECT * FROM auctions WHERE date = ?", (date,))

# Setup SMTP server
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "maksgeardealz@gmail.com"
smtp_password = os.environ.get("GMAIL")

# create message
message = MIMEMultipart("alternative")
message["From"] = "maksgeardealz@gmail.com"
message["To"] = "marcin.barcz@icloud.com"
message["Subject"] = f"GearDealz {date}"

# set up the Jinja2 environment
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("mail_template.html")

# define the variables to pass to the template
heading = f"GearDealz {date}"
items = data

output = template.render(heading=heading, items=items)

# add a plain-text part to the message
text = f"GearDealz {date}"
html = output

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')
message.attach(part1)
message.attach(part2)
    
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.ehlo()
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(message["From"], message["To"], message.as_string())