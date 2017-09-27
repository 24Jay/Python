# /user/bin/python3.5
from bs4 import BeautifulSoup
import requests
import codecs
import bs4.element


# 获取每一章的文本
def getPage(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html,'html.parser')
    # print(soup.prettify())

    soup_txt = soup.find('div', id='htmlContent',class_="contentbox")

    title_tag = soup.find('div',class_="h1title")
    titles = title_tag.h1.string
    print("titles = "+(titles))
    content = ">>>>>>>>>>>>"+titles+"\n"
    for c in soup_txt.children:
        if c != None:
            if type(c) == bs4.element.Tag:
                content +=c.get_text()

    content = content.strip()
    return content



# 获取某一本书的所有章节url
def getBook(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    soup_txt = soup.find('div', class_="book_list")

    print("*"*90)

    linkList = list()
    index = ""
    for link in soup_txt.ul.children:
        if link != '\n':
            hrf = link.a.get('href')
            title = link.a.string

            print("title="+title, end="\t")
            print("link="+hrf)
            index += title+"\n"
            linkList.append(hrf)
    return linkList,index


# 获取金庸全集书的url : {书名:url}
def getList(url):
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')

    soup_list= soup.find_all('div',  class_="bk")

    print(soup_list)

    bookList = dict()

    for i in soup_list:
        print("---" * 30)
        print(i.h3.a)
        href = i.h3.a.get('href')
        title = i.h3.a.get('title')
        bookList[title]=href
        print("---" * 30)
    print(bookList)

    return bookList



# 运行主程序, 先获取金庸全集的书名:url, 然后逐一去爬取数据，保存到对应的txt文件中
if __name__ == "__main__":
    # get a list for bookName:url
    bookList = dict(getList('http://jinyong.zuopinj.com/'))

    for title,url  in bookList.items():
        # get all url
        print(">>>>>>>>>>>>>>"+title)
        print(">>>>>>>>>>>>>>"+url)

        lis,index = getBook(url)

        f = codecs.open(title+".txt",'w','utf-8')
        f.write(index)
        f.write("**"*50)
        f.write("\n\n")
        for uri in lis:
            print("--"*40)
            cont = getPage(uri)
            f.write(uri+"\n")
            f.write(cont+'\n\n')
            f.write("**"*50)
            f.write("\n\n")
        f.close()