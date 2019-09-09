import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import Library
import time
from sql import Sql_sand

def remove_advertising(browser):
    try:
        WebDriverWait(browser, 5).until(ec.element_to_be_clickable((By.CLASS_NAME, "box_over_content")))
        browser.execute_script('''var app = document.querySelector(".sticky-wrapper");
                                  app.removeChild(app.firstChild)''')
    except selenium.common.exceptions.JavascriptException:
        pass
    except selenium.common.exceptions.TimeoutException:
        pass

def open_tabs_raspis(browser):
    z = -1
    while True:
        try:
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/'
                                                                                   'div[1]/ul/li[2]/a/div')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/'
                                                                                   'div[1]/ul/li[2]/a/div')))
        else:
            break

    List_scroll = browser.find_elements_by_css_selector(".event__expander.icon--expander.expand")
    for x in List_scroll:
        List_scroll[z].click()
        z -= 1
    List_scroll.clear()
    browser.execute_script("window.scrollTo(0, 0)")

def select_match_schedule(browser):
    while True:
        try:
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/'
                                                                                   'ul/li[5]/a/div')))
            browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/ul/li[5]/a/div').click()
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
        else:
            break

    open_tabs_raspis(browser)
    List_need = []
    List_need_two = []
    List_match = browser.find_elements_by_class_name('event__match')

    for x in List_match:
        if str(x.text).strip().split("\n")[1] == "с.п.":
            List_need.append(str(x.text).strip().split("\n")[2])
        else:
            List_need.append(str(x.text).strip().split("\n")[1])

    print(List_need)

    # Отправляем sql запрос на получение списка команд
    text = Sql_sand.scan_name()
    for x in text:
        if str(x).strip('(),').strip(chr(39)) in List_need:
            print(str(x) + " НАШЕЛ!!!")
            List_need_two.append(str(x).strip('(),').strip(chr(39)))

    return List_need_two

def open_match(List_need_match, browser):
    # Получаем список всех матчей
    List_match_online = browser.find_elements_by_class_name('event__participant--home')
    # Ищем нужный нам матч и открываем его
    try:
        for x in List_need_match:
            for y in List_match_online:
                if x == y.text:
                    while True:
                        try:
                            y.click()
                            analysis(browser, x)
                        except selenium.common.exceptions.ElementClickInterceptedException:
                            browser.execute_script("window.scrollTo(0," + str(int(x.location.get("y")) + 100) + ")")
                        else:
                            break
                else:
                    pass
    except IndexError:
        pass

def analysis(browser, name):
    browser.switch_to.window(browser.window_handles[-1])
    while True:
        try:
            WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="summary-content"]')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
        else:
            break

    if browser.find_element_by_xpath('//*[@id="summary-content"]/div[1]').text == "Информация появится позже.":
        pass
    elif (int(browser.find_element_by_xpath('//*[@id="summary-content"]/div[1]/div[1]/div[2]/span[1]').text) > 0 or
          int(browser.find_element_by_xpath('//*[@id="summary-content"]/div[1]/div[1]/div[2]/span[2]').text) > 0):
        print(str(browser.find_element_by_xpath('//*[@id="summary-content"]/div[1]/div[1]/div[2]/span[1]').text) + " | " +
              str(browser.find_element_by_xpath('//*[@id="summary-content"]/div[1]/div[1]/div[2]/span[2]').text))
        Sql_sand.analysis(name)

    browser.close()
    browser.switch_to.window(browser.window_handles[-1])