from unittest import TestCase
 
from core import FreqScrapper
 
class FreqScrapperTest(TestCase):
 
    def setUp(self):
 
        self.fs = FreqScrapper('https://www.washingtonpost.com/',["washingtonpost.com"])
 
    def test_get_freq_words(self):
        fw = self.fs.get_freq_words(2,10,1)        
        test_data = [('washington post', 11), ('the pandemic', 9)]
        # Verify the speed is 0 after stopping
        for t in test_data: 
            self.assertIn(t, fw)
