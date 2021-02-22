from utils import initialize
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import time
import re
import os


class M3U8:

    def get(self, url):
        self.path = os.getcwd()

        self.setProp()

        self.root.get(url)

        self.login()

        name=self.root.find_element_by_xpath("/html/body/section[3]/div/div/div[1]/div/a/h1").text.lower()

        id = re.findall(
            'https://hdpass.click/movie/(.*)\?noads=1', self.root.page_source)[0]
        self.root.get(
            "https://hdpass.click/movie/%s?resolution=2&noads=1" % id)

        id_4k = re.findall(
            'https://hdmario.live/embed/(.*)\?&amp;noads=1', self.root.page_source)[0]
        self.root.get("https://hdmario.live/embed/%s?&noads=1" % id_4k)

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

                    with open("%s\\%s.m3u8" % (self.path, blob), 'r') as m3u8_url:
                        for line in m3u8_url.readlines():
                            m3u8 = re.findall("^(blob.*)\n", line)
                            if len(m3u8) != 0:
                                m3u8 = m3u8[0]
                                break
                    self.root.get(m3u8)
                    os.remove("%s\\%s.m3u8" % (self.path, blob))
                    time.sleep(0.5)
                    initialize(name,m3u8.split('/')[-1])
                    return name

    def login(self):
        email = self.root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[1]/input")
        email.send_keys("ggcarlo632@gmail.com")

        pas = self.root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[2]/input")
        pas.send_keys("sonoi00")

        butt = self.root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[3]/button")
        butt.submit()

    def setProp(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"browser": "ALL"}

        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': self.path}
        options.add_experimental_option('prefs', prefs)

        self.root = webdriver.Chrome(
            executable_path="%s\\chromedriver_win32\\chromedriver.exe" % self.path, desired_capabilities=capabilities, options=options)
