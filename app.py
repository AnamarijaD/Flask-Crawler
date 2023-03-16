from flask import Flask, request
from bs4 import BeautifulSoup

import pymongo
import json
import requests

app = Flask(__name__)


@app.route("/api/crawler")
def crawler():
    '''method for retrieving data from crawler_data mongo collection'''
    #creating a connection using MongoClient
    client = pymongo.MongoClient('mongodb://localhost:27017/')

    
    mydb = client["pythonDB"]
    collection = mydb.crawler_data
    documents = collection.find()

    #retrieving crawler_data collection
    return json.dumps([doc for doc in documents], indent=4, default=str)


@app.route("/api/crawler/trigger", methods=['POST'])
def crawler_trigger():
    import pandas as pd
    '''post method for scraping data from website and storing into mongodb'''

    res = requests.get('https://www.scottishmedicines.org.uk/medicines-advice/')

    #using BeautifulSoup to scrape html content
    soup = BeautifulSoup(res.content, 'html.parser')

    #finding all div tags with a specific class name
    tables = soup.find_all("div", class_="tabs__content")

    #creating lists for storing table data
    smc_list = []
    date_list = []
    medicine_list = []
    submission_list = []
    indication_list = []
    href_list = []

    #finding all tr tags from second to the last element
    rows = tables[0].find_all("tr")[1:]


    #looping through rows finding table data and appending it to a lists
    for row in rows:
        if row.find_all("td") is None:
            print("Found")
            break

        smc_list.append(row.find_all("td")[0].text.strip())
        date_list.append(row.find_all("td")[1].text.strip())
        medicine_list.append(row.find_all("td")[2].text.strip())
        submission_list.append(row.find_all("td")[3].text.strip())
        indication_list.append(row.find_all("td")[4].text.strip())
        href_list.append(row.find_all("td")[5].find('a', href=True)['href'])

    #making dataframe out of lists
    output = pd.DataFrame({'smc_id': smc_list, 'date': date_list, 'medicine': medicine_list,'submission': submission_list, 
            'indication':indication_list, 'link': href_list})

    #creating connection with database
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = client["pythonDB"]
    collection = mydb.crawler_data
    records = json.loads(output.T.to_json()).values()

    #inserting collection into database
    collection.insert(records)

    return "Success"



@app.route("/api/pricing_data")
def pricing_data():
    '''method for retrieving pricing data from mongodb'''
   
    #creating a connection using MongoClient
    client = pymongo.MongoClient('mongodb://localhost:27017/')

    mydb = client["pythonDB"]
    collection = mydb.pricing_data

    query = get_query(request.args)

    #finding data from collection that meets the query
    documents = collection.find(query)

    #retrieving filtered pricing_data collection
    return json.dumps([doc for doc in documents], indent=4, default=str)



def get_query(args):
    '''function for creating filter with request params'''
    query = {}

    if args.get("product_name") is not None:
        query["Product Name"] = args.get("product_name")
    if args.get("therapeutic_area") is not None:
        query["Therapeutic Area"] = args.get("therapeutic_area")
    if args.get("mnf") is not None:
        query["MNF"] = args.get("mnf")
    if args.get("route_of_administration") is not None:
        query["Route Of Administration"] = args.get("route_of_administration")
    return query
    

@app.route("/api/pricing_data/process")
def pricing_data_process():
    '''method for inserting excel data into mongodb'''
    import pandas as pd

    #reading excel table into dataframe
    dataframe = pd.read_excel('pricing_data.xlsx')

    #creating a connection using MongoClient
    client = pymongo.MongoClient('mongodb://localhost:27017/')

    mydb = client["pythonDB"]
    collection = mydb.pricing_data
    data = json.loads(dataframe.T.to_json()).values()

    #inserting collection into databse
    collection.insert_many(data)

    return "Success"

  
if __name__ == "__main__":
    app.run(debug=True)