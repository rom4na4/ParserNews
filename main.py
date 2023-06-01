from bs4 import BeautifulSoup
import requests
import json

urls = ['https://amur.info/category/society/']  # поиск пока по 1 ресурсу - можно добавить через запятую ещё
news = []
filteredNews = dict.fromkeys(['sourceName', 'link', 'title', 'time', 'descr', 'img'])

for i in urls:
    page = requests.get(i)
    if page.status_code == 200:
        print("Загрузился ресурс ", i)
        parser = BeautifulSoup(page.text, 'html.parser')
        articles = parser.find_all('div', 'long-news-block with-text')
        for data in articles:
            link = data.find('a', 'long-news-block__img-block')['href']
            img = data.find('img', 'long-news-block__img')['src']
            time = data.find('a', 'news-date').text
            title = data.find('a', 'h2').text
            descr = data.find('p', 'long-news-block__fragment').text
            filteredNews['sourceName'] = i
            filteredNews['link'] = link
            filteredNews['title'] = title
            filteredNews['time'] = time
            filteredNews['descr'] = descr
            filteredNews['img'] = img
            news.append(filteredNews.copy())
        with open("data_file.json", "w") as write_file:
            json.dump(news, write_file, indent=4)

    else:
        print("не загрузился ресурс ", i)
