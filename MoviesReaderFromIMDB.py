import selenium, time, re, PostgresSQL, unittest
from selenium import webdriver

class MoviesReader:
    def __init__(self):
        pass
    
    def checking_for_apostrophe(self, line:str) -> bool:
        for letter in line:
            if letter == "'":
                return True
        return False
    
    def return_working_line_with_SQL(self, line:str) -> str:
        return "".join(map(lambda letter : (letter * 2) if letter == "'" else letter, line))
    
class TestModule(unittest.TestCase):
    def test_apostrophe(self):
        self.assertEqual(MoviesReader().checking_for_apostrophe("Conan O'Brian"), True)
        self.assertEqual(MoviesReader().checking_for_apostrophe("Whitney Houston"), False)
        self.assertEqual(MoviesReader().checking_for_apostrophe("'"), True)
    
    def test_apostrophe_returned_line(self):
        self.assertEqual(MoviesReader().return_working_line_with_SQL("Conan O'Brian"), "Conan O''Brian")
        self.assertEqual(MoviesReader().return_working_line_with_SQL("Whitney Houston"), "Whitney Houston")
        self.assertEqual(MoviesReader().return_working_line_with_SQL("'"), "''")

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