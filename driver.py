from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re
import argparse
import logging
import nltk
logging.basicConfig(level=logging.INFO)
class FreqScrapper:
    """ 
    This is a class for Ngram frequency scrapper. 
      
    Attributes: 
        url (string): The base url to scrap. 
        scrap_domains (list of strings): domain to restrict the scrapping to. 
    """
    def __init__(self, url,scrap_domains):
        self.url = url
        self.scrap_domains = scrap_domains
        self.url_visited = []
        self.level_counter=1
        self.freq_dict = {}

        
    def _get_page_html(self,url):
        """ 
        Fetches page html. 
    
        Parameters: 
        url (string): url to be fetched 
    
        Returns: 
        string: Returns the fetched page html 
        """
        try:
            payload = {}
            #Set headers - so as not to be blocked
            headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            }

            response = requests.request("GET", url, headers=headers, data = payload)

            return response.text
        except Exception as e:
            logging.error("Error: {} ".format(e))
            return ""

    def _clean_normalize_string(self,string):
        """ 
        Clean and normalize the string to lowercase - replace alphanumeric chars with single spaces. 
    
        Parameters: 
        string (string): string to be cleaned 
    
        Returns: 
        string: Returns the cleaned string 
        """
        #find and replace alphanumeric chars with single spaces
        string = re.sub(r'[^a-zA-Z0-9\s]', ' ', string)
        return string.lower()


    def _compose_ngrams(self, raw, n):
        """ 
        Generate ngrams from the string. 
    
        Parameters: 
        string (string): string from which ngrams need to be composed 
        n (int): ngram value
    
        Returns: 
        list: Returns list of n-grams
        """
        
        raw = self._clean_normalize_string(raw)
        from nltk.util import ngrams    

        tokens = nltk.word_tokenize(raw)

        #Create your ngrams
        ngs = ngrams(tokens, n)

        #compute frequency distribution for all the bigrams in the text
        fdist = nltk.FreqDist(ngs)

        return fdist



    def _is_visible_tag(self,element):
        """ 
        Check if tag is visible text e.g: other than any style/scrip content. 
    
        Parameters: 
        element (BeautifulSoup element): Element to do check against

        Returns: 
        bool: Returns True/False
        """
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta','[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def _find_filter_links(self,soup, scrap_domains):
        """ 
        Find and filters href links to be scraped.
        . 
    
        Parameters: 
        soup (BeautifulSoup soup): soup to be
        scrap_domains(list): List of domain string to check against

        Returns: 
        list: List of href links
        """
        link_list = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            for domain in scrap_domains:
                if 'blog' in href:
                    continue
                if domain in href:
                    link_list.add(link['href'])
        return link_list

    
    def _get_master_sentence_list(self,url,ngram,top,max_level):
        """ 
        Generates the list of individual sentences for ngram generation. 
    
        Parameters: 
        url (string): url to fetch content from
        level_counter(int): keeps track of levels scraped, while recursion

        Returns: 
        list: List of ngrams generated from all the sentences.
        """
        self.url_visited.append(url)
        ngramlist = []
        body = self._get_page_html(url)
        logging.info('Fetched {} , Level: {}'.format(url, self.level_counter))
        body = body.replace("<br />","") #Ignore html line breaks to let BeautifulSoup ignore it as different element/para 
        soup = BeautifulSoup(body, 'html.parser')
        #print(_find_filter_links(soup))

        texts = soup.findAll(text=True)
        texts_visible_tags = filter(self._is_visible_tag, texts)
        page_sentences = []
        for text in  filter(None, texts_visible_tags):
            sub_sentences = text.strip().lower().split(".") #Split on fullstop, to generate n-grams for each sentence and avoid geenrating ngrams across teh paras across different section
            sub_sentences = [s for s in filter(None,sub_sentences )]
            page_sentences.extend(sub_sentences)
        raw = " ".join(page_sentences)
        logging.info('Computing ngram frequency for url {} ..'.format(url))
        fdist = self._compose_ngrams(raw, ngram)
        for k,v in fdist.items():
            word = k
            freq = v
            if word not in self.freq_dict:
                self.freq_dict[word] = freq
            else:
                self.freq_dict[word] += freq
        links =  self._find_filter_links(soup,self.scrap_domains)
        if len(links) > 0:
            self.level_counter += 1
            if self.level_counter == max_level+1:
                self.level_counter = 1
                return ngramlist
        for link in links:
            if link not in self.url_visited:
                self._get_master_sentence_list(link,ngram,top,max_level)
                
        return self.freq_dict



    def get_freq_words(self,ngram,top,max_level,sort="desc"):
        """ 
        Generates ngrams and their frequency. 
    
        Parameters: 
        ngram (int): ngram to generate
        top(int): To limit and control the top limit e.g: return top 10
        max_level(int): Max levels to scrap
        sort(string): sorting order

        Returns: 
        list of tuples: List of top tuples(<ngram>,<frequency>).
        """
        reverse = True
        if sort == "asc":
            reverse=False
        self._get_master_sentence_list(self.url, ngram,top,max_level)
        
        # raw = " ".join(self.master_sentence_list)
        # logging.info('Computing ngram frequency ..')
        # fdist = self._compose_ngrams(raw, ngram)
        
        sorted_by_freq = sorted( self.freq_dict.items() , key=lambda tup:tup[1],reverse = reverse )
        
        return sorted_by_freq[:top]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to scrap any website and fetch top ngrams with their frequency.")

    parser.add_argument('--url',type=str, help='Base url to scrap.', required=True)
    parser.add_argument('--scrap_domains',type=str,help='Comma seperated list of domains to restrict scraping and cralwing to.', required=True)
    parser.add_argument('--ngrams',type=int, help='ngrams value', required=True)
    parser.add_argument('--top',type=int, help='Top limit', required=True)
    parser.add_argument('--max_level',type=int, help='Max level to cralw & scrap', required=True)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    arguments = parser.parse_args()
    url = arguments.url
    scrap_domains = arguments.scrap_domains.split(",")
    ngrams = arguments.ngrams
    top = arguments.top
    max_level = arguments.max_level
    fs = FreqScrapper(url,scrap_domains)
    for row in fs.get_freq_words(ngrams,top, max_level):
        print(" ".join(row[0]),row[1] )
    #Test data to check against view:source via browser
    #[('know more', 6), ('healthcare it', 5), ('cures act', 5), ('ehr help', 4), ('go live', 4)