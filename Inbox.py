import imaplib
import email
from email.header import decode_header
import os
import speech_recognition as sr
import pyttsx3
import pyaudio
engine=pyttsx3.init()

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login('emailproject0521@gmail.com', 'Tyrion@1793')

atus, messages = imap.select("INBOX")
N = 3
messages = int(messages[0])
for i in range(messages, messages-N, -1):
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            engine.say("EMail number"+str(N-i))
            engine.runAndWait()
            engine.say("EMail is from:"+From)
            engine.runAndWait()
            engine.say("Subject OF the EMail is: "+subject)
            engine.runAndWait()
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" :
                        engine.say("Content of EMail is: "+body)
                        engine.runAndWait()
imap.close()
imap.logout()