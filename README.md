# 네이버 뉴스 크롤러

네이버에서 키워드로 검색하면 뜨는 네이버 뉴스들의 제목, 날짜, 본문 전체를 크롤링해주는 봇입니다. 



## 시작하기에 앞서

#### 요구사항

본 프로젝트는 python3 와 아래 라이브러리로 쓰여졌습니다. 

```bash
beautifulsoup4==4.9.0
openpyxl=3.0.3
pandas=1.0.5
```



#### (선택) 가상환경 사용하기

원한다면 가상환경을 만들어 실행할 수 있습니다. 깔끔한 라이브러리 관리가 가능하므로, 가상환경을 사용하시는 걸 추천드립니다!

```bash
$ virtualenv venv -p python3
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```



## 사용하는 법

#### (1) 기본 사용법

```bash
$ python query_crawler.py -h
usage: query_crawler.py [-h] --query QUERY --begin BEGIN --end END
                        [--path PATH] [--limit LIMIT] [--sort SORT]
                        [--field FIELD] [--sleep SLEEP]

optional arguments:
  -h, --help     show this help message and exit
  --query QUERY  query to search on NAVER
  --begin BEGIN  crawling begin point
  --end END      crawling end point
  --path PATH    saving path for crawling results
  --limit LIMIT  crawling page limit on single query, 0 for no limit
  --sort SORT    search result sorting: 0(relevant), 1(newest), 2(oldest)
  --field FIELD  search field: 0(all), 1(title)
  --sleep SLEEP  sleep interval between requests
```

