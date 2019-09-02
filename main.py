import Library
import Func
import time
import selenium

url = "https://www.myscore.ru/"
Library.browser.get(url)
Func.remove_advertising(Library.browser)
Library.time_match = 45
# Написать "LIVE" для парсинга лайв матчей. По умолчанию пасинг происходит по "Расписание"
Library.Select = "LIVE"
for times in range(100):
    try:
        Func.open_tabs(Library.browser)
        if Library.Select == "LIVE":
            Func.open_match(Func.select_match(Library.browser, times), Library.browser)
        else:
            Func.open_match(Func.select_match_schedule(Library.browser), Library.browser)
        print("Цикл пройден!")
        time.sleep(300)
    except selenium.common.exceptions.StaleElementReferenceException:
        print("Чет ошибка..")
