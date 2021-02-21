from selenium.webdriver import Chrome, Edge
import re
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class M3U8:
    def __init__(self, url):
        self.url = url

    def get(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"browser": "ALL"}
        root = Chrome(
            executable_path="C:\\Users\\marti\\Downloads\\chromedriver_win32\\chromedriver.exe", desired_capabilities=capabilities)
        root.get(self.url)

        email = root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[1]/input")
        email.send_keys("ggcarlo632@gmail.com")

        pas = root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[2]/input")
        pas.send_keys("sonoi00")

        butt = root.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div[2]/form/div[3]/button")
        butt.submit()

        id = re.findall(
            'https://hdpass.click/movie/(.*)\?noads=1', root.page_source)[0]
        root.get("https://hdpass.click/movie/%s?resolution=2&noads=1" % id)

        id_4k = re.findall(
            'https://hdmario.live/embed/(.*)\?&amp;noads=1', root.page_source)[0]
        root.get("https://hdmario.live/embed/%s?&noads=1" % id_4k)

        time.sleep(1)

        while True:
            for log in root.get_log("browser"):
                blob = re.findall(
                    '.*"converted url" "(.*)"', log["message"])

                if len(blob) !=0:
                    print(blob[0])
                    root.get(blob[0])
                    blob_name=blob[0].split('/')[-1]
                    time.sleep(1)
                    with open("C:\\Users\\marti\\Downloads\\%s.m3u8" %blob_name,'r') as m3u8_url: 
                        for line in m3u8_url.readlines():
                            m3u8=re.findall("^(blob.*)\n",line)
                            if len(m3u8)!=0:
                                m3u8=m3u8[0]
                                break
                        root.get(m3u8)
                        time.sleep(1)
                        return "C:\\Users\\marti\\Downloads\\%s.m3u8"%m3u8.split('/')[-1]


print(M3U8("https://altadefinizionecommunity.net/flora-ulisse-streaming/?loggedin=eyJlIjoiZ2djYXJsbzYzMkBnbWFpbC5jb20iLCJwIjoic29ub2RpMDAifQ==").get())
