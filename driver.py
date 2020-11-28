from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re

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

        
    def _get_page_html(self,url):
        """ 
        Fetches page html. 
    
        Parameters: 
        url (string): url to be fetched 
    
        Returns: 
        string: Returns the fetched page html 
        """
        try:
            print("Fetching..",url)
            payload = {}
            #Set headers - so as not to be blocked
            headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            }

            response = requests.request("GET", url, headers=headers, data = payload)

            return response.text
        except Exception as e:
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


    def _compose_ngrams(self, string, n):
        """ 
        Generate ngrams from the string. 
    
        Parameters: 
        string (string): string from which ngrams need to be composed 
        n (int): ngram value
    
        Returns: 
        list: Returns list of n-grams
        """
        string = self._clean_normalize_string(string)

        #Remove empty tokens
        tokens = list(filter(None, string.split(" ")))


        # Use the zip function to help us generate n-grams
        # Concatentate the tokens into ngrams and return
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]


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
                if domain in href:
                    link_list.add(link['href'])
        return link_list

    
    def _get_sentence_ngrams_list(self,url,ngram,top,max_level,level_counter=1):
        """ 
        Generates the list of ngrams from individual sentences. 
    
        Parameters: 
        url (string): url to fetch content from
        level_counter(int): keeps track of levels scraped, while recursion

        Returns: 
        list: List of ngrams generated from all the sentences.
        """
        self.url_visited.append(url)
        ngramlist = []
        body = self._get_page_html(url)
        body = body.replace("<br />","") #Ignore html line breaks to let BeautifulSoup ignore it as different element/para 
        soup = BeautifulSoup(body, 'html.parser')
        #print(_find_filter_links(soup))

        texts = soup.findAll(text=True)
        texts_visible_tags = filter(self._is_visible_tag, texts)
        sentences = []
        for text in  filter(None, texts_visible_tags):
            sub_sentences = text.strip().lower().split(".") #Split on fullstop, to generate n-grams for each sentence and avoid geenrating ngrams across teh paras across different section
            sentences.extend(sub_sentences)

        for sentence in sentences:
            ngramlist.extend(self._compose_ngrams(sentence, ngram))
        for link in self._find_filter_links(soup,self.scrap_domains):
            if level_counter >= max_level:
                return ngramlist
            else:
                level_counter += 1
                if link not in self.url_visited:
                    ngramlist.extend(self._get_sentence_ngrams_list(link,ngram,top,max_level,level_counter))
        return ngramlist



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
        sentence_ngrams_list = self._get_sentence_ngrams_list(self.url, ngram,top,max_level)
        ngramfreq = [sentence_ngrams_list.count(ngram) for ngram in sentence_ngrams_list]
        unique_ngram_freq = set(zip(sentence_ngrams_list, ngramfreq))
        sorted_by_freq = sorted(unique_ngram_freq, key=lambda tup:tup[1],reverse = reverse )
        return sorted_by_freq[:top]
    
    
#fs = FreqScrapper('https://www.bing.com/',["bing.com"], ngram=2,top=10, max_level=1)
    
#fs.get_freq_words()
#Test data to check against view:source via browser
#[('know more', 6), ('healthcare it', 5), ('cures act', 5), ('ehr help', 4), ('go live', 4)