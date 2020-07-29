#!/usr/bin/python3

import smtplib
import ssl
import urllib.request
import json
import datetime
from datetime import date


class Apartment():
    def __init__(self, sqrMtrs, area, dueDate, objectnumber):
        self.sqrMtrs = sqrMtrs
        self.area = area
        self.dueDate = dueDate
        self.objectnumber = objectnumber

    def getSqrMtrs(self):
        return self.sqrMtrs

    def getArea(self):
        return self.area

    def getDueDate(self):
        return self.dueDate

    def getObjectnumber(self):
        return self.objectnumber


def retrieveApartments(urlData, aptm):
    with urllib.request.urlopen(urlData) as url:
        dataFile = json.loads(url.read())

    availableApartments = []

    for obj in dataFile['product']:
        if obj['shortDescription'] == aptm:
            availableApartments.append(Apartment(
                obj['sqrMtrs'], obj['area'], obj['reserveUntilDate'], obj['objectnumber']))

    return availableApartments


def checkIfSent(objectnumber):
    logFile = open("/users/Albin/Desktop/log.txt", "r")
    return objectnumber in logFile.read()


def addToLog(objectnumber, dueDate):
    log = open("/users/Albin/Desktop/log.txt", "a")
    log.write(objectnumber + " " + dueDate + "\n")
    log.close()


def removeOld(date):
    with open("/users/Albin/Desktop/log.txt", "r") as log:
        lines = log.readlines()
    with open("/users/Albin/Desktop/log.txt", "w") as log:
        for line in lines:
            if str(date) not in line:
                log.write(line)


def removeAlOld():
    today = datetime.date.today()
    date_list = [today - datetime.timedelta(days=x) for x in range(7)]
    for date in date_list:
        removeOld(str(date))


def clearLog():
    log = open("/users/Albin/Desktop/log.txt", "w")
    log.write("")


def sendMail(finalApartments):
    port = 465  # For SSL
    mail = "testserver.albin@gmail.com"
    password = "Test1234!"

    sender_email = "testserver.albin@gmail.com"
    # , "al0235li-s@student.lu.se", "Rudin.malin@gmail.com", "lovesjftw@gmail.com"]
    receiver_emails = ["testserver.albin@gmail.com"]

    txt1 = """\
    Dags att ställa sig i kö :)

    Hej!
    Det finns nu 1 lägenhet med 4 rum på AFB.
    På {}, med en storlekt på {} m^2.
    Sista dagen att ställa sig i kö är {}.

    //Albins bot"""

    message1 = txt1.format(finalApartments[0].getArea(
    ), finalApartments[0].getSqrMtrs(), finalApartments[0].getDueDate()).encode()

    txt2 = """\
    Dags att ställa sig i kö :)

    Hej!
    Det finns nu {} lägenheter med 4 rum på AFB.
    På {}, med en storlekt på {} m^2.
    Sista dagen att ställa sig i kö är {}.
    
    //Albins bot"""
    area = []
    sqrm = []
    due = []
    for apt in finalApartments:
        area.append(apt.getArea())
        sqrm.append(apt.getSqrMtrs())
        due.append(apt.getDueDate())
    message2 = txt2.format(len(finalApartments), area, sqrm, due).encode()

    # Creat a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail, password)
        for email in receiver_emails:
            if len(finalApartments) == 1:
                server.sendmail(sender_email, email, message1)
            else:
                server.sendmail(sender_email, email, message2)


# Driver code
if __name__ == '__main__':
    removeAlOld()
    clearLog()

    apartments = retrieveApartments(
        "https://www.afbostader.se/redimo/rest/vacantproducts?lang=sv_SE&type=1", '4 Rum')

    finalApartments = []
    for apartment in apartments:
        if not checkIfSent(apartment.getObjectnumber()):
            addToLog(apartment.getObjectnumber(), apartment.getDueDate())
            finalApartments.append(apartment)

    if len(finalApartments) > 0:
        sendMail(finalApartments)
