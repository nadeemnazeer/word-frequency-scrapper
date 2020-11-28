from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re

class FreqScrapper:
    def __init__(self, url,scrap_domains, ngram=1,top=10, max_level=4):
        self.url = url
        self.scrap_domains = scrap_domains
        self.ngram = ngram
        self.top = top
        self.max_level= max_level
        self.url_visited = []

        
    def _get_page_html(self,url):
        try:
            print("Fetching..",url)
            payload = {}
            headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            }

            response = requests.request("GET", url, headers=headers, data = payload)

            return response.text
        except Exception as e:
            return ""

    def _clean_normalize_string(self,string):
        #find and replace alphanumeric chars with single spaces
        string = re.sub(r'[^a-zA-Z0-9\s]', ' ', string)
        return string.lower()


    def compose_ngrams(self, string, n):

        string = self._clean_normalize_string(string)

        #Remove empty tokens
        tokens = list(filter(None, string.split(" ")))


        # Use the zip function to help us generate n-grams
        # Concatentate the tokens into ngrams and return
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]


    def _get_visible_tag(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta','[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def get_internal_links(self,soup, scrap_domains):
        link_list = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            for domain in scrap_domains:
                if domain in href:
                    link_list.add(link['href'])
        return link_list

    
    def get_sentence_ngrams_list(self,url, level=1):
        self.url_visited.append(url)
        ngramlist = []
        body = self._get_page_html(url)
        body = body.replace("<br />","")
        soup = BeautifulSoup(body, 'html.parser')
        #print(get_internal_links(soup))

        texts = soup.findAll(text=True)
        texts_visible_tags = filter(self._get_visible_tag, texts)
        sentences = []
        for text in  filter(None, texts_visible_tags):
            sub_sentences = text.strip().lower().split(".")
            sentences.extend(sub_sentences)


        for sentence in sentences:
            ngramlist.extend(self.compose_ngrams(sentence, self.ngram))
        for link in self.get_internal_links(soup,self.scrap_domains):
            if level >= self.max_level:
                return ngramlist
            else:
                level += 1
                if link not in self.url_visited:
                    ngramlist.extend(self.get_sentence_ngrams_list(link,level))
        return ngramlist



    def get_freq_words(self):
        sentence_ngrams_list = self.get_sentence_ngrams_list(self.url)
        ngramfreq = [sentence_ngrams_list.count(ngram) for ngram in sentence_ngrams_list]
        unique_ngram_freq = set(zip(sentence_ngrams_list, ngramfreq))
        sorted_by_freq = sorted(unique_ngram_freq, key=lambda tup:tup[1], reverse=True)
        return sorted_by_freq[:self.top]
    
    
#fs = FreqScrapper('https://www.bing.com/',["bing.com"], ngram=2,top=10, max_level=1)
    
#fs.get_freq_words()
#Test data to check against view:source via browser
#[('know more', 6), ('healthcare it', 5), ('cures act', 5), ('ehr help', 4), ('go live', 4)