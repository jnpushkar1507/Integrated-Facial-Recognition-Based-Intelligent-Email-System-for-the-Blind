import smtplib
import speech_recognition as sr
import pyttsx3
import pyaudio
from email.message import EmailMessage
listener=sr.Recognizer()
engine=pyttsx3.init()

email_list = {
    'pushkar' : 'pushkarjain2002@gmail.com',
    'michael' : 'jn.pushkar1507@gmail.com'
}

def talk(text):
    engine.say(text)
    engine.runAndWait()

def get_info():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice=listener.listen(source,timeout=1,phrase_time_limit=5)
            info=listener.recognize_google(voice)
            print(info)
            return info.lower()
    except:
        pass

def send_email(reciever,subject,message):
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('emailproject0521@gmail.com', 'Tyrion@1793')
    email=EmailMessage()
    email['From'] = 'emailproject0521@gmail.com'
    email['To'] = reciever
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)

def get_email_info():
    talk('To whom you want to send email')
    name = get_info()
    if name in email_list:
        reciever = email_list[name]
    else:
        reciever = name
    print(reciever)
    talk('what is the subject of your email?')
    subject = get_info()
    talk('tell me the content of your email?')
    message = get_info()
    talk('Sending your Email')
    send_email(reciever,subject,message)
    talk('E-Mail Sent!')
    talk('Do You want to send Another Email?')
    send_more = get_info()
    if 'yes' in send_more:
        get_email_info()
    talk('Do You want to read your E-mails?')
    read_email = get_info()
    if 'yes' in read_email:
        import Inbox.py

get_email_info()