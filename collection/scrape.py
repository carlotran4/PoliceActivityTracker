import sqlite3
import os.path
import requests
import datetime
from bs4 import BeautifulSoup

def scrape():
    db = None
    if not os.path.exists("data.db"):
        db = init()
    else:
        db = sqlite3.connect("data.db")
    cursor = db.cursor()

    highest_cfs = cursor.execute('''SELECT MAX(CFS_NUMBER) FROM callInfo''').fetchone()[0]  
    if highest_cfs is None: highest_cfs = 0
    day = datetime.datetime.today()
    #Including the exact time of today() will result in false addition when generating timestamps.
    day = day.replace(microsecond=0,second=0, minute=0, hour=0)
    
    while insert_to_db(day, highest_cfs, db):
        day-= datetime.timedelta(days=1)
        print("Scraping "+ day.strftime("%m/%d/%Y"))
    
    db.commit()


def init() -> sqlite3.Connection:
    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    cursor.execute('''
               CREATE TABLE callInfo(
                CFS_NUMBER INTEGER,
                CALL_DATETIME TIMESTAMP,
                ADDRESS TEXT,
                APPT_NUMBER TEXT,
                AGENCY TEXT,
                DISPOSITION TEXT,
                CALLTYPE TEXT,
                DETAILS TEXT,
                LATITUDE DECIMAL(10,8),
                LONGITUDE DECIMAL(11,8),
                CAN_GEOCODE BOOLEAN  
               )
               ''')
    
    cursor.execute('''
               CREATE TABLE arrestInfo(
                CFS_NUMBER INTEGER,
                INCIDENT_ID TEXT,
                OFFENDER_NAME TEXT,
                JAILED BOOLEAN,
                OFFICER_NAME TEXT,
                CHARGES TEXT
               )
               ''')
    return db

def getCrimeData(row:BeautifulSoup) -> list:
    all_cols = row.find_all("td")
    data_cols = [all_cols[1],all_cols[3],all_cols[5]]
    data = list()
    for col in data_cols:
        text = col.text
        text = text.split("\n")
        data += text
    return data

def insert_to_db(day: datetime.datetime,stop:int, db:sqlite3.Connection ) -> bool:
    """Given a date, insert all call for service data in the given db,
    but stop if the cfs number gets lower than the given stop. 
    Return false if stopped at any point.

    Args:
        day (datetime.datetime): Day of the data to add to the database
        stop (int): All data higher than stop will be added, but nothing
        equal to or lower.
        db (sqlite3.Connection): Connection object to the target database.

    Returns:
        bool: returns false if stopped at any point due to cfs numbers going below stop
    """
    form_data = {'SelectedDate': day.strftime("%m/%d/%Y"),
                 "SelectedAgency":"All"}
    page = requests.post("http://www.jecc-ema.org/jecc/jecccfs.php", form_data)
    soup = BeautifulSoup(page.content,"html.parser")
    table_rows = soup.find_all("table")[1].find_all("tr")
    for (i, row) in enumerate(table_rows):
        table_rows[i] = getCrimeData(table_rows[i])
    
    if(not table_rows): return False
    cursor = db.cursor()
    # Since rows on site are earliest to latest, it needs to be reversed to match latest to earliest
    # in order to stop at the correct CFS
    for row in reversed(table_rows):
        if(int(row[0]) <= stop): return False
        cfs = int(row[0])
        address = row[1]
        calltype = row[2]
        time =  day + datetime.timedelta(hours = int(row[3][0:2]), minutes= int(row[3][3:5]))
        apptno = row[4]
        agency = row[5]
        disposition = row[6]
        incident_id = row[7]
        
        cursor.execute('''INSERT INTO callInfo(CFS_NUMBER, CALL_DATETIME, ADDRESS, APPT_NUMBER, AGENCY, DISPOSITION, CALLTYPE)
                       VALUES (?,?,?,?,?,?,?)''', 
                       (cfs, time, address, apptno, agency, disposition, calltype))
        
        if(len(incident_id)>0):
            cursor.execute('''INSERT INTO arrestInfo(CFS_NUMBER, INCIDENT_ID)
                           VALUES (?, ?)''', (cfs, incident_id))
    
    return True
    
    

scrape()