from trafilatura import fetch_url, extract
print(extract(fetch_url('https://webkul.com/')))

from trafilatura.sitemaps import sitemap_search
urls = sitemap_search('https://webkul.com')
print(len(urls))

import time
import requests
import os
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from trafilatura.sitemaps import sitemap_search
from trafilatura import fetch_url, extract, extract_metadata




# def create_dataset(list_of_websites: list) -> pd.DataFrame:
#     """
#     Function that creates a Pandas DataFrame of URLs and articles.
#     """
#     data = []
#     for website in tqdm(list_of_websites, desc="Websites"):
#         urls = get_urls_from_sitemap(website)
#         for url in tqdm(urls, desc="URLs"):
#             html = fetch_url(url)
#             body = extract(html)
#             try:
#                 metadata = extract_metadata(html)
#                 title = metadata.title
#                 description = metadata.description
#             except:
#                 metadata = ""
#                 title = ""
#                 description = ""
#             d = {
#                 'url': url,
#                 "body": body,
#                 "title": title,
#                 "description": description
#             }
#             data.append(d)
#             time.sleep(0.5)
#     df = pd.DataFrame(data)
#     df = df.drop_duplicates()
#     df = df.dropna()

#     return df



def getTextFrom_url(url):
    data={}
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    data['url'] = url
    data['title'] = soup.title.string
    data['body'] = soup.get_text()
    return data
def get_Dataset(url):
    urls = sitemap_search(url)
    data = []
    for myurl in tqdm(urls, desc="URLs"):
        data.append(getTextFrom_url(myurl))
  
    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    df = df.dropna()
    return df


if __name__ == "__main__":
    # list_of_websites = [
    #     "https://webkul.com"
    # ]
    # df = create_dataset(list_of_websites)
    df = get_Dataset("https://webkul.com")
    df.to_csv("new_webkul_data.csv", index=False)

