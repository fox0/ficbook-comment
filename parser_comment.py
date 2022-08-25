import logging
import requests
from bs4 import BeautifulSoup

url_template = 'https://ficbook.net/authors/%d/comments'

log = logging.getLogger(__name__)


def main(author_id, pages):
    url = url_template % author_id
    s = requests.Session()
    s.headers.update({
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    })
    for p in range(pages, 0, -1):
        r = s.get(url, params=dict(p=p))
        assert r.status_code == 200
        soup = BeautifulSoup(r.text, 'lxml')
        for i in reversed(soup.find_all('div', {'class': 'comment-content'})):
            link = i.find('div', {'class': 'comment_link_to_fic'})
            print('https://ficbook.net' + link.a['href'])
            print('Фанфик: ' + link.text.strip())
            print(i.find('time').text.strip())
            print()
            print(i.find('div', {'class': 'comment_text'}).text.strip())
            print()
            print('---------')
            print()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s %(funcName)s():%(lineno)d: %(message)s',
                        level=logging.DEBUG)
    main(author_id=1880805, pages=150)
