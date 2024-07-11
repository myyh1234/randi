from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from random import random
import datetime, time
from info import PASSWORD

GROUP_ID = 20229

def build_driver():
    options = Options()
    # options.add_argument("--single-process")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def login(driver = False):
    global GROUP_ID
    if not driver:
        driver = build_driver()
    driver.get(url=f'https://www.acmicpc.net/group/practice/{GROUP_ID}')
    driver.implicitly_wait(time_to_wait=5)

    if driver.title == '로그인':
        id_box = driver.find_element(By.NAME, 'login_user_id')
        for c in 'myyh1234':
            id_box.send_keys(c)
            time.sleep(random()/2)
        time.sleep(random() * 2)

        pw_box = driver.find_element(By.NAME, 'login_password')
        for c in PASSWORD:
            pw_box.send_keys(c)
            time.sleep(random()/2)
        time.sleep(random() * 2)

        auto_checkbox = driver.find_element(By.NAME, 'auto_login')
        auto_checkbox.click()
        time.sleep(random() * 2)

        submit = driver.find_element(By.ID, 'submit_button')
        submit.click()

        time.sleep(5)
        if driver.title == '로그인':
            return False

    print('login')
    return True

def make_practice(title: str, today: datetime.datetime, start_time: str, problems):
    global GROUP_ID
    # options.add_argument("--headless")
    # if __name__ == '__main__':
    #     options.add_experimental_option("detach", True)

    driver = build_driver()
    
    if not login(driver):
        return False

    driver.get(f'https://www.acmicpc.net/group/practice/create/{GROUP_ID}')
    driver.implicitly_wait(time_to_wait=5)
    
    driver.find_element(By.NAME, 'contest_title').send_keys(title)
    # time.sleep(3)

    start_box = driver.find_element(By.NAME, 'contest_start')
    start_box.clear()
    start_box.send_keys(today.strftime("%Y-%m-%d") + " " + start_time)
    # time.sleep(3)
    tomorrow = today + datetime.timedelta(days=1)
    end_box = driver.find_element(By.NAME, 'contest_end')
    end_box.clear()
    end_box.send_keys(tomorrow.strftime("%Y-%m-%d") + " " + start_time)
    # time.sleep(3)
    
    freeze = driver.find_element(By.NAME, 'contest_freeze')
    freeze.clear()
    freeze.send_keys('0')
    # time.sleep(3)
    print('filled setting')

    add_box = driver.find_element(By.ID, 'problem-search')
    for level in problems:
        for problem in problems[level]:
            add_box.send_keys(problem.problem_id)
            add_box.send_keys(Keys.RETURN)
            driver.implicitly_wait(time_to_wait=2)
            # time.sleep(3)
    
    print('added problems')
    driver.find_element(By.ID, 'save_button').click()

    return True

# if __name__ == '__main__':
#     class Problem:
#         def __init__(self, problem_id, title, level):
#             self.problem_id = str(problem_id)
#             self.title = title
#             self.level = str(level)
#             self.img_src = str(level) + '.svg'
#             self.alt_level = 'BSGP'[(level-1) // 5] + str(5 - level % 5)
#             self.url = 'https://www.acmicpc.net/problem/' + str(problem_id)
        
#         def __str__(self):
#             return f'{self.level} {self.problem_id} {self.title}'
        
#         def __repr__(self):
#             return str(self)
        
#     tmp = {
#         'Bronze':[Problem(24264, 'asdf', 1), Problem(25593, 'asdf', 1), Problem(25965, 'asdf', 1)],
#         'Silver':[Problem(3231, 'asdf', 1), Problem(14426, 'asdf', 1), Problem(10819, 'asdf', 1)],
#         'Gold':[Problem(15712, 'asdf', 1), Problem(23318, 'asdf', 1), Problem(29894, 'asdf', 1)],
#         'Platinum':[Problem(28452, 'asdf', 1), Problem(9334, 'asdf', 1), Problem(1603, 'asdf', 1)]
#     }
#     for i in range(5):
#         now = datetime.datetime.now() + datetime.timedelta(days=i)
#         make_practice(now.strftime("%m/%d") + 'test', now, tmp)