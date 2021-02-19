from selenium.webdriver import Chrome, Edge
import re
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class M3U8:
    def __init__(self, url):
        self.url = url

    def get(self):
        capabilities = DesiredCapabilities.CHROME
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
        capabilities["goog:loggingPrefs"] = {
            "browser": "ALL"}  # chromedriver 75+
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
        page = re.findall(
            'https://hdpass.click/movie/(.*)\?noads=1', root.page_source)[0]
        root.get("https://hdpass.click/movie/%s?resolution=2&noads=1" % page)
        url4K = re.findall(
            'https://hdmario.live/embed/(.*)\?&amp;noads=1', root.page_source)[0]
        root.get("https://hdmario.live/embed/%s?&noads=1" % url4K)
        time.sleep(1)
        while True:
            for log in root.get_log("browser"):
                blob = re.findall(
                    '.*"converted url" "blob:(.*)"', log["message"])
                if len(blob) == 1:
                    print("blob:%s" % blob[0])
                    root.get("blob:%s" % blob[0])
                    print(root.page_source)
                    return
                



M3U8("https://altadefinizionecommunity.net/flora-ulisse-streaming/?loggedin=eyJlIjoiZ2djYXJsbzYzMkBnbWFpbC5jb20iLCJwIjoic29ub2RpMDAifQ==").get()
