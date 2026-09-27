import json,time,sys,urllib.robotparser
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl, Field
BASE='https://books.toscrape.com/'; HEADERS={'User-Agent':'FlyRank-Intern-PoliteScraper/1.0 (educational)'}
class Book(BaseModel):
    title:str=Field(min_length=1); price:float=Field(ge=0); currency:str='GBP'; availability:str; rating:int=Field(ge=1,le=5); url:HttpUrl

def scrape(pages=3,delay=0.4):
    rp=urllib.robotparser.RobotFileParser(BASE+'robots.txt'); rp.read(); out=[]
    for page in range(1,pages+1):
        url=BASE+('catalogue/page-%d.html'%page if page>1 else 'index.html')
        if not rp.can_fetch(HEADERS['User-Agent'],url): raise RuntimeError('blocked by robots.txt')
        r=requests.get(url,headers=HEADERS,timeout=10); r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser')
        for x in soup.select('article.product_pod'):
            try:
                rating={'One':1,'Two':2,'Three':3,'Four':4,'Five':5}[x.select_one('.star-rating')['class'][1]]
                out.append(Book(title=x.h3.a['title'],price=float(x.select_one('.price_color').text.replace('£','')),availability=x.select_one('.availability').get_text(' ',strip=True),rating=rating,url=requests.compat.urljoin(url,x.h3.a['href'])))
            except (KeyError,TypeError,ValueError): continue
        time.sleep(delay)
    return out
if __name__=='__main__':
    try: data=[x.model_dump(mode='json') for x in scrape()]; Path('books.json').write_text(json.dumps(data,indent=2)); print(f'wrote {len(data)} checked books')
    except Exception as e: print(f'scrape failed safely: {e}',file=sys.stderr); sys.exit(1)
