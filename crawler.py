import requests
from bs4 import BeautifulSoup
import lxml
import time

# 標頭檔
HADERS = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68"}

# 取得搜尋網址內容
def getSearchURL(url):
    html = requests.get(url, headers = HADERS)
    soup = BeautifulSoup(html.text, "lxml")

    return soup

# 取得總頁數
def getTotalPage(soup):
    totalPage = soup.select_one("p.BH-pagebtnA > a:last-child").text

    return totalPage

# 取得樓層
def getFloor(soup):
    floor_list = soup.select(".c-post__header__author .floor")

    return floor_list

# 取得資料
def getContent(soup, menu):
    if(menu == "1"):    # 回覆
        content_list = soup.select(".c-article__content")
    elif(menu == "2"):  # 作者
        content_list = soup.select(".c-post__header__author .userid")

    return content_list


if __name__ == "__main__":
    # 取得欲搜尋討論串
    search_url = input("請輸入要搜尋的討論串網址: ") # https://forum.gamer.com.tw/C.php?bsn=60030&snA=398025&tnum=2892

    # 取得總頁數
    totalPage = getTotalPage(getSearchURL(search_url))

    while(True):
        # 選擇功能
        menu = input("選擇功能  1.搜尋內容 2.搜尋作者 3.離開: ")
        if(menu == "3"):break

        # 取得欲搜尋內容
        search_word = input("請輸入要搜尋的內容 or 作者: ")

        # 遍歷每頁
        for page in range(int(totalPage)):
            url = "{}&page={}".format(search_url,page+1)

            soup = getSearchURL(url)
            floor_list = getFloor(soup)

            if(menu == "1"):
                content_list = getContent(soup, menu)

                for floor, content in zip(floor_list, content_list):
                    # 比對字串
                    if(content.text.find(search_word) != -1):
                        print(floor.text + content.text)
            
            elif (menu == "2"):
                content_list = getContent(soup, "1")
                author_list = getContent(soup, menu)

                for floor, content,author in zip(floor_list, content_list, author_list):
                    # 比對字串
                    if(author.text.find(search_word) != -1):
                        print(floor.text  + " " + author.text + content.text)
                
            
            time.sleep(0.1)
    