from flask import Flask, render_template
import requests, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from info import user_list
from add_practice import make_practice

app = Flask(__name__)
DATE = ''

problem_list = {"Bronze":[], "Silver":[], "Gold":[], "Platinum":[]}
next_problems = {}

class Problem:
    def __init__(self, problem_id, title, level):
        self.problem_id = str(problem_id)
        self.title = title
        self.level = str(level)
        self.img_src = str(level) + '.svg'
        self.alt_level = 'BSGP'[(level-1) // 5] + str(5 - level % 5)
        self.url = 'https://www.acmicpc.net/problem/' + str(problem_id)
    
    def __str__(self):
        return f'{self.level} {self.problem_id} {self.title}'
    
    def __repr__(self):
        return str(self)

def set_problem():
    global DATE, next_problems

    ret = {}
    url = "https://solved.ac/api/v3/search/problem"
    now_user = []

    for level in user_list:
        now_user += user_list[level]
        query = f'*{level[0].lower()} %ko -(@{"|@".join(now_user)})'
        querystring = {"query":query, "sort":"random"}
        headers = {
            "x-solvedac-language": "ko",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, params=querystring)

        problems = response.json()['items']
        if len(problems) < 3:
            ret.append([])
        else:
            now_problem = []
            for i in range(3):
                now_problem.append(Problem(
                    problem_id=problems[i]["problemId"], 
                    title=problems[i]["titleKo"], 
                    level=problems[i]["level"]
                ))
            ret[level] = now_problem
            
    next_problems = ret

    t = datetime.datetime.now()
    WEEKDAY = {0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'}
    DATE = f'{t.year}년 {t.month}월 {t.day}일 ({WEEKDAY[t.weekday()]})'
    # DATE += ' ' + t.strftime('%m/%d %H:%M')

    make_practice(t.strftime('%m/%d') + " Random Defense", t, next_problems)

    # print("problem set: ")
    # print(problem_list)
    # print(DATE)
    # print('changed')
    
def update_problem():
    global problem_list, next_problems
    problem_list = next_problems
    # print('updated')

@app.route('/')
def root():
    global DATE, problem_list
    return render_template('main.html', update_time = DATE, problem_list = problem_list)

if __name__ == '__main__':
    with app.app_context():
        if not problem_list:
            set_problem()
    worker = BackgroundScheduler(timezone='Asia/Seoul')
    worker.add_job(set_problem, 'cron', hour=5, minute=30)
    worker.add_job(update_problem, 'cron', hour=6)
    worker.start()
    app.run(host='172.26.8.200')
    # app.run()
