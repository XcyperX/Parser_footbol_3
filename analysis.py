import selenium
import pickle
import time
import Library
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

def click_completed(browser):
    open_tabs(browser)
    List_need = {}
    with open('data_one.txt', 'rb') as inp:
        List_need = pickle.load(inp)
    print(List_need.keys())
    open_match(List_need.keys(), browser)

def open_tabs(browser):
    z = -1
    while True:
        try:
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/'
                                                                                   'ul/li[5]/a/div')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/'
                                                                                   'ul/li[5]/a/div')))
        else:
            break
    browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/ul/li[5]/a/div').click()

    List_scroll = browser.find_elements_by_css_selector(".event__expander.icon--expander.expand")

    for x in List_scroll:
        List_scroll[z].click()
        z -= 1
    List_scroll.clear()
    browser.execute_script("window.scrollTo(0, 0)")

def open_match(List_need_match, browser):
    z=0
    # Получаем список всех матчей
    print("Дошли до открытия")
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
    print(Library.passed)
    print("Закончили!!")
    write_data_analysis(Library.passed)

def analysis(browser, name_one_team):
    browser.switch_to.window(browser.window_handles[-1])

    print("Чекаем матчи")
    try:
        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="summary-content"]/'
                                                                                   'div[1]/div[1]/div[2]')))
        time.sleep(1)
        result = browser.find_element_by_xpath('//*[@id="summary-content"]/div[1]/div[1]/div[2]').text
        result = str(result).replace(" ", "").split('-')
        print(result)
        if int(result[0]) == 0 and int(result[1]) == 0:
            print("По нулям")
            pass
        else:
            Library.passed.append(name_one_team)
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
    except selenium.common.exceptions.NoSuchElementException:
        print("Чет не получилось )")

def write_data_analysis(name):

    with open('List_chapter2.txt', 'r', encoding='utf-8') as out:
        data = out.read()
    data = data.split('#')
    for x in data:
        for y in name:
            # print(x.replace("\n", " ").strip().split(" "))
            if str(y).split(" ")[0] in x.replace("\n", " ").strip().split(" "):
                print("Нашел")
                with open('data_analysis.txt', 'a', encoding='utf-8') as file11:
                    file11.write(x)
            else:
                # print("Не нашел")
                pass