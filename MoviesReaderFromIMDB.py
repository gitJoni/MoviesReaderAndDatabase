import selenium, time, re, PostgresSQL, unittest
from selenium import webdriver

class MoviesReader:
    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.chrome.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250") # Starting search from Top 250 page
    
    def checking_for_apostrophe(self, line:str) -> bool:
        for letter in line:
            if letter == "'":
                return True
        return False
    
    def return_working_line_with_SQL(self, line:str) -> str:
        return "".join(map(lambda letter : (letter * 2) if letter == "'" else letter, line))
    
    def start_search_from_page(self, page:str) -> None:
        self.chrome.get(page)
        
    def get_director_element(self) -> str:
        try:
            return self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a').text
        except Exception as error:
            print(error, "\nRan to an error while fetching director element, trying another xpath.")
        try:
            return self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[2]/a').text
        except Exception as error:
            print(error, "\nRan to an another error, could not fetch director element")
            return error
    
    def get_rating_element(self) -> str:
        try:
            return float(self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span').text)
        except Exception as error:
            return error
        
    def get_title_element(self) -> str:
        try:
            return self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1').text.split(" (")[0]
        except Exception as error:
            return error
    
    def get_year_element(self) -> int:
        try:
            return int(self.chrome.find_element_by_xpath('//*[@id="titleYear"]/a').text)
        except Exception as error:
            return error
    
    def sleep_awhile_for_pages_to_download(self, how_long:float or int) -> None:
        time.sleep(how_long)
    
    def run_program(self):
        pass
        
class TestModule(unittest.TestCase):
    Reader = MoviesReader()
    def test_apostrophe(self):
        self.assertEqual(self.Reader.checking_for_apostrophe("Conan O'Brian"), True)
        self.assertEqual(self.Reader.checking_for_apostrophe("Whitney Houston"), False)
        self.assertEqual(self.Reader.checking_for_apostrophe("'"), True)
    
    def test_apostrophe_returned_line(self):
        self.assertEqual(self.Reader.return_working_line_with_SQL("Conan O'Brian"), "Conan O''Brian")
        self.assertEqual(self.Reader.return_working_line_with_SQL("Whitney Houston"), "Whitney Houston")
        self.assertEqual(self.Reader.return_working_line_with_SQL("'"), "''")
    
    def test_timing(self):
        self.assertEqual(self.Reader.sleep_awhile_for_pages_to_download(2), None)
        self.assertEqual(self.Reader.sleep_awhile_for_pages_to_download(0.2), None)

if __name__ == "__main__":
    unittest.main()

"""
# Starting to search movies from Cast Away movie.
chrome = webdriver.Chrome()
chrome.get("https://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=8T22EMXCZBPAENNVDGBT&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1")
postgres_lista = PostgresSQL.Postgres()
i = 1
time.sleep(1)
while i <= 250:
    try:
        director_element = chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a').text
    except Exception:
        director_element = chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[2]/a').text
    try:
        rating_element = float(chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span').text)
        title_element = chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1').text.split(" (")[0]
        title_has_apostrophe = False
        for letter in title_element:
            if letter == "'":
                title_has_apostrophe = True
        if title_has_apostrophe:
            title_element = ''.join(map(lambda letter : (letter * 2) if letter == "'" else letter, title_element))
        director_has_apostrophe = False
        for letter in director_element:
            if letter == "'":
                director_has_apostrophe = True
        if director_has_apostrophe:
            director_element = ''.join(map(lambda letter : (letter * 2) if letter == "'" else letter, director_element))
        year_element = int(chrome.find_element_by_xpath('//*[@id="titleYear"]/a').text)
        if director_element == "Lana Wachowski":
            director_element = "Lana and Lilly Wachowski"
        postgres_lista.setToList(title_element, director_element, rating_element, year_element)
        chrome.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
        time.sleep(3)
        i += 1
        chrome.find_element_by_xpath(f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{i}]/td[2]/a').click()
        time.sleep(1)
    except Exception as err:
        print(err)
        break
postgres_lista.sendToDatabase()
"""