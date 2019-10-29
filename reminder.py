import requests
import re
from bs4 import BeautifulSoup
import smtplib, ssl
import getpass
import time

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
password = "INSERT GOOGLE APP PASSWORD"
sender_email = "INSERT SENDER EMAIL"
receiver_email = "INSERT RECEIVER EMAIL"

# Query for SOFE 3950U class
url ="https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec?TRM=U&term_in=202001&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=SOFE&sel_crse=3950U&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a"


# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
 
    server.login(sender_email, password)
    while True:
            
        # Get information from url
        response = requests.get(url)
        print("Status: ", response.status_code)
            
        # Parse html
        soup = BeautifulSoup(response.text, 'html.parser')

        # Retrieve remaing slots
        remaining = str(soup.findAll("td", "dbdefault")[2].decode_contents())   
        remaining = int(re.search("[0-9]{0,}", remaining).string)

        # Message sent to user
        message = """\
                Subject: Slot Available 
                \

                There is """+str(remaining) + """ slot available
                This message is sent from Python."""


        if remaining > 0:
            server.sendmail(sender_email, receiver_email, message)
            print("Mail sent")
            
        time.sleep(900)                         # sleep for 15 minutes


