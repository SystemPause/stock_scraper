from bs4 import BeautifulSoup
import time
import requests
from prettytable import PrettyTable

def get_values(stocks):
    roic = []
    ey = []
    validStocks = []

    print("\n>>>Number of stocks to analyse: " + str(len(stocks)) + "\n")
    print("\n>>>Stock list:\n")
    print(stocks)
    print("\n")

    for stock in stocks:
        # Open the connection
        while True:
            try:
                quote_page = 'https://quotes.wsj.com/' + stock + '/financials'
                pageOne = requests.get(quote_page)
                soupOne = BeautifulSoup(pageOne.text, "html.parser")
                if pageOne.status_code == 200:
                    break
            except:
                continue

        roicValue = None
        eyValue = None
        try:
            # Get the ROIC
            name_box = soupOne.find(string='Return on Invested Capital')
            roicValue = cleanRoic(name_box.find_parents("span")[0].find_next_siblings('span')[0].findChildren()[0].string)

            # Get the Earnings Yield
            name_box = soupOne.find(string='P/E Ratio ')
            eyValue = cleanEy(name_box.find_parents("span")[0].find_next_siblings('span')[0].findChildren()[0].string)

        except:
            pass


        if roicValue != None and eyValue != None:
            roic.append(roicValue)
            ey.append(eyValue)
            validStocks.append(stock)
            print("\n" + stock + " " + str(roicValue) + " " + str(eyValue))

    return validStocks,roic,ey

def cleanRoic(roic):
    try:
        roic = float(roic)
    except:
        roic = 0.0
    return roic

def cleanEy(ey):
    try:
        ey = float(ey)
        ey = 1 / ey
    except:
        ey = 0.0
    return ey


def get_rank():
    rank = [[x,y,z] for x,y,z in zip(validStocks,roic,ey)]
    #print
    #print rank
    roicSorted = sorted(rank,key=lambda x:x[1],reverse = True)
    #print
    #print roicSorted
    eySorted = sorted(rank,key=lambda x:x[2],reverse = True)
    #print
    #print eySorted
    s = [];

    for i in range(len(roicSorted)):
        for j in range(len(eySorted)):
            if(roicSorted[i][0] == eySorted[j][0]):
                s.append([roicSorted[i][0],i + j])

    s = sorted(s,key=lambda x:x[1],reverse = False)

    table = PrettyTable(['Stock Name', 'Positive Index'])
    for el in s:
        table.add_row(el)

    print(table)


def get_values_from_yahoo(inputUrl):
    offset = 0
    estimatedResults = int(input("\n>>>Type the number of estimated results:\n"))

    temp = []
    while offset < estimatedResults:
        r  = requests.get(inputUrl + "?offset=" + str(offset))
        data = r.text
        soup = BeautifulSoup(data,"html.parser")
        for link in soup.find_all("a"):
            if link.get("class") == ['Fw(b)']:
                temp.append(str(link.text))
        offset += 100
    return temp


inputLink = input("\n>>>Type Yahoo Screener URL:\n")

stocks = get_values_from_yahoo(inputLink)

print("\n>>>Computing...\n")
print("###################################################")
start_time = time.time()

validStocks,roic,ey = get_values(stocks)

get_rank()

print("\nTotal execution time " + str((time.time() - start_time)))
print("###################################################")

print("\n Press ENTER to close the shell")

string = input()
string = ""
if string == "":
    exit()
