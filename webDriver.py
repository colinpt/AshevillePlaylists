import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def getDomString(dom: etree.HTML, xpath: str, index: int) -> str:
    return dom.xpath(xpath)[index].xpath("string()").strip()

def getWebpageAsDom(url: str) -> etree.HTML:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    webpage = requests.get(url, headers=headers)
    soup = str(BeautifulSoup(webpage.content, "html.parser"))    
    return etree.HTML(soup)

def getSpotifyAuthCode(creds: dict) -> str:
    query_params = {
        "response_type": "code",
        "client_id": creds['clientId'],
        "scope": 'playlist-modify-public playlist-modify-private',
        "redirect_uri": 'http://localhost:3000',
        "state": creds['state']
    }

    url = "https://accounts.spotify.com/authorize?" + requests.compat.urlencode(query_params)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.find_element('id', 'login-username').send_keys(creds['spotifyUsername'])
    driver.find_element('id', 'login-password').send_keys(creds['spotifyPassword'])
    loginButton = driver.find_element('id', 'login-button')
    loginButton.click()

    WebDriverWait(driver, 30).until(
        staleness_of(loginButton)
    )

    try:
        authButton = driver.find_element(By.XPATH, "//button[@data-testid = 'auth-accept']")
        authButton.click()
        WebDriverWait(driver, 30).until(
            staleness_of(authButton)
        )
    except NoSuchElementException:
        pass

    return driver.current_url.split('code=')[1].split('&state')[0]