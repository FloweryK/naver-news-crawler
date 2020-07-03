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

예를 들어 '네이버'라는 검색어로 뉴스를 검색한다고 한다면, `--query` 인자로 넘겨 다음과 같이 실행하면 됩니다.

```bash
$ python query_crawler.py --query 네이버 --begin 2020.01.01 --end 2020.03.01

crawling... 네이버 (page 1/1)
opening url: https://search.naver.com/search.naver?&where=news&query=%EB%84%A4%EC%9D%B4%EB%B2%84&sort=0&field=1&ds=2020.01.01&de=2020.03.01&
nso=so:r,p:from20200101to20200301&start=1&refresh_start=0
parsing html
        opening inside https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=092&aid=0002182034
        opening inside https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=015&aid=0004298040
...
```



#### (2) 추가 기능



| Argument    | type | help                                              | default               |
| ----------- | ---- | ------------------------------------------------- | --------------------- |
| `--query`   | str  | 검색어                                            | Required              |
| `--begin`   | str  | 검색 기간 시작                                    | Required (`%Y.%m.%d`) |
| `--end`     | str  | 검색 기간 끝                                      | Required (`%Y.%m.%d`) |
| `--savedir` | str  | 결과 저장 경로                                    | `results`             |
| `--sort`    | int  | 검색 옵션: `0`=관련도순, `1`=최신순, `2`=오래된순 | `0` (관련도순)        |
| `--field`   | int  | 검색 옵션: `0`=전체, `1`=제목                     | `1` (제목)            |



## Arguments

```bash
$ python query_crawler.py -h
usage: query_crawler.py [-h] --query QUERY --begin BEGIN --end END
                        [--savedir SAVEDIR] [--sort SORT] [--field FIELD]

optional arguments:
  -h, --help         show this help message and exit
  --query QUERY      query to search on NAVER
  --begin BEGIN      crawling begin point (%Y.%m.%d format)
  --end END          crawling end point (%Y.%m.%d format)
  --savedir SAVEDIR  save directory
  --sort SORT        search result sorting: 0(relevant), 1(newest), 2(oldest)
  --field FIELD      search field: 0(all), 1(title)
```

