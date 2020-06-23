# 네이버 뉴스 크롤러

네이버에서 키워드로 검색하면 뜨는 네이버 뉴스들의 제목, 날짜, 본문 전체를 크롤링해주는 봇입니다. 



#### 현재 구현된 기능

(1) 키워드로 검색했을 때 나오는 네이버 뉴스들의 제목, 날짜 본문 전체 크롤링

(2) 원하는 기간의 검색 결과 크롤링

(3) 검색 결과 정렬 옵션 선택: 

​		(3-a) 관련도순/최신순/오래된순 정렬

​		(3-b) 전체/제목 연관 정렬



#### 이슈

연예인과 관련된 일부 페이지는 네이버 TV연예 통합 페이지(`https://entertain.naver.com`)로 이어지는데, 아직 이 페이지는 크롤링하지 못합니다ㅠㅅㅠ 다양한 분야에 관한 크롤링이 차차 추가될 예정입니다.



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

#### (1) 기본적인 사용법

예를 들어 '카카오'라는 검색어로 뉴스를 검색한다고 한다면, `--query` 인자로 넘겨 다음과 같이 실행하면 됩니다.

```bash
$ python query_crawler.py --query 카카오

crawling... 카카오 (page 1/1)
opening url: https://search.naver.com/search.naver?&where=news&query=%EC%B9%B4%EC%B9%B4%EC%98%A4&sort=0&field=1&ds=2020.01.01&de=2020.06.23&nso=so:r,p:from20200101to20200623&start=1&refresh_start=0

crawling... 카카오 (page 2/10)
opening url: https://search.naver.com/search.naver?&where=news&query=%EC%B9%B4%EC%B9%B4%EC%98%A4&sort=0&field=1&ds=2020.01.01&de=2020.06.23&nso=so:r,p:from20200101to20200623&start=11&refresh_start=0

crawling... 카카오 (page 3/10)
opening url: https://search.naver.com/search.naver?&where=news&query=%EC%B9%B4%EC%B9%B4%EC%98%A4&sort=0&field=1&ds=2020.01.01&de=2020.06.23&nso=so:r,p:from20200101to20200623&start=21&refresh_start=0

...
```



#### (2) 추가 기능



| Argument  | type  | help                                              | default                     |
| --------- | ----- | ------------------------------------------------- | --------------------------- |
| `--query` | str   | 검색어                                            | Required                    |
| `--begin` | str   | 검색 기간 시작                                    | `2020.01.01`                |
| `--end`   | str   | 검색 기간 끝                                      | 오늘 날짜의 `%Y.%m.%d` 형식 |
| `--path`  | str   | 결과 저장 경로                                    | `results/`                  |
| `--limit` | int   | 페이지 한계                                       | `300`                       |
| `--sort`  | int   | 검색 옵션: `0`=관련도순, `1`=최신순, `2`=오래된순 | `0` (관련도순)              |
| `--field` | int   | 검색 옵션: `0`=전체, `1`=제목                     | `1` (제목)                  |
| `--sleep` | float | anti-crawling을 막기 위한 sleep time (sec)        | `1.` (sec)                  |



## Arguments

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

