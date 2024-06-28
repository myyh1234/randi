# randi

오전 6시마다 새로운 문제 선정

`app.py`와 같은 디렉토리에 `info.py` 파일이 있어야 하며, 해당 파일에는 아래와 같은 형식의 딕셔너리인 `user_list` 변수가 있어야 합니다.

`user_list` 변수는 각 난이도의 문제를 풀 사람의 BOJ 핸들 목록을 담습니다.
```python
user_list = {
        'Bronze':['boj 핸들'],
        'Silver':['boj 핸들1', 'boj 핸들2', 'boj 핸들3', ],
        'Gold':['boj 핸들4', 'boj 핸들5'],
        'Platinum':['boj 핸들6']
    }
```
