import selenium, time, re, PostgresSQL
from selenium import webdriver


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