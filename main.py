import Library
import Func
import time
import selenium

url = "https://www.myscore.ru/"
Library.browser.get(url)
# Удаляем рекламу, чтоб она не мешала открывать вкладки
Func.remove_advertising(Library.browser)
Library.time_match = 23
# Написать "LIVE" для парсинга лайв матчей. По умолчанию пасинг происходит по "Расписание"
Library.Select = ""
x = 0

if Library.Select != "LIVE":
    try:
        Func.open_match(Func.select_match_schedule(Library.browser), Library.browser)
    except selenium.common.exceptions.StaleElementReferenceException:
        pass
else:
    while x < 10:
        Func.open_tabs(Library.browser)
        Func.open_match(Func.select_match(Library.browser), Library.browser)
        print("Цикл пройден")
        time.sleep(150)
