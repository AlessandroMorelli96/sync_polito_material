from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import json


class DownloaderFile:
    # Variable
    user = ""
    passw = ""
    path = ""
    
    def __init__(self):
        super().__init__()

    def startDownload(self):
        with open('settings.json', 'r+') as f:
            data = json.load(f)
            self.user = "s" + data['credentials']['username'] + "@studenti.polito.it"
            self.passw = data['credentials']['password']
            self.path = data['download_folder']
        
        # WebDriver
        options = Options() 
        options.add_argument("--disable-notifications")
        options.add_experimental_option("prefs", {
                "download.default_directory": self.path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
        })
        driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
        
        self._login(driver)
    
        with open('list.json') as json_file:
            data = json.load(json_file)
            for info in data['file']:
                self._downloadData(driver, info)
            change = input("Finito il Download? [Y/n]") or "y"
            if change == "y" or change == "Y":
                for info in data['file']:
                    self._replaceFile(info)

        driver.quit()

    def _login(self, driver):
        print("Logging in...")
        driver.get('https://idp.polito.it/idp/x509mixed-login')
        driver.find_element_by_id('j_username').send_keys(self.user)
        driver.find_element_by_id('j_password').send_keys(self.passw)
        driver.find_element_by_id('usernamepassword').click()
        print("Loged")

    def _replaceFile(self, info):
        os.replace(self.path + info['name'], info['folder']+"/"+info['name'])

    def _downloadData(self, driver, info):
        url = "https://file.didattica.polito.it/download/MATDID/" + info['code'] + "?download"
        driver.get(url)
