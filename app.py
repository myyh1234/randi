from flask import Flask, render_template, send_from_directory
import requests, datetime, sys
from apscheduler.schedulers.background import BackgroundScheduler
from info import *
from add_practice import *

app = Flask(__name__)

def date_to_str(date):
    WEEKDAY = {0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'}
    return f'{date.year}년 {date.month}월 {date.day}일 ({WEEKDAY[date.weekday()]})'

DATE = date_to_str(datetime.datetime.now() - datetime.timedelta(days=1))
next_date = ''
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

def set_problem(start_time = '06:00'):
    global DATE, next_problems, next_date

    ret = {}
    url = "https://solved.ac/api/v3/search/problem"
    now_user = []

    problem_str = ''
    for level in user_list:
        problem_str += level + ": "
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
            ret[level] = []
        else:
            now_problem = []
            for i in range(3):
                now_problem.append(Problem(
                    problem_id=problems[i]["problemId"], 
                    title=problems[i]["titleKo"], 
                    level=problems[i]["level"]
                ))
                problem_str += str(problems[i]["problemId"]) + " "
            ret[level] = now_problem
        problem_str += "\n"
            
    next_problems = ret

    t = datetime.datetime.now()
    
    next_date = date_to_str(t)

    with open("problem_history.txt", "a") as f:
        f.write(next_date + "\n" + problem_str)

    if not make_practice(t.strftime('%m/%d') + " Random Defense", t, start_time, next_problems):
        print('login failed', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # print("problem set: ")
    # print(problem_list)
    # print(DATE)
    print('changed')

def check_solved():
    global problem_list, DATE
    LEVELS = ['Platinum', 'Gold', 'Silver', 'Bronze']
    with open('no-solve.txt', 'a') as f:
        f.write(DATE + '\n')
        problem_query = ''
        url = "https://solved.ac/api/v3/search/problem"
        headers = {
            "x-solvedac-language": "ko",
            "Accept": "application/json"
        }
        for lv in LEVELS:
            if not problem_list[lv]:
                continue
            for p in problem_list[lv]:
                problem_query += '|' + p.problem_id
            if problem_query[0] == '|':
                problem_query = problem_query[1:]
            # print(problem_query)
            for user in user_list[lv]:
                response = requests.get(url, headers=headers, params={"query":f'({problem_query}) @{user}'}).json()['items']
                # print(user, end=' ')
                # for i in response:
                #     print(i['titleKo'], end=' ')
                # print()
                if len(response) == 0:
                    f.write(user + " " + user_name_map[user] + "\n")
    print('check solved function end')
    
def update_problem(chk = True):
    global problem_list, next_problems, DATE, next_date
    if chk: 
        check_solved()
    problem_list = next_problems
    DATE = next_date
    print('updated')

@app.route('/')
def root():
    global DATE, problem_list
    return render_template('main.html', update_time = DATE, problem_list = problem_list)

@app.route('/css/<path:text>')
def css(text):
    return send_from_directory('css', text)

if __name__ == '__main__':
    # if not login():
    #     print("login failed")
    # else:
    #     print("login")
    
    worker = BackgroundScheduler(timezone='Asia/Seoul')
    
    if len(sys.argv) > 1:
        url = "https://solved.ac/api/v3/search/problem"
        headers = {
            "x-solvedac-language": "ko",
            "Accept": "application/json"
        }
        
        got = sys.argv[1].split(',')
        if len(got) != 3*len(problem_list):
            print("Wrong number of problem")
        for i, lv in enumerate(problem_list):
            tmp = []
            for x in range(3):
                now_num = got[i*3+x]
                if now_num:
                    response = requests.get(url, headers=headers, params={"query":now_num})
                    problem = response.json()['items'][0]
                    tmp.append((Problem(
                        problem_id=problem["problemId"], 
                        title=problem["titleKo"], 
                        level=problem["level"]
                    )))

            next_problems[lv] = tmp
        
        next_date = date_to_str(datetime.datetime.now() - datetime.timedelta(hours=6))
        update_problem(False)
    # else:
    #     worker.add_job(lambda: set_problem('06:20'), 'date', run_date='2024-07-02 06:15:00')
    #     worker.add_job(lambda: update_problem(False), 'date', run_date='2024-07-02 06:20:00')
    
    worker.add_job(set_problem, 'cron', hour=0)
    worker.add_job(update_problem, 'cron', hour=6)
    worker.start()
    app.run(host='0.0.0.0', port=80)
    # app.run()
