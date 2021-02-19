from selenium.webdriver import Edge
import requests
import re


class M3U8:
    def __init__(self, url):
        self.url = url

    def get(self):
        root = Edge(
            executable_path="C:\\Users\\marti\\Downloads\\edgedriver_win64\\msedgedriver.exe")

        headers = {"X-Secure-Proof": "pyTQsmrq-jBTIgtPhBK1kA"
                   }
        html = requests.get(self.url).text
        iframe = re.findall(
            '<iframe allowfullscreen src="(.*)"></iframe>', html)
        m3u8 = re.findall(
            'https://hdmario.live/embed/(.*)\?&amp;noads=1', iframe[0])
        print(
            'https://hdmario.live/embed/%s?loggedin=eyJlIjoiZ2djYXJsbzYzMkBnbWFpbC5jb20iLCJwIjoic29ub2RpMDAifQ==' % m3u8[0])
        root.get('https://hdmario.live/embed/%s?loggedin=1613756278' %
                 m3u8)

# elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div[1]/div/label/input")
# elem.send_keys("zeb98@gmail.co")
# mail=driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input")
# mail.send_keys("martinigay")
# button = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/form/button")
# button.submit()
# time.sleep(1)
# if driver.current_url!="https://www.netflix.com/login":
#     driver.get("https://www.netflix.com/logout")


M3U8("https://hdpass.click/movie/28927?resolution=2&noads=1").get()
