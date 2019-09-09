import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import Library
import time
import Bot_telegram
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

def open_tabs(browser):
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

    if Library.Select == "LIVE":
        browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/ul/li[2]/a/div').click()
        browser.find_element_by_xpath('//*[@id="sound-switch"]').click()
    else:
        browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/ul/li[6]/a/div').click()

    List_scroll = browser.find_elements_by_css_selector(".event__expander.icon--expander.expand")
    # Удаляем рекламу, чтоб она не мешала открывать вкладки
    for x in List_scroll:
        List_scroll[z].click()
        z -= 1
    List_scroll.clear()
    browser.execute_script("window.scrollTo(0, 0)")

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
    # Удаляем рекламу, чтоб она не мешала открывать вкладки
    for x in List_scroll:
        List_scroll[z].click()
        z -= 1
    List_scroll.clear()
    browser.execute_script("window.scrollTo(0, 0)")

# Сбор необходимых матчей
def select_match(browser):
    List_match = browser.find_elements_by_class_name("event__match")
    List_need_match = []
    for x in List_match:
        try:
            # Выбор матчей со временем игры меньше 15 минут
            if int(str(x.text).strip().split("\n")[0]) < Library.time_match and \
               int(str(x.text).strip().split("\n")[2]) == 0 and \
               int(str(x.text).strip().split("\n")[4]) == 0:
                List_need_match.append(str(x.text).strip().split("\n")[1])
        except ValueError:
            pass
    text = Sql_sand.scan_name()
    for x in text:
        if str(x).strip('(),').strip(chr(39)) in List_need_match:
            print(str(x) + " НАШЕЛ!!!")
            List_need_match.remove(str(x).strip('(),').strip(chr(39)))
    return List_need_match

def select_match_schedule(browser):
    # time.sleep(4)
    try:
        WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/'
                                                                               'div/div[3]/div')))
        browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/div/div[3]/div').click()
    except selenium.common.exceptions.TimeoutException:
        browser.refresh()
        WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/'
                                                                               'div/div[3]/div')))
    time.sleep(3)
    try:
        WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/'
                                                                               'ul/li[6]/a/div')))
        browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/ul/li[6]/a/div').click()
    except selenium.common.exceptions.TimeoutException:
        browser.refresh()
        WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/div[1]/'
                                                                               'ul/li[6]/a/div')))


    open_tabs_raspis(browser)
    List_need = []
    List_match = browser.find_elements_by_class_name('event__match')

    for x in List_match:
        if str(x.text).strip().split("\n")[0] == "Будет":
            pass
        elif str(x.text).strip().split("\n")[1] != "TKP":
            List_need.append(str(x.text).strip().split("\n")[1])
        else:
            List_need.append(str(x.text).strip().split("\n")[2])

    # Отправляем sql запрос на получение списка команд
    text = Sql_sand.scan_name()
    for x in text:
        if str(x).strip('(),').strip(chr(39)) in List_need:
            print(str(x) + " НАШЕЛ!!!")
            List_need.remove(str(x).strip('(),').strip(chr(39)))
    return List_need

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
                            number_of_matches(browser)
                        except selenium.common.exceptions.ElementClickInterceptedException:
                            browser.execute_script("window.scrollTo(0," + str(int(x.location.get("y")) + 100) + ")")
                        else:
                            break
                else:
                    pass
    except IndexError:
        pass


def number_of_matches(browser):
    browser.switch_to.window(browser.window_handles[-1])
    number_match_one = 0
    number_match_two = 0
    while True:
        try:
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="li-match-head-2-head"]')))
            browser.find_element_by_class_name("li2").click()
            # Проверка загрузки последних матчей
            WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                             'table/thead/tr/td')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
        else:
            break
    # Узнаем url страницы
    Library.url_ifo = browser.current_url
    # print(browser.current_url)

    # Находим количество матчей у первой команды
    max_match_one = browser.find_elements_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr').__len__()
    # Находим количество матчей у второй команды
    max_match_two = browser.find_elements_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr').__len__()
    # Находим название первой команды
    # all_data[0]
    try:
        Library.all_data.append(browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[1]/'
                                                              'td[@class="name highTeam"]').text)
    except selenium.common.exceptions.NoSuchElementException:
        Library.all_data.append(browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr/'
                                                              'td[@class="name highTeam lastR"]').text)

    # Находим название второй команды
    # all_data[1]
    try:
        Library.all_data.append(browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr[1]/'
                                                              'td[@class="name highTeam"]').text)
    except selenium.common.exceptions.NoSuchElementException:
        Library.all_data.append(browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr/'
                                                              'td[@class="name highTeam lastR"]').text)

    # Чекаем страну
    # all_data[2]
    Library.all_data.append(browser.find_element_by_xpath('//*[@id="detcon"]/div[2]/div[1]/span[2]').text)
    if browser.find_element_by_xpath('//*[@id="detcon"]/div[2]/div[1]/span[2]').text == Library.all_data[2]:
        Library.all_data[2] = browser.find_element_by_xpath('//*[@id="detcon"]/div[2]/div[1]/span[2]').text
    # all_data[3]
    Library.all_data.append(str(browser.find_element_by_xpath('//*[@id="utime"]').text).split(" ")[1])

    if max_match_one < 5:
        number_match_one = max_match_one
    else:
        number_match_one = 5

    if max_match_two < 5:
        number_match_two = max_match_two
    else:
        number_match_two = 5

    print(Library.all_data[0] + " | " + Library.all_data[1])
    analysis_one_team(browser, number_match_one)
    analysis_two_team(browser, number_match_two)

def analysis_one_team(browser, number_match):
    team_one_goal = 0
    team_one_missing = 0
    team_one_goal_home = 0
    team_one_goal_away = 0
    for y in range(1, number_match + 1):
        while True:
            try:
                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="tab-h2h-overall"]/'
                                                                                       'div[1]/table/tbody/tr[' + str(y)
                                                                                        + ']/td[2]')))
            except selenium.common.exceptions.TimeoutException:
                browser.refresh()
            else:
                break
        browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
        browser.switch_to.window(browser.window_handles[-1])
        try:
            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.CLASS_NAME, "detailMS")))
            if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a') \
                    .text.find(Library.all_data[0]) == -1:
                while True:
                    try:
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="li-match-summary"]')))
                    except selenium.common.exceptions.TimeoutException:
                        browser.refresh()
                    else:
                        break
                team_one_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                team_one_goal_away += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                        'div[1]/div[1]/div[2]/span[2]').text)
                team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[1]').text)
            else:
                try:
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-head-2-head"]')))
                except selenium.common.exceptions.TimeoutException:
                    browser.refresh()
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-summary"]')))
                team_one_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                team_one_goal_home += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                        'div[1]/div[1]/div[2]/span[1]').text)
                team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[2]').text)
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
        except selenium.common.exceptions.NoSuchElementException:
            print("Чет не получилось )")
        except ImportError:
            print("Не нашел счет, ля!")
        except selenium.common.exceptions.TimeoutException:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            Library.One_metod_one_team = Library.all_data[0] + " - " + "0%" + " | "
            Library.Two_metod_one_team = Library.all_data[0] + " - " + "0 | "
            Library.all_data.append("0%")
            Library.all_data.append("0")

    if Library.all_data.__len__() < 5:
        try:
            one = team_one_goal / team_one_missing
        except ZeroDivisionError:
            one = 0
        Library.One_metod_one_team = Library.all_data[0] + " - " + str((team_one_goal / 5) * 100) + "%" + " | "
        Library.Two_metod_one_team = Library.all_data[0] + " - " + str(round(one, 2)) + " | "
        # all_data[4-5]
        Library.all_data.append(str((team_one_goal / 5) * 100) + "%")
        Library.all_data.append(str(round(one, 2)))

def analysis_two_team(browser, number_match):
    team_two_goal = 0
    team_two_missing = 0
    team_two_goal_home = 0
    team_two_goal_away = 0
    for y in range(1, number_match + 1):
        while True:
            try:
                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                             '//*[@id="tab-h2h-overall"]/div[2]/'
                                                                             'table/tbody/tr[' + str(y) + ']/td[2]')))
            except selenium.common.exceptions.TimeoutException:
                browser.refresh()
            else:
                break
        browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr[' + str(y) + ']/td[2]').click()
        browser.switch_to.window(browser.window_handles[-1])
        try:
            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.CLASS_NAME, "detailMS")))
            if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a') \
                    .text.find(Library.all_data[1]) == -1:
                while True:
                    try:
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="li-match-summary"]')))
                    except selenium.common.exceptions.TimeoutException:
                        browser.refresh()
                    else:
                        break
                team_two_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                 '//*[@id="summary-content"]/'
                                                                                 'div[1]/div[1]/div[2]/span[2]')))
                team_two_goal_away += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                        'div[1]/div[1]/div[2]/span[2]').text)
                team_two_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[1]').text)
            else:
                try:
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-head-2-head"]')))
                except selenium.common.exceptions.TimeoutException:
                    browser.refresh()
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-summary"]')))
                team_two_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                team_two_goal_home += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                        'div[1]/div[1]/div[2]/span[1]').text)
                team_two_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[2]').text)
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
        except selenium.common.exceptions.NoSuchElementException:
            print("Чет не получилось )")
        except ImportError:
            print("Не нашел гол, ля!")
        except selenium.common.exceptions.StaleElementReferenceException:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
        except selenium.common.exceptions.TimeoutException:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            Library.One_metod_two_team = "0%" + " - " + Library.all_data[1]
            Library.Two_metod_two_team = "0" + " - " + Library.all_data[1] + "\n"
            Library.all_data.append("0%")
            Library.all_data.append("0")
    if Library.all_data.__len__() < 8:
        try:
            three = team_two_goal / team_two_missing
        except ZeroDivisionError:
            three = 0
        Library.One_metod_two_team = str((team_two_goal / 5) * 100) + "%" + " - " + Library.all_data[1]
        Library.Two_metod_two_team = str(round(three, 2)) + " - " + Library.all_data[1] + "\n"
        # all_data[6-7]
        Library.all_data.append(str((team_two_goal / 5) * 100) + "%")
        Library.all_data.append(str(round(three, 2)))
    if browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[3]/table/tbody/tr[1]').text != "Нет матчей.":
        analysis_intramural_match(browser)
    else:
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        write_to_file(Library.One_metod_one_team, Library.One_metod_two_team,
                      Library.Two_metod_one_team, Library.Two_metod_two_team,
                      Library.och_one, Library.och2_one, Library.och_two, Library.och2_two)

def analysis_intramural_match(browser):
    team_one_goal = 0
    team_one_missing = 0
    team_two_goal = 0
    team_two_missing = 0
    max_match = browser.find_elements_by_xpath('//*[@id="tab-h2h-overall"]/div[3]/table/tbody/tr').__len__()
    if max_match < 5:
        number_match = max_match
    else:
        number_match = 5
    for y in range(1, number_match + 1):
        while True:
            try:
                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="tab-h2h-overall"]/'
                                                                                       'div[3]/table/tbody/tr[' + str(y)
                                                                             + ']/td[2]')))
            except selenium.common.exceptions.TimeoutException:
                browser.refresh()
            else:
                break
        browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[3]/table/tbody/tr[' + str(y) + ']/td[2]').click()
        browser.switch_to.window(browser.window_handles[-1])
        try:
            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.CLASS_NAME, "detailMS")))
            if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a') \
                    .text.find(Library.all_data[0]) == -1:
                while True:
                    try:
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="li-match-summary"]')))
                    except selenium.common.exceptions.TimeoutException:
                        browser.refresh()
                    else:
                        break
                team_one_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[1]').text)
                team_two_goal += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[1]').text)
                team_two_missing += int(browser.find_elements_by_class_name("p1_away")[0].text)
            else:
                try:
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-head-2-head"]')))
                except selenium.common.exceptions.TimeoutException:
                    browser.refresh()
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-summary"]')))
                team_one_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[2]').text)
                team_two_goal += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[2]').text)
                team_two_missing += int(browser.find_elements_by_class_name("p1_home")[0].text)
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])

        except selenium.common.exceptions.NoSuchElementException:
            print("Чет не получилось )")
        except ImportError:
            print("Не нашел счет, ля!")
        except selenium.common.exceptions.TimeoutException:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            Library.och_one = Library.all_data[0] + " - " + str(0) + "%" + " | "
            Library.och2_one = Library.all_data[0] + " - " + str(0) + " | "
            Library.och_two = str(0) + "%" + " - " + Library.all_data[1]
            Library.och2_two = str(0) + " - " + Library.all_data[1] + "\n"
            Library.all_data.append("0%")
            Library.all_data.append("0")
            Library.all_data.append("0%")
            Library.all_data.append("0")

    if Library.all_data.__len__() > 11:
        pass
    else:
        try:
            one = team_one_goal / team_one_missing
        except ZeroDivisionError:
            one = 0
        Library.och_one = Library.all_data[0] + " - " + str((team_one_goal / 5) * 100) + "%" + " | "
        Library.och2_one = Library.all_data[0] + " - " + str(round(one, 2)) + " | "

        Library.all_data.append(str((team_one_goal / 5) * 100) + "%")
        Library.all_data.append(str(round(one, 2)))
        try:
            three = team_two_goal / team_two_missing
        except ZeroDivisionError:
            three = 0
        Library.och_two = str((team_two_goal / 5) * 100) + "%" + " - " + Library.all_data[1]
        Library.och2_two = str(round(three, 2)) + " - " + Library.all_data[1] + "\n"
        # all_data[8-11]
        Library.all_data.append(str((team_two_goal / 5) * 100) + "%")
        Library.all_data.append(str(round(three, 2)))
    browser.close()
    browser.switch_to.window(browser.window_handles[-1])
    write_to_file(Library.One_metod_one_team, Library.One_metod_two_team,
                  Library.Two_metod_one_team, Library.Two_metod_two_team,
                  Library.och_one, Library.och2_one, Library.och_two, Library.och2_two)


def write_to_file(One_metod_one_team, One_metod_two_team, Two_metod_one_team, Two_metod_two_team,
                  och_one, och2_one, och_two, och2_two):
    print(Library.all_data)
    Sql_sand.isert_one_team(Library.all_data[3], Library.all_data[2], Library.all_data[0],
                            Library.all_data[4], Library.all_data[5])
    Sql_sand.isert_two_team(Library.all_data[3], Library.all_data[2], Library.all_data[1],
                            Library.all_data[6], Library.all_data[7])
    if Library.all_data.__len__() > 10:
        Sql_sand.isert_intramural_one_team(Library.all_data[2], Library.all_data[0],
                                           Library.all_data[8], Library.all_data[9])
        Sql_sand.isert_intramural_two_team(Library.all_data[2], Library.all_data[1],
                                           Library.all_data[10], Library.all_data[11])

    if och_one == "":
        Bot_telegram.send_match(Library.all_data[2] + "\n" + Library.all_data[3] + "\n" + One_metod_one_team + One_metod_two_team + "\n" +
                                Two_metod_one_team + Two_metod_two_team, Library.url_ifo)
    else:
        Bot_telegram.send_match(Library.all_data[2] + "\n" + Library.all_data[3] + "\n" + One_metod_one_team + One_metod_two_team + "\n" +
                                Two_metod_one_team + Two_metod_two_team + "Очные встречи:" + "\n" + och_one + och_two +
                                "\n" + och2_one + och2_two, Library.url_ifo)
    Library.och_one = ""
    Library.och2_one = ""
    Library.och_two = ""
    Library.och2_two = ""
    Library.all_data.clear()
