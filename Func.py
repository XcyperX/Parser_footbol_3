import selenium
import pickle
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import Library
import time
import Bot_telegram
from collections import OrderedDict

def remove_advertising(browser):
    try:
        # time.sleep(3)
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
def select_match(browser, times):
    List_match = browser.find_elements_by_class_name("event__match")
    List_match_edit = []
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
    # Убираем из списка метчи найденные в первом прогоне
    if times >= 2:
        List_need_match = list(set(List_need_match) - set(List_match_edit))
    else:
        List_match_edit = List_need_match
    # Убираем из списка матчи которые уже есть в результатах
    with open('List_chapter.txt', 'r', encoding='utf-8') as file1:
        text = ' '.join(file1.read().split())
        file1.close()
    for x in List_need_match:
        if x in text:
            List_need_match.remove(x)
    return List_need_match

def select_match_schedule(browser):
    # time.sleep(4)
    browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/div/div[3]/div').click()
    time.sleep(2)
    open_tabs_raspis(browser)
    List_need = {}
    List_match = browser.find_elements_by_class_name("event__match")
    for x in List_match:
        if str(x.text).strip().split("\n")[0] == "Будет":
            pass
        elif str(x.text).strip().split("\n")[1] != "TKP":
            List_need[str(x.text).strip().split("\n")[1]] = str(x.text).strip().split("\n")[0]
        else:
            List_need[str(x.text).strip().split("\n")[2]] = str(x.text).strip().split("\n")[0]

    List_need = OrderedDict(sorted(List_need.items(), key=lambda t: t[1]))
    Library.List_need = list(List_need.values())
    # Время и название первой команды
    # with open('data_one.txt', 'wb') as file11:
    #     pickle.dump(List_need, file11)
    return List_need.keys()

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
    try:
        Library.name_one_team = browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[1]/'
                                                      'td[@class="name highTeam"]').text
    except selenium.common.exceptions.NoSuchElementException:
        Library.name_one_team = browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr/'
                                                              'td[@class="name highTeam lastR"]').text

    # Находим название второй команды
    try:
        Library.name_two_team = browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr[1]/'
                                                      'td[@class="name highTeam"]').text
    except selenium.common.exceptions.NoSuchElementException:
        Library.name_one_team = browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr/'
                                                              'td[@class="name highTeam lastR"]').text

    # Чекаем страну
    Library.country = browser.find_element_by_xpath('//*[@id="detcon"]/div[2]/div[1]/span[2]').text
    if browser.find_element_by_xpath('//*[@id="detcon"]/div[2]/div[1]/span[2]').text == Library.country:
        Library.country = browser.find_element_by_xpath('//*[@id="detcon"]/div[2]/div[1]/span[2]').text

    if max_match_one < 5:
        number_match_one = max_match_one
    else:
        number_match_one = 5

    if max_match_two < 5:
        number_match_two = max_match_two
    else:
        number_match_two = 5

    Library.all_data.append(Library.List_need[Library.x])
    Library.all_data.append(Library.country)
    Library.x += 1
    print(Library.name_one_team + " | " + Library.name_two_team)
    analysis_one_team(browser, number_match_one, Library.name_one_team)
    analysis_two_team(browser, number_match_two, Library.name_two_team)

def analysis_one_team(browser, number_match, name_one_team):
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
                    .text.find(name_one_team) == -1:
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
            try:
                one = team_one_goal / team_one_missing
            except ZeroDivisionError:
                one = 0
            Library.One_metod_one_team = name_one_team + " - " + str((team_one_goal / 5) * 100) + "%" + " | "
            Library.Two_metod_one_team = name_one_team + " - " + str(round(one, 2)) + " | "

        except selenium.common.exceptions.NoSuchElementException:
            print("Чет не получилось )")
        except ImportError:
            print("Не нашел счет, ля!")
        except selenium.common.exceptions.TimeoutException:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            Library.One_metod_one_team = name_one_team + " - " + str(0) + "%" + " | "
            Library.Two_metod_one_team = name_one_team + " - " + str(0) + " | "
            Library.all_data.append(name_one_team)
            Library.all_data.append("0%")
            
    Library.all_data.append(name_one_team)
    Library.all_data.append(str((team_one_goal / 5) * 100) + "%")

def analysis_two_team(browser, number_match, name_two_team):
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
                    .text.find(name_two_team) == -1:
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
            try:
                three = team_two_goal / team_two_missing
            except ZeroDivisionError:
                three = 0
            Library.One_metod_two_team = str((team_two_goal / 5) * 100) + "%" + " - " + name_two_team
            Library.Two_metod_two_team = str(round(three, 2)) + " - " + name_two_team + "\n"
            Library.all_data.append(str((team_two_goal / 5) * 100) + "%")
            Library.all_data.append(name_two_team)
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
            Library.One_metod_two_team = str(0) + "%" + " - " + name_two_team
            Library.Two_metod_two_team = str(0) + " - " + name_two_team + "\n"
            Library.all_data.append("0%")
            Library.all_data.append(name_two_team)
    if browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[3]/table/tbody/tr[1]').text != "Нет матчей.":
        analysis_intramural_match(browser, Library.name_one_team, Library.name_two_team)
    else:
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        write_to_file(Library.One_metod_one_team, Library.One_metod_two_team,
                      Library.Two_metod_one_team, Library.Two_metod_two_team,
                      Library.och_one, Library.och2_one, Library.och_two, Library.och2_two)

def analysis_intramural_match(browser, name_one_team, name_two_team):
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
                    .text.find(name_one_team) == -1:
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

            try:
                one = team_one_goal / team_one_missing
            except ZeroDivisionError:
                one = 0
            Library.och_one = name_one_team + " - " + str((team_one_goal / 5) * 100) + "%" + " | "
            Library.och2_one = name_one_team + " - " + str(round(one, 2)) + " | "
            try:
                three = team_two_goal / team_two_missing
            except ZeroDivisionError:
                three = 0
            Library.och_two = str((team_two_goal / 5) * 100) + "%" + " - " + name_two_team
            Library.och2_two = str(round(three, 2)) + " - " + name_two_team + "\n"


        except selenium.common.exceptions.NoSuchElementException:
            print("Чет не получилось )")
        except ImportError:
            print("Не нашел счет, ля!")
        except selenium.common.exceptions.TimeoutException:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            Library.och_one = name_one_team + " - " + str(0) + "%" + " | "
            Library.och2_one = name_one_team + " - " + str(0) + " | "
            Library.och_two = str(0) + "%" + " - " + name_two_team
            Library.och2_two = str(0) + " - " + name_two_team + "\n"
    browser.close()
    browser.switch_to.window(browser.window_handles[-1])
    write_to_file(Library.One_metod_one_team, Library.One_metod_two_team,
                  Library.Two_metod_one_team, Library.Two_metod_two_team,
                  Library.och_one, Library.och2_one, Library.och_two, Library.och2_two)


def write_to_file(One_metod_one_team, One_metod_two_team, Two_metod_one_team, Two_metod_two_team,
                  och_one, och2_one, och_two, och2_two):
    print(Library.all_data)

    if och_one == "":
        The_end = []
        The_end.append(Library.country + "\n" + One_metod_one_team + One_metod_two_team)
        The_end.append(Two_metod_one_team + Two_metod_two_team)
        Bot_telegram.send_match(Library.country + "\n" + One_metod_one_team + One_metod_two_team + "\n" +
                                Two_metod_one_team + Two_metod_two_team, Library.url_ifo)
        with open('List_chapter.txt', 'a', encoding='utf-8') as file11:
            file11.writelines("%s\n" % place for place in The_end)
        The_end.clear()
    else:
        The_end = []
        The_end.append(Library.country + "\n" + One_metod_one_team + One_metod_two_team + "\n" +
                       Two_metod_one_team + Two_metod_two_team + "Очные встречи:" + "\n" + och_one +
                       och_two + "\n" + och2_one + och2_two)
        Bot_telegram.send_match(Library.country + "\n" + One_metod_one_team + One_metod_two_team + "\n" +
                                Two_metod_one_team + Two_metod_two_team + "Очные встречи:" + "\n" + och_one + och_two +
                                "\n" + och2_one + och2_two, Library.url_ifo)
        with open('List_chapter.txt', 'a', encoding='utf-8') as file11:
            file11.writelines("%s\n" % place for place in The_end)
        The_end.clear()
        Library.och_one = ""
        Library.och2_one = ""
        Library.och_two = ""
        Library.och2_two = ""
