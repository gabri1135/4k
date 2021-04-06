from serie import Serie
from path import PathModel
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from accessKey import User
import base64
import time
import re
import os


class DownloadM3U8:
    def __init__(self) -> None:
        self._setProp()

    def _blob(self) -> str:
        time.sleep(0.5)

        while True:
            for log in self.root.get_log("browser"):
                blob = re.findall(
                    '.*"converted url" "(.*)"', log["message"])

                if len(blob) != 0:
                    blob = blob[0]
                    print(blob)
                    self.root.get(blob)
                    time.sleep(1)

                    blob = blob.split('/')[-1]

                    with open("%s.m3u8" % blob, 'r') as m3u8_url:
                        for line in m3u8_url.readlines():
                            m3u8 = re.findall("^(blob.*)\n", line)
                            if len(m3u8) != 0:
                                m3u8 = m3u8[0]
                                break
                    self.root.get(m3u8)
                    os.remove("%s.m3u8" % blob)
                    time.sleep(0.5)
                    return m3u8.split('/')[-1]+'.m3u8'

    def getFilm(self,  url: str) -> PathModel:
        self.root.get(url)

        # go to 4k definition
        button4k = self.root.find_element_by_xpath(
            "/html/body/div[1]/div[1]/ul/li[3]/a")
        self.root.get(button4k.get_attribute("href"))

        embed = self.root.find_element_by_xpath(
            '/html/body/div[2]/iframe')
        embedUrl = str(embed.get_attribute("src"))

        self.root.get(embedUrl.replace("embed", "login"))
        if re.match(r".*\/login\/.*", self.root.current_url) != None:
            self._login()

        m3u8 = self._blob()
        self.root.quit()
        return PathModel(os.getcwd()).add(m3u8)

    def getSerie(self, outputFolder: PathModel, url: str, all: list[tuple]) -> None:
        for x in all:
            _m3u8 = self._getEpisode(url, x)
            Serie.initialize(x, outputFolder,  PathModel(os.getcwd()).add(_m3u8))
        self.root.quit()

    def _getEpisode(self, url: str, detail: tuple) -> str:
        self.root.get('{}?season=%d&episode=%d'.format(url) % detail)

        # go to 4k definition
        button_4k = self.root.find_element_by_xpath(
            "/html/body/div[4]/div[1]/ul/li[3]/a")
        self.root.get(button_4k.get_attribute("href"))

        # got encoded url embed page
        embed = self.root.find_element_by_xpath(
            '/html/body/div[6]/iframe')
        encodedUrl = embed.get_attribute("custom-src")

        # go to login page
        _url = base64.b64decode(encodedUrl).decode()
        self.root.get(_url.replace("embed", "login"))

        if re.match(r".*\/login\/.*", self.root.current_url) != None:
            self._login()

        return self._blob()

    def _numEpisode(self, seasonUrl: str) -> set:
        self.root.get(seasonUrl)
        _all = self.root.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/ul')
        lenght = len(_all.find_elements_by_tag_name('li'))
        return set([i for i in range(lenght)])

    def _login(self) -> None:
        email = self.root.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div[1]/input")
        email.send_keys(User.email())

        pas = self.root.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div[2]/input")
        pas.send_keys(User.password())

        butt = self.root.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div[3]/button")
        butt.submit()

    def _setProp(self) -> None:
        path = os.getcwd()

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"browser": "ALL"}

        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': path}
        options.add_experimental_option('prefs', prefs)

        self.root = webdriver.Chrome(
            executable_path="%s\\chromedriver_win32\\chromedriver.exe" % path, desired_capabilities=capabilities, options=options)

        #button_4k = self.root.find_elements_by_name('2K')
        # if len(button_4k) == 0:
        #button_4k = self.root.find_elements_by_name('4K')
