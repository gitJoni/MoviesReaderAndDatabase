import selenium, time, re, PostgresSQL, unittest
from selenium import webdriver

class MoviesReader:
    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.chrome.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250") # Starting search from Top rated page
        self.size = int(self.chrome.find_element_by_xpath('//*[@id="main"]/div/span/div/div/div[3]/div/div/div[2]/span').text)
        self.postgres_lista = PostgresSQL.Postgres()
    
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
            director = self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a').text
        except Exception as error:
            print(error, "\nRan to an error while fetching director element, trying another xpath.")
            try:
                director = self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[2]/a').text
            except Exception as error:
                print(error, "\nRan to an another error, could not fetch director element")
                return False
        if self.checking_for_apostrophe(director):
            return self.return_working_line_with_SQL(director)
        else:
            return director
    
    def get_rating_element(self) -> str:
        try:
            return float(self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span').text)
        except Exception as error:
            return error
        
    def get_title_element(self) -> str:
        try:
            title = self.chrome.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1').text.split(" (")[0]
        except Exception as error:
            return error
        if self.checking_for_apostrophe(title):
            return self.return_working_line_with_SQL(title)
        else:
            return title
    
    def get_year_element(self) -> int:
        try:
            return int(self.chrome.find_element_by_xpath('//*[@id="titleYear"]/a').text)
        except Exception as error:
            return error
    
    def sleep_awhile_for_pages_to_download(self, how_long:float or int) -> None:
        time.sleep(how_long)
    
    def run_program(self):
        self.sleep_awhile_for_pages_to_download(2)
        for i in range(self.size):
            self.chrome.find_element_by_xpath(f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{i + 1}]/td[2]/a').click()
            self.sleep_awhile_for_pages_to_download(2)
            self.postgres_lista.setToList(self.get_title_element(), self.get_director_element(), self.get_rating_element(), self.get_year_element())
            self.chrome.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
            self.sleep_awhile_for_pages_to_download(2)
        self.postgres_lista.sendToDatabase()
        
class TestModule(unittest.TestCase):
    def __init__(self):
        self.Reader = MoviesReader()
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
    MoviesReader().run_program()