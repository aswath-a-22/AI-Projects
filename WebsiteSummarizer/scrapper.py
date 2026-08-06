import requests #human-friendly third-party library used for sending HTTP requests to web servers. It allows your Python program to interact with the internet—whether you want to download webpage HTML, interact with REST APIs, or upload data
from bs4 import BeautifulSoup #Beautiful Soup is a popular Python library used to parse HTML and XML documents for web scraping

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_website_contents(url):
    # adds https:// if the user didn't include it.
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    #try and except is used to prevent the program from crashing if the website is not reachable.
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() #checks the https returncode status(200 - OK, 404 - Not Found, 500 - Internal Server Error, etc.) of the response. If the status code indicates an error (4xx or 5xx), it raises an HTTPError exception.
    except requests.exceptions.RequestException as e: #If there is any error while fetching the website, it will be caught here and the program will not crash.
        return f"Could not fetch the website. Error: {e}"

    soup = BeautifulSoup(response.text, "html.parser") 

    title = soup.title.string if soup.title else "No title found"

    """
    This removes elements that usually don't contain useful article text, unwanted tags from the webpage.
    """
    for tag in soup(["script", "style", "nav", "footer", "header", "img", "input"]):
        tag.decompose()  #Deletes the entire tag and its contents from the BeautifulSoup object.


    text = soup.get_text(separator="\n", strip=True) 
    return f"Title: {title}\n\nPage contents:\n{text}"
