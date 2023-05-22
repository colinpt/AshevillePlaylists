from lxml import etree
from webDriver import getWebpageAsDom, getDomString
import datetime

def standardizeDate(dateString: str) -> str:
    #TODO add a year if date < current date (may not apply to all sites)
    dateParts = dateString.split(' ')
    fullDateString = dateParts[0][0:3] + ' ' + dateParts[1] + ' ' + datetime.date.today().strftime('%Y')
    for format in ['%b %d %Y', '%B %d %Y']:
        try:
            return datetime.datetime.strptime(fullDateString, format).strftime('%Y-%m-%d')
        except ValueError:
            pass
    raise ValueError(f'no valid date format found: {dateString}')

def getShowData() -> dict:
    dom = getWebpageAsDom('https://theorangepeel.net/events/')
    titleXpath = "//div[contains(@class, 'generalView')]/descendant::a[@id='eventTitle']//h2"
    dateXpath = "//div[contains(@class, 'generalView')]/descendant::div[@id='eventDate']"

    shows = []
    showCount = len(dom.xpath(titleXpath))
    
    for i in range(showCount):
        date = standardizeDate(getDomString(dom, dateXpath, i).split(',')[1].strip())
        shows.append({ 'artist' : getDomString(dom, titleXpath, i), 
                       'date'   : date})
    return shows
