#!/usr/bin/python3

import smtplib, ssl
import urllib.request, json

def start(urlData):
    availableApartment = False
    sqrMtrs = []
    area = []
    dueDate = []
    
    with urllib.request.urlopen(urlData) as url:
        dataFile = json.loads(url.read())

    for obj in dataFile['product']:
        if obj['shortDescription'] == '4 Rum':
            availableApartment = True
            sqrMtrs.append(obj['sqrMtrs'])
            area.append(obj['area'])
            dueDate.append(obj['reserveUntilDate'])

    if availableApartment:
        sendMail(sqrMtrs, area, dueDate)




def sendMail(sqrMtrs, area, dueDate):
    port = 465 #For SSL
    mail = "testserver.albin@gmail.com"
    password = "Test1234!"

    sender_email = "testserver.albin@gmail.com"
    #receiver_email = "testserver.albin@gmail.com"
    receiver_email1 = "al0235li-s@student.lu.se"
    receiver_email2 = "Rudin.malin@gmail.com"
    receiver_email3 = "lovesjftw@gmail.com"
    
    txt = """\
    Subject: Dags att ställa sig i kö!

    Hej!
    Det finns nu {} lägenhet/er med 4 rum på AFB.
    På {}, med en storlekt om {} m2.
    Sista dagen att ställa sig i kö är {}.
    //Albins bot
    
    btw vi kommer får mejl fram tills lägenheterna försvinner från AFB som det är nu. Sorry är lat <3"""

    message = txt.format(len(sqrMtrs), area, sqrMtrs, dueDate).encode()

    # Creat a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail, password)
        server.sendmail(sender_email, receiver_email1, message)
        server.sendmail(sender_email, receiver_email2, message)
        server.sendmail(sender_email, receiver_email3, message)


# Driver code 
if __name__ == '__main__': 
    start("https://www.afbostader.se/redimo/rest/vacantproducts?lang=sv_SE&type=1")
