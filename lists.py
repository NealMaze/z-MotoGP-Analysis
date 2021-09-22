import re
import tabula
from tabula.io import read_pdf
import fnmatch
from os import listdir, mkdir
from os import listdir, mkdir
import pdfplumber as plumb
import fnmatch
import pandas as pd
import os
import sys
from time import sleep
from winsound import Beep

rnd = "*"
lges = ["MotoGP", "Moto2", "Moto3", "MotoE", "500cc", "250cc", "125cc"]
manus = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA", "KAWASAKI", "BMW", "TRIUMPH", "HUSQVARNA", "KALEX",
         "BOSCOSCURO", "MV AGUSTA", "NTS", "GAS GAS", "MV", "GASGAS", "SPEED UP"]
nats = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR", "AUT",
        "ARG", "CZE", "TUR", "BEL", "FIN", "POL", "AND", "KAZ"]
ses = ["RACE", "RACE2", "RAC", "RAC2", "Q2", "Q1", "QP_", "QP1", "QP2", "WUP", "FP1", "FP2", "FP3", "FP4", "EP"]
yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008",
       "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]
intes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
         "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36",
         "37", "38", "39"]
tires = ["Slick-Soft", "Slick-Medium", "Slick-Hard", "Wet-Soft", "Wet-Medium", "Wet-Hard", "missing", "Wet-ExtraSof"]
days = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]
months = ["january" "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december", "January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]

rootDir = "C:/Users/LuciusFish/Desktop/motoFiles/"
pdfDir = (f"{rootDir}pdfFiles/")
csvDir = (f"{rootDir}csvFiles/")
csvSesDir = (f"{csvDir}sessions/")
csvRidersDir = (f"{csvDir}riders/")
csvWeatherDir = (f"{csvDir}weather/")
csvTracksDir = (f"{csvDir}tracks/")
csvSeasonDir = (f"{csvDir}wholeSeasons/")

position = re.compile("^\d{1,2}(st|nd|rd|th)$")
name = re.compile("^[\-a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.']+$")
avgSpeed = re.compile("^\d{2,3}[.]\d{1}$")
inte = re.compile("^\d{1,2}\d{0,1}$")
integ = re.compile("^\d{1,2}\d{0,1}$")
yrReg = re.compile("^\d{4}$")
bSecTime = re.compile("^\d\d\d\d[.][.]\d\d\d\d\d\d$")
bLapTime = re.compile("^\d[']\d\d\d\d[.][.]\d\d\d\d\d\d$")

wLap = re.compile("^\d{0,1}\d{0,1}[']{0,1}[']{0,1}\d\d\d\d[.][.]\d\d\d\d\d\d")
secTime = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}$")
lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
pitTime = re.compile("^\d{1,2}[:]\d\d[']\d\d[.]\d\d\d$")
