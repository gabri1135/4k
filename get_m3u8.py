from selenium.webdriver import Edge
import re


class M3U8:
    def __init__(self, url):
        self.url = url

    def get(self):
        root = Edge(
            executable_path="C:\\Users\\marti\\Downloads\\edgedriver_win64\\msedgedriver.exe")
        root.get(self.url)
        email=root.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/form/div[1]/input")
        email.send_keys("ggcarlo632@gmail.com")
        pas=root.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/form/div[2]/input")
        pas.send_keys("sonoi00")
        butt=root.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/form/div[3]/button")
        butt.submit()
        page=re.findall(
            'https://hdpass.click/movie/(.*)\?noads=1', root.page_source)[0]
        root.get("https://hdpass.click/movie/%s?resolution=2&noads=1"%page)
        url4K=re.findall(
            'https://hdmario.live/embed/(.*)/?&amp;noads=1', root.page_source)[0]
        root.get("https://hdmario.live/embed/%s?&noads=1"%url4K)
        print(root.get_log("browser"))
        #k4=root.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[2]/div[12]/div[1]/div/div/div[2]/div")
        #k4.submit()


# elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div[1]/div/label/input")
# elem.send_keys("zeb98@gmail.co")
# mail=driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input")
# mail.send_keys("martinigay")
# button = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/form/button")
# button.submit()
# time.sleep(1)
# if driver.current_url!="https://www.netflix.com/login":
#     driver.get("https://www.netflix.com/logout")


M3U8("https://altadefinizionecommunity.net/flora-ulisse-streaming/?loggedin=eyJlIjoiZ2djYXJsbzYzMkBnbWFpbC5jb20iLCJwIjoic29ub2RpMDAifQ==").get()
