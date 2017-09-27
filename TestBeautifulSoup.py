from bs4 import BeautifulSoup
import re
html = '''
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<c href="http://example.com/elsie" class="sister" id="link1"><!--This is a comment--></c>,

<p class="story">...</p>
'''

soup = BeautifulSoup(html,'lxml')
# print(soup.prettify())

# 1. Tag:
# 可以通过soup.TagName来得到标签, 但是返回的只是第一个满足条件的标签
print('\n\n','*'*60,'Tag','*'*60,'\n')
print(type(soup.head))
print(soup.head,'***name=',soup.head.name,'***attr=',soup.head.attrs)
print(soup.title,'***name=',soup.title.name,'***attr=',soup.title.attrs)
print(soup.p,'***name=',soup.p.name,'***attr=',soup.p.attrs)
print(soup.b,'***name=',soup.b.name,'***attr=',soup.b.attrs)
print(soup.a,'***name=',soup.a.name,'***attr=',soup.a.attrs)
# 获取Tag的属性attrs
for att,val in soup.a.attrs.items():
    print(att,'====',val)

# 2. NavigableString:可遍历字符串
# 获取Tag的文字内容, Tag.string
print('\n\n','*'*60,'NavigableString','*'*60,'\n')
print(type(soup.a.string))
print(type(soup.a.get_text()))
print(soup.a.get_text(),soup.a.string)

# 3. BeautifulSoup:
# BeautifulSoup对象表示的是一个文档的全部内容.大部分时候,可以把它当作Tag对象,它支持遍历文档树和搜索文档树中描述的大部分的方法.
print('\n\n','*'*60,'BeautifulSoup','*'*60,'\n')
print(type(soup))
print(soup.name)
print(soup.attrs)


# 4. Comment:
# Tag , NavigableString , BeautifulSoup 几乎覆盖了html和xml中的所有内容,但是还有一些特殊对象.容易让人担心的内容是文档的注释部分:
# Comment 对象是一个特殊类型的 NavigableString 对象:
print('\n\n','*'*60,'Comment','*'*60,'\n')
print(soup.c)
print(soup.c.string)
print(type(soup.c.string))


# 5. 遍历文档树
# 5.1 直接子节点: Tag.contents[返回列表], Tag.children[返回listiterator]
print('\n\n','*'*60,'Iterate the DOM','*'*60,'\n')
# contents
cont = soup.body.contents
print(type(cont),'len(cont)=',len(cont))
for i in cont:
    print('>>>',i)

# children
chils = soup.body.children
print(type(chils),chils)
for i in chils:
    print("*"*20,i)

# 5.2 所有子孙节点: Tag.descendants[可以对所有tag的子孙节点进行递归循环，和 children类似，我们也需要遍历获取其中的内容。]
print(type(soup.descendants))
for item in soup.descendants:
    print("所有子孙节点:",item)

# 5.3 节点的内容:Tag.string,
# 如果tag只有一个 NavigableString 类型子节点,那么这个tag可以使用 Tag.string得到子节点.
# 如果一个tag仅有一个子节点,那么这个tag也可以使用Tag.string方法,输出结果与当前唯一子节点的Tag.string 结果相同.
# 如果tag包含了多个子节点,tag就无法确定Tag.string应该调用哪个子节点的内容,Tag.string的输出结果是None
body = soup.body
print(body.string)
print(soup.title.string)

# 5.4 节点的多个内容: Tag.strings, Tag.stripped_strings[去除空格]
for i in body.strings:
    print('节点的多个内容',i)
for i in body.stripped_strings:
    print('节点的多个内容',i)

# 5.5 父亲节点: Tag.parent
title = soup.title
print(title.parent)

# 5.6 全部父亲节点: Tag.parents
for i in (title.parents):
    print('全部父亲节点',i.name)

# 5.7 兄弟节点: Tag.next_sibling, Tag.previous_sibling
a = soup.a
print(a)
while a != None:
    a = (a.next_sibling)
    print(a)

# 5.8 全部兄弟节点: Tag.next_siblings, Tag.previous_siblings
a = soup.a
for i in a.next_siblings:
    print("全部兄弟节点",i)

# 5.9 前后节点: Tag.next_element, Tag.previous_element
# 与Tag.next_sibling, Tag.previous_sibling不同, 它并不是针对于兄弟节点, 而是在所有节点,不分层次
print('前后节点',a.previous_element)

# 5.10 全部前后节点: Tag.next_elements, Tag.previous_elements
for i in a.previous_elements:
    print('全部前后节点：', i.name)


# 6 搜索文档树 : find_all( name , attrs , recursive , text , **kwargs )
# 6.1 name参数:
# 1.字符串, 2.正则表达式, 3.列表, 4.True, 5.函数
for i in soup.find_all(['a','b','c']):
    print('搜索所有文档: ', i)
for i in soup.find_all(re.compile('^b')):
    print('搜索文档with正则: ', i.name)

def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
for i in soup.find_all(has_class_but_no_id):
    print('搜索文档with函数: ', i.name)

# 6.2 keyword参数:
for i in soup.find_all(id='link1'):
    print('keyword参数id : ',i)

#class是python的关键词, 因此使用class_
for i in soup.find_all(class_='sister'):
    print('keyword参数class_ : ', i)

# 6.3 text参数:
for i in soup.find_all(text=['Elsie','Lacie']):
    print('text参数 : ', i)
for i in soup.find_all(text=re.compile('Dormouse')):
    print('text参数 : ',i)


# 6.4 limit参数:
for i in soup.find_all('a',limit=2):
    print('limit参数 : ',i)

# 6.5 recursive参数:
# 调用tag的find_all()方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数recursive=False
for i in soup.find_all('title',recursive=False):
    print('recursive参数 : ',i)
for i in soup.find_all('html',recursive=False):
    print('recursive参数 : ',i)

# 6.6 find( name , attrs , recursive , text , **kwargs )
# 它与find_all()方法唯一的区别是find_all()方法的返回结果是值包含一个元素的列表,而find()方法直接返回结果
print('find : ',soup.find('a'))


# find_parents()  find_parent()
# find_next_siblings()  find_next_sibling()
# find_previous_siblings()  find_previous_sibling()
# find_all_next()  find_next()
# find_all_previous() 和 find_previous()

# 7. CSS查找:
# 写CSS标签名不加任何修饰, 类名前加点, id名前加#, 在这里我们也可以利用类似的方法来筛选元素，用到的方法是soup.select(), 返回类型是list
# 7.1 通过标签名查找
soup.select('title')

# 7.2 通过类名查找
for i in soup.select('.sister'):
    print('通过类名查找 : ', i)

# 7.3 通过id名查找
for i in soup.select('#link1'):
    print('通过id名查找 : ',i)

# 7.4 组合查找
for i in soup.select('p #link1'):
    print('组合查找 : ',i)

# 7.5 属性查找
for i in soup.select('a[class="sister"]'):
    print('属性查找 : ', i)