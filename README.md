# 인스타그램 크롤러

[English translation](README-eng.md)

인스타그램을 크롤링해주는 봇입니다. 현재 구현된 기능은 다음과 같습니다:

(1) 원하는 태그를 지정해 최근 포스트부터 크롤링 하기

(2) 원하는 장소를 지정해 최근 포스트부터 크롤링 하기



## 시작하기에 앞서

#### 요구사항

본 프로젝트는 python3 와 아래 라이브러리로 쓰여졌습니다. 

```
beautifulsoup4==4.9.0
soupsieve==2.0
```



#### (선택) 가상환경 사용하기

원한다면 가상환경을 만들어 실행할 수 있습니다. 깔끔한 라이브러리 관리가 가능하므로, 가상환경을 사용하시는 걸 추천드립니다!

```bash
$ virtualenv venv -p python3
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```



## 사용하는 법

#### (1) 태그로 크롤링하기

예를 들어 'coffee'라는 태그를 가진 포스트들을 크롤링해보려고 한다면, 다음과 같이 실행하면 됩니다. 

```bash
$ python crawler.py --mode tag --target coffee
(tags/coffee) opening url: https://www.instagram.com/explore/tags/coffee/
(tags/coffee) 70 posts to be added (merged_results: 0)
...
```

 크롤링 시작 직후부터 `result/tags` 디렉토리에 `coffee.json` 파일이 생성됩니다. 만약 크롤링을 도중에 중단 한 뒤, 나중에 다시 시작한다면 현재까지 저장된 포스트를 읽어 크롤링을 알아서 다시 이어하게 됩니다. 

 `coffee.json`  파일은 각 포스트의 고유한 id를 key로, 포스트의 내용과 관련된 메타데이터를 value로 가지며, 메타데이터는 다시 종류별로 각각 key와 value를 가집니다. 아래는 `coffee.json` 을 열어 본 것입니다. 

![](_src/img/json.PNG)

| Key                | Value                                    |
| ------------------ | ---------------------------------------- |
| id                 | 포스트가 갖는 고유한 id                  |
| owner              | 포스트를 올린 사람의 고유한 id           |
| taken_at_timestamp | 포스트를 올린 시간의 타임스탬프          |
| shortcode          | 포스트 주소                              |
| text               | 내용                                     |
| caption            | 댓글                                     |
| is_video           | 올린 것이 비디오면 True, 아니면 False    |
| display_url        | 처음으로 보여지는 대표 이미지/비디오 url |



#### (2) 장소로 크롤링하기

인스타그램 포스트를 올릴 때 설정하는 위치 정보는 모두 고유한 location ID를 가지고 있습니다. 위에서 인스타그램 포스트의 태그로 크롤링을 한 것 처럼, 포스트에 Geo-tag된 장소의 location ID로 크롤링을 할 수도 있습니다. 

예를 들어 합정역으로 위치 정보를 입력한 포스트들을 크롤링한다고 하면, 먼저 아래와 같이 합정역의 location ID를 얻을 수 있습니다. 

![Inkedlocaion_guide_01](_src/img/Inkedlocaion_guide_01.jpg)



![Inkedlocaion_guide_02](_src/img/Inkedlocaion_guide_02.jpg)



하늘 색 쳐진 숫자 부분이 합정역의 location ID에 해당하는 부분입니다. 이제 태그로 크롤링 할 때와 비슷한 방식으로 실행하면 크롤링이 시작됩니다. 결과물은  `result/locations`에 저장되며, 형식은 태그로 할 때와 같습니다.

```bash
$ python crawler.py --mode location --target 251020013
(locations/251020013) opening url: https://www.instagram.com/explore/locations/2
51020013/
(locations/251020013) 24 posts to be added (merged_results: 0)
...
```



## Arguments

```bash
$ python crawler.py -h
usage: crawler.py [-h] --mode MODE --target TARGET [--limit LIMIT]

optional arguments:
  -h, --help       show this help message and exit
  --mode MODE      crawling mode among: tag, locationid
  --target TARGET  crawling target
  --limit LIMIT    Post # limit (default=1000). 0 for no limit.
```

