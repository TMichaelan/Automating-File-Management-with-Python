from selenium import webdriver
import configparser
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
options = webdriver.ChromeOptions()

config = configparser.ConfigParser()
config.read("settings.ini")
URL = config["DEFAULT"]["URL"]
DOWNLOAD_DIR = config["DEFAULT"]["download_dir"]

prefs = {
"download.default_directory": r"{DOWNLOAD_DIR}".format(DOWNLOAD_DIR = DOWNLOAD_DIR),
"download.prompt_for_download": False,
"download.directory_upgrade": True
}

options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chrome_options=options)
driver.get(URL)
button = driver.find_element_by_class_name(u"h-sb-Ic")
driver.implicitly_wait(10)
button.click()
