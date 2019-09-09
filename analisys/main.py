from analisys import Func
from analisys import setting

url = "https://www.myscore.ru/"
setting.browser.get(url)

Func.remove_advertising(setting.browser)

Func.open_match(Func.select_match_schedule(setting.browser), setting.browser)

setting.browser.close()
print("Анализ завершен!")