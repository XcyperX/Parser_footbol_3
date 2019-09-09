from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# ua = dict(DesiredCapabilities.CHROME)
# options = webdriver.ChromeOptions()
# # options.add_argument('headless')
# options.add_argument('window-size=1920x935')
# # options.add_argument("--no-startup-window")
# browser = webdriver.Chrome(chrome_options=options)
browser = webdriver.Firefox()