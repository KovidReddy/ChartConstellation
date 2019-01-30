from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
# Define function to scrape data from the web
def get_web_data(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
    except RequestException as e:
        print('Error: {0} : {1}'.format(url, str(e)))


# Check if the response is HTML or not
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

# Fetch all the website urls
def excel_url_fetch(filepath):
    reader = pd.read_excel(filepath,sheet_name=0)
    url_list = []
    for elem in reader['Positive']:
        url_list.append(elem)
    return url_list

# Filter for Visible content
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'noscript']:
        return False
    if isinstance(element, Comment):
        return False
    return True

url_list = []
url_list = excel_url_fetch('C:\\Users\\pylak\\Documents\\Fall_2018\\DV\\Project\\Trump\\TEST.xlsx')
article_list = []
for url in url_list:
    raw_html = get_web_data(url)
    if raw_html:
    # fetch the html content in the tag format
        soup = BeautifulSoup(raw_html, 'html.parser')
    else:
        continue
    texts = soup.findAll(text = True)
    visible_text = filter(tag_visible, texts)

    article_list.append(u" ".join(t.strip() for t in visible_text))

df = pd.DataFrame({'a':article_list}).applymap(lambda x: x.encode('unicode_escape').
                 decode('utf-8') if isinstance(x, str) else x)
writer = pd.ExcelWriter('C:\\Users\\pylak\\Documents\\Fall_2018\\DV\\Project\\Trump\\TESTArticle.xlsx')
df.to_excel(writer, 'Sheet1', index=False)
writer.save()

