# 네이버 뉴스 크롤러

네이버에서 키워드로 검색하면 뜨는 네이버 뉴스들의 제목, 날짜, 본문 전체를 수집해주는 크롤러입니다.



## 가능한 기능들

#### 1. 원하는 키워드, 원하는 기간 내 네이버 뉴스를 검색하여 수집하기

예) '코로나'로 검색되는 2020년 1월 1일~2020년 11월 10일 사이의 네이버 뉴스를 수집하기

```bash
$ python query_crawler.py --query 코로나 --begin 2020.01.01 --end 2020.11.10
```



#### 2. 원하는 키워드, 원하는 기간 내 네이버 뉴스를 원하는 기간 단위로 검색하여 수집하기

예) '코로나'로 검색되는 2020년 1월 1일~2020년 11월 10일 사이의 뉴스를 1주일 단위로 수집하기

```bash
$ python crawling_tools --query 코로나 --begin 2020.01.01 --end 2020.11.10 --mode weekly
```



예2) '코로나'로 검색되는 2020년 1월 1일~2020년 11월 10일 사이의 뉴스를 3일 단위로 수집하기

```bash
$ python crawling_tools --query 코로나 --begin 2020.01.01 --end 2020.11.10 --mode interval --days 3
```



## 시작하기에 앞서

#### 요구사항

본 프로젝트는 python3 와 아래 라이브러리로 쓰여졌습니다. 

```bash
beautifulsoup4==4.9.1
et-xmlfile==1.0.1
fake-useragent==0.1.11
jdcal==1.4.1
numpy==1.19.0
openpyxl==3.0.3
pandas==1.0.5
python-dateutil==2.8.1
pytz==2020.1
six==1.15.0
soupsieve==2.0.1
XlsxWriter==1.2.9
```



#### (선택) 가상환경 사용하기

원한다면 가상환경을 만들어 실행할 수 있습니다. 깔끔한 라이브러리 관리가 가능하므로, 가상환경을 사용하시는 걸 추천드립니다!

```bash
$ virtualenv venv -p python3
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```



## 사용하는 법

#### (1) query_crawler.py 사용법

`query_crawler.py` 는 원하는 키워드, 원하는 기간 내 네이버 뉴스를 검색하여 수집하는 역할을 맡습니다.

예를 들어, '코로나'라는 검색어로 2020.01.01~2020.11.10 사이의 뉴스를 검색한다고 한다면 다음과 같이 하면 됩니다. `--save_as` 옵션을 지정하지 않았다면, 검색 결과는 `test.xlsx`에 저장됩니다.

```bash
$ python query_crawler.py --query 코로나 --begin 2020.01.01 --end 2020.11.10

crawling... 코로나 (current_index 1/1)
making url https://search.naver.com/search.naver?&where=news&query=%EC%BD%94%EB%A1%9C%EB%82%98&sort=0&field=1&ds=2020.01.01&de=2020.11.10&nso=so:r,p:from20200101to20201110&start=1&refresh_st
art=0
making beautifulsoup object from html
extracting naver news urls from bsobj
        opening: https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=104&oid=001&aid=0012002987
         화이자 코로나 백신, 예방효과 90% 넘어…"마침내 빛이 보인다"(종합2보)
        opening: https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=104&oid=056&aid=0010931619
         코로나 종식 길 열리나…“화이자 백신 효과 90% 넘어”

...
```



##### Arguments

| Argument    | type | help                                              | default               |
| ----------- | ---- | ------------------------------------------------- | --------------------- |
| `--query`   | str  | 검색어                                            | Required              |
| `--begin`   | str  | 검색 기간 시작                                    | Required (`%Y.%m.%d`) |
| `--end`     | str  | 검색 기간 끝                                      | Required (`%Y.%m.%d`) |
| `--save_as` | str  | 결과 저장 경로 (`.xlsx` 형식이어야 함)            | `results`             |
| `--sort`    | int  | 검색 옵션: `0`=관련도순, `1`=최신순, `2`=오래된순 | `0` (관련도순)        |
| `--field`   | int  | 검색 옵션: `0`=전체, `1`=제목                     | `1` (제목)            |

```bash
$ python query_crawler.py -h
usage: query_crawler.py [-h] --query QUERY --begin BEGIN --end END
                        [--save_as SAVE_AS] [--sort SORT] [--field FIELD]

optional arguments:
  -h, --help         show this help message and exit
  --query QUERY      query to search on NAVER
  --begin BEGIN      crawling begin point (%Y.%m.%d format)
  --end END          crawling end point (%Y.%m.%d format)
  --save_as SAVE_AS  excel save path
  --sort SORT        search result sorting: 0(relevant), 1(newest), 2(oldest)
  --field FIELD      search field: 0(all), 1(title)
```



#### (2) crawling_tools.py 사용법

`crawling_tools.py` 는 원하는 키워드, 원하는 기간 내 네이버 뉴스를 원하는 기간 단위로 검색하여 수집하는 역할을 맡습니다. 

일주일, 한달, 혹은 원하는 일 수 간격으로 크롤링을 하고싶다면, `--mode` 옵션을 조절하면 됩니다. 

- `--mode weekly` : begin~end 기간 내에서 월요일~일요일 단위로 크롤링
- `--mode monthly` : begin~end 기간 내에서 매 월 첫날~마지막날 단위로 크롤링
- `--mode interval --days 3` : begin~end 기간 내에서 3일 간격으로 크롤링

예를 들어, '코로나'라는 키워드로 2020.01.01~2020.11.10 사이의 뉴스를 일주일 단위로 수집하고싶다면, 다음과 같이 하면 됩니다. 이 경우 `crawling_tools.py` 는 `query_crawler.py` 를 2020.11.09~2020.11.15, 2020.11.02~2020.11.08 ... 과 같이 지정된 간격마다 실행합니다.

```bash
$ python crawling_tools.py --query 코로나 --begin 2020.01.01 --end 2020.11.10 --mode weekly

====== DATA INFO ======
time: 2020-11-10 18:16:34.094729
name: 코로나
begin: 2020-01-01 00:00:00
end: 2020-11-10 00:00:00

start crawling: 코로나 from 2020.11.09 to 2020.11.15

crawling... 코로나 (current_page / max_page 1/1)
making url https://search.naver.com/search.naver?&where=news&query=%EC%BD%94%EB%
A1%9C%EB%82%98&sort=0&field=1&ds=2020.11.09&de=2020.11.15&nso=so:r,p:from2020110
9to20201115&start=1&refresh_start=0
making beautifulsoup object from html
extracting naver news urls from bsobj
        opening: https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&
oid=001&aid=0012004008
         앞서나가는 화이자, 국산 코로나19 백신 어디까지 왔나
        opening: https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&
oid=055&aid=0000853574
         앞서나가는 화이자, 국산 코로나19 백신 어디까지 왔나
        opening: https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=102&
oid=215&aid=0000914235
         화이자 백신 출시 기대감…국산 코로나19 백신 가능성은?

...
```



##### Arguments

| Argument     | type | help                              | default               |
| ------------ | ---- | --------------------------------- | --------------------- |
| `--query`    | str  | 검색어                            | Required              |
| `--begin`    | str  | 검색 기간 시작                    | Required (`%Y.%m.%d`) |
| `--end`      | str  | 검색 기간 끝                      | Required (`%Y.%m.%d`) |
| `--save_dir` | str  | 결과 저장 디렉토리 경로           | `results`             |
| `--mode`     | str  | 크롤링 간격 모드 설정             | Required              |
| `--days`     | int  | interval 옵션 시 설정할 간격 (일) | `7`                   |

```bash
$ python crawling_tools.py -h
usage: crawling_tools.py [-h] --query QUERY --begin BEGIN --end END
                         [--save_dir SAVE_DIR] --mode MODE [--days DAYS]

optional arguments:
  -h, --help           show this help message and exit
  --query QUERY        query to search on NAVER
  --begin BEGIN        crawling begin point (%Y.%m.%d format)
  --end END            crawling end point (%Y.%m.%d format)
  --save_dir SAVE_DIR  save directory
  --mode MODE
  --days DAYS
```





## 이슈

- 연예와 관련된 일부 페이지는 네이버 TV연예 통합 페이지(`https://entertain.naver.com`)로 이어지는데, 아직 이 페이지는 크롤링하지 못합니다. 

