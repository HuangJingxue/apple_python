
- 获取君子协议
```python
https://y.qq.com/robots.txt
User-agent: *
Disallow: /playlist/
Disallow: /yqq/playlist/
Disallow: /n/yqq/playlist/
```

- 获取HTML网页讨论共同点
```python
评论内容在 class="c_tx_normal comment__text js_hot_text" 的 p 标签内

import requests
from bs4 import BeautifulSoup

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
res = requests.get('https://y.qq.com/n/yqq/song/001J5QJL1pRQYB.html', headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
comments = soup.find_all('p', class_='c_tx_normal comment__text js_hot_text')
print(comments)
# 输出：[]
```
