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

        iframe=self.root.find_element_by_xpath("/html/body/section[5]/div/div/div/div/div[1]/div[2]/iframe")
        self.root.get(iframe.get_attribute("src"))
        
        button_4k=self.root.find_element_by_xpath("/html/body/div[1]/div[1]/ul/li[3]/a")
        
        self.root.get(button_4k.get_attribute("href"))
        
        iframe_4k = self.root.find_element_by_xpath("/html/body/div[2]/iframe")
        self.root.get(iframe_4k.get_attribute("src"))

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

                    with open("%s.m3u8" %blob, 'r') as m3u8_url:
                        for line in m3u8_url.readlines():
                            m3u8 = re.findall("^(blob.*)\n", line)
                            if len(m3u8) != 0:
                                m3u8 = m3u8[0]
                                break
                    self.root.get(m3u8)
                    os.remove("%s.m3u8" %blob)
                    time.sleep(0.5)
                    self.root.quit()
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
