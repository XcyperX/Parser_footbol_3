from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# ua = dict(DesiredCapabilities.CHROME)
# options = webdriver.ChromeOptions()
# # options.add_argument('headless')
# options.add_argument('window-size=1920x935')
# # options.add_argument("--no-startup-window")
# browser = webdriver.Chrome(chrome_options=options)
browser = webdriver.Firefox()
x = 0
country = ""
name_one_team = ""
name_two_team = ""
Select = ""
One_metod_one_team = ""
One_metod_two_team = ""
Two_metod_one_team = ""
Two_metod_two_team = ""

och_one = ""
och_two = ""
och2_one = ""
och2_two = ""

url_ifo = ""

intramural_one_team = ""
intramural_two_team = ""
time_match = 0

List_need = []
passed = []

all_data = []