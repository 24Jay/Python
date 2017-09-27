import requests
import json

# requests的使用
# requests.get()
response = requests.get("http://localhost:31547")
content = response.content

# print(response.content)
print('\n','*'*50,'GET','*'*50)
print(type(response))
print(response.encoding)
print(response.status_code)
print(response.text)



# requests.post to get cookies
print('\n','*'*50,'POST for login','*'*50)
body = {"userName":"admin","password":123456}
r = requests.post('http://localhost:31547/login',data=body)
print("PostResponse.status = ",r.status_code)
print('PostResponse.txt = ',r.text)
print('PostResponse.cookies',r.cookies)
# cookies
cks = r.cookies


# requests.get with cookies
print('\n','*'*50,'GET all users with cookies','*'*50)
r = requests.get('http://localhost:31547/user',cookies=cks)
print(r.text)

print('\n','*'*50,'GET user info with cookies','*'*50)
r = requests.get('http://localhost:31547/user/1',cookies=cks)
print(r.text)

# requests.get articles
print('\n','*'*50,'GET all articles with cookies','*'*50)
r = requests.get('http://localhost:31547/article',cookies=cks)
print(r.text)


print('\n','*'*50,'GET article info','*'*50)
r = requests.get('http://localhost:31547/article/4',cookies=cks)
print(r.text)

# requests.post for add a article
print('\n','*'*50,'Add article','*'*50)
# body
body = {
    "id": 39,
    "title": "机器学习Machine Learning",
    "content": "机器学习与人工智能",
    "authorId": "1"
}
# headers
headers = {'Content-type': 'application/json'}
r = requests.post('http://localhost:31547/article',cookies=cks,data=json.dumps(body),headers=headers)
print(r.text)

# requests.put for update article
print('\n','*'*50,'Update article','*'*50)
body = {
    "id": 35,
    "title": "机器学习Machine Learning",
    "content": "机器学习与人工智能, 深度学习",
    "authorId": "1"
}
headers = {'Content-type': 'application/json'}
r = requests.put('http://localhost:31547/article/35',cookies=cks,data=json.dumps(body),headers=headers)
print(r.text)


# requests.delete a article
print('\n','*'*50,'Delete article','*'*50)
headers = {'Content-type': 'application/json'}
r = requests.delete('http://localhost:31547/article/34',cookies=cks,data=json.dumps(body),headers=headers)
print(r.text)
