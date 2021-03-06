from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from accessKey import User
from utils import *
import base64
import time
import re
import os


class M3U8:

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

    def getFilm(self,  url: str) -> None:
        self.root.get(url)
        self._login()

        # get name
        name = self.root.find_element_by_xpath(
            "/html/body/section[3]/div/div/div[1]/div/a/h1").text.lower()

        # go to movie page
        iframe = self.root.find_element_by_xpath(
            "/html/body/section[5]/div/div/div/div/div[1]/div[2]/iframe")
        self.root.get(iframe.get_attribute("src"))

        # go to 4k definition
        button_4k = self.root.find_element_by_xpath(
            "/html/body/div[1]/div[1]/ul/li[3]/a")
        self.root.get(button_4k.get_attribute("href"))

        # go to embed page
        embed = self.root.find_element_by_xpath("/html/body/div[2]/iframe")
        self.root.get(embed.get_attribute("src"))

        m3u8 = self._blob()
        self.root.quit()
        initializeFilm(name, m3u8)

    def getSerie(self, url: str, seasons: set, episodes: set) -> None:
        self.root.get(url)

        # get name
        name = self.root.find_element_by_xpath(
            "/html/body/div/section[1]/div/div/div[2]/div/div/div[2]/a/h1").text.lower()
        if name[-9:] == ' la serie':
            name = name[:-9]

        # go to tvShow page
        allEpisode = self.root.find_element_by_xpath(
            '/html/body/div/section[1]/div/div/div[2]/div/div/div[2]/iframe')
        episodeUrl = allEpisode.get_attribute("src")

        for season in seasons:
            if len(episodes) == 0:
                episodes = self._numEpisode(
                    '%s/?season=%d' % (episodeUrl, season))

            for episode in episodes:
                _m3u8 = self._getEpisode(episodeUrl, season, episode)
                initializeSerie(name, _m3u8, season+1, episode+1)
        self.root.quit()
        return name

    def _getEpisode(self, url: str, season: int, episode: int) -> str:
        self.root.get('%s?season=%d&episode=%d' %
                      (url, season, episode))

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
        _id = re.findall(r"https:\/\/hdmario.live\/embed\/(.*)", _url)[0]
        self.root.get("https://hdmario.live/login/%s" % _id)

        if re.match(r".*\/login\/.*", self.root.current_url) != None:
            self._login(False)

        return self._blob()

    def _numEpisode(self, seasonUrl: str) -> set:
        self.root.get(seasonUrl)
        _all = self.root.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/ul')
        lenght = len(_all.find_elements_by_tag_name('li'))
        return set([i for i in range(lenght)])

    def _login(self, film) -> None:
        email = self.root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[1]/input" if film else
            "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div[1]/input")
        email.send_keys(User.email())

        pas = self.root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[2]/input" if film else "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div[2]/input")
        pas.send_keys(User.password())

        butt = self.root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[3]/button" if film else
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
