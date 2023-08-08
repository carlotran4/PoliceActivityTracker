import requests
from constants import API_KEY
import sqlite3

def geocode():
    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    #Separate cursor to insert values so as not to mess up iteration.
    insertionCursor = db.cursor()
    
    cursor.execute('''
                   SELECT CFS_NUMBER, ADDRESS FROM callInfo WHERE LATITUDE IS NULL
                   ''')
        
    for(cfs, address) in cursor:
        address = getAddress(address)
        while(True):
            try:
                request = requests.get(f"https://api.geocod.io/v1.7/geocode?q={address}&api_key={API_KEY}")
                break
            except (requests.exceptions.ConnectTimeout,requests.exceptions.ConnectionError):
                input("Wifi is down. Please reconnect and press enter to continue")
            
        print(request.status_code)
        
        if (request.status_code == 429 or request.status_code == 403):
            print("Reached daily limit")
            break
        if (request.status_code == 422):
            print(f"Address unprocessable. Address: {address}")
            continue
        
        if (noResults(request)):
            print(f"No results found. Address: {address}")
            continue
        
        if not locationIsAccurate(request):
            print(f"Address not considered accurate. Address:{address}")
            continue
        
        
        
        latitude = request.json()["results"][0]["location"]["lat"]
        longitude = request.json()["results"][0]["location"]["lng"]
        
        insertionCursor.execute('''
                       UPDATE callInfo
                       SET LATITUDE = ?, LONGITUDE = ?
                       WHERE CFS_NUMBER = ?
                       ''', (latitude, longitude, cfs))
    print("Finished. Committing to database.")
    db.commit()

def getAddress(address: str) -> str:
    """Reformats address from blotter to be more accurate when working
    with geocodio.
    
    Args:
        address (str): Address from data.db

    Returns:
        str: Formatted string that works better with geocodio
    """
    return address + ", IA"

def locationIsAccurate(data:requests.Response) -> bool:
    """Determines if the latitude & longitude value given by geocodio is 
    feasible.

    Args:
        data (requests.Response): http Response.

    Returns:
        bool: True if accurate, false otherwise.
    """
    accuracyType = data.json()["results"][0]["accuracy_type"]
    accuracy = data.json()["results"][0]["accuracy"]
    address = data.json()["results"][0]["formatted_address"]
    print(f"Address: {address}  Accuracy: {accuracy}  accuracyType: {accuracyType}")
    if accuracyType == "place" or accuracyType == "county" or accuracyType == "state":
        return False
    
    return True

def noResults(data: requests.Response) -> bool:
    """Returns true if a geocodio response does not have any results

    Args:
        data (requests.Response): HTTP Response for geocodio

    Returns:
        bool: True if there are no results
    """
    if(data.json()["results"]):
        return False
    return True
    
geocode()
