import Library
import Func
import analysis
import time
import selenium

url = "https://www.myscore.ru/"
Library.browser.get(url)
# Удаляем рекламу, чтоб она не мешала открывать вкладки
Func.remove_advertising(Library.browser)
Library.time_match = 23
# Написать "LIVE" для парсинга лайв матчей. По умолчанию пасинг происходит по "Расписание"
Library.Select = ""
for times in range(100):
    try:
        # analysis.click_completed(Library.browser)
        if Library.Select == "LIVE":
            Func.open_tabs(Library.browser)
            Func.open_match(Func.select_match(Library.browser, times), Library.browser)
        else:
            Func.open_match(Func.select_match_schedule(Library.browser), Library.browser)
        Library.x = 0
        print("Цикл пройден!")
        time.sleep(150)
    except selenium.common.exceptions.StaleElementReferenceException:
        print("Чет ошибка..")
