from lxml import etree
from webDriver import getWebpageAsDom, getDomString
import datetime

def standardizeDate(dayString: str, monthString: str, yearString: str) -> str:
    fullDateString = monthString + ' ' + dayString + ' ' + yearString
    for format in ['%b %d %Y', '%B %d %Y']:
        try:
            return datetime.datetime.strptime(fullDateString, format).strftime('%Y-%m-%d')
        except ValueError:
            pass
    raise ValueError(f'no valid date format found: {monthString} {dayString} {yearString}')

def getShowData() -> dict:
    excludedSubtitles = ['tribute']
    dom = getWebpageAsDom('https://salvagestation.com/events/')
    titleXpath = "//div[contains(@class, 'event-list-wrapper')]/descendant::div[@class = 'event-list-title']"
    subtitleXpath = "//div[contains(@class, 'event-list-wrapper')]/descendant::div[@class = 'event-list-supporting']"
    dayXpath = "//div[contains(@class, 'event-list-wrapper')]/descendant::div[contains(@class, 'event-list-number')]"
    monthXpath = "//div[contains(@class, 'event-list-wrapper')]/descendant::div[contains(@class, 'event-list-month')]"
    yearXpath = "//div[contains(@class, 'event-list-wrapper')]/descendant::div[contains(@class, 'event-list-year')]"

    shows = []
    showCount = len(dom.xpath(titleXpath))
 
    for i in range(showCount):
        subtitle = getDomString(dom, subtitleXpath, i)
        if not any(x in subtitle.lower() for x in excludedSubtitles):
            day = getDomString(dom, dayXpath, i)
            month = getDomString(dom, monthXpath, i)
            year = getDomString(dom, yearXpath, i)
            date = standardizeDate(day, month, year)
            artist = getDomString(dom, titleXpath, i)
            shows.append({ 'artist' : artist, 
                        'date'   : date})
    return shows
