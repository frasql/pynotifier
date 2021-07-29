import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import config_dict
   
        
username = config_dict.get("MAIL_USER")
password = config_dict.get("MAIL_PASSWORD")

# send mail to single/multiple user/s
def send_mail(text: str ='Email Body', subject: str = 'Hello', from_email: str ='Name <address>', to_emails=None, html=None) -> None:
    assert isinstance(to_emails, list)

    # create message
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] =  ','.join(to_emails)
    msg['Subject'] = subject

    # attach text
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    
    # attach html
    if html is not None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
    # login to smtp server
    with smtplib.SMTP(host='smtp.domain.com', port=587) as server:
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_email, to_emails, msg)

    
def convert_datetime(datetime_obj):
    milliseconds = datetime_obj.strftime("%Y-%m-%d %H:%M:%S,%f").split(",")[1].replace("0", "")
    date_to_search = datetime_obj.strftime("%Y-%m-%d %H:%M:%S,%f").split(",")[0]
            
    if milliseconds:
        date_to_search += f",{milliseconds}"
        
    return date_to_search

def convert_time(time_obj):
    milliseconds = time_obj.strftime("%H:%M:%S,%f").split(",")[1].replace("0", "")
    time_to_search = time_obj.strftime("%H:%M:%S,%f").split(",")[0]
    if milliseconds:
        time_to_search += f",{milliseconds}"
        
    return time_to_search
    

