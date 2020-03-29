from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time

url = "https://kkutu.co.kr/"

f = open("driverpath.txt","r")
driverPath = f.readline()
print("driverPath")
print(driverPath)

def errorMsg(e):
    print(str(e))
    print("Please copy this error and comment on GitHub.")

def updateDb() :
    f = open("db.txt", 'r')
    n_l = open("no_list.txt",'r')
    no_list = []
    db = {}
    while True:
        no = n_l.readline()
        if not no: break
        no_list.append(no)

    n_l.close()
    i = 0
    while True:
        line = f.readline()
        line=line.split(' ')[0]
        if not line: break

        if len(line) <= 1:
            continue

        if not(line[0] in db.keys()):
            db.update({line[0] : [line]})
        else :
            if not ("(어인정)" in line or "{끄투 코리아}" in line):
                if not line in no_list:
                    line = line.replace(" ","")
                    line = line.replace("\n", "")
                    line = line.strip()
                    db[line[0]].append(line)
                    print(line)
    f.close()
    return db

def login(driver):
    # login button : .account-nick
    loginBtn = driver.find_element_by_class_name('account-nick')
    print(loginBtn)
    loginBtn.click()
    print("Please complete the login")
    html = ""
    while True:
        ready = input("input 'ready' when your login is done\n >>>>>>>>>>>>")
        if (ready == "ready"):
            html = driver.page_source
            break
    soup = BeautifulSoup(html, 'html.parser')
    user_info = soup.find("span", id="profile").getText()
    print(user_info)
    user_info = json.loads(user_info)
    return user_info

db = updateDb()

try :
    driver = webdriver.Chrome()
    driver.get(url)
except Exception as e:
    driver = webdriver.Chrome(driverPath)
    driver.get(url)

user_info = login(driver)  # data type json
print("join your room")
# user_profiles : game-body
while True:
    lastWordTemp = ""
    menu = input("input 'ready' when game is start\n >>>>>>>>>>>> ")

    if menu == 'ready':  # if game is started
        isGaming = driver.find_element_by_css_selector("#GameBox").value_of_css_property('display')
        print(isGaming)
        history = []
        while isGaming == "block":  # game progress checking
            isGaming = driver.find_element_by_css_selector("#GameBox").value_of_css_property('display')
            if (isGaming != "block"):
                break
            player_list = driver.find_elements_by_css_selector(".game-body>div")
            for p_l in player_list:
                # id : game-user-142191361 : class : game-user game-user-current
                player_attribute_dict = {'class': p_l.get_attribute("class"), 'id': p_l.get_attribute("id")}
                if 'game-user-bomb' in player_attribute_dict['class']:
                    history = []

                if 'game-user-current' in player_attribute_dict['class']:
                    if player_attribute_dict['id'].split('-')[2] == user_info['id']:  # player turn
                        lastWord = driver.find_element_by_css_selector('.jjo-display.ellipse').text  # load last word
                        print('lastword is : ' + lastWord)
                        if not('(' in lastWord):
                            lastWord = lastWord[-1]

                        readHistory = []

                        try:
                            readHistory = driver.find_elements_by_css_selector('.history>div')
                            tmp = []
                            for h in readHistory:
                                tmp.append(h.text)
                            readHistory = tmp
                            history.extend(readHistory)
                        except AttributeError as e:
                            history = []
                            errorMsg(e)
                        # print("------- history -------")
                        # print(history)

                        overlap = False
                        input_word = ""
                        if '(' in lastWord:
                            str = lastWord
                            str = str.split('(')
                            tmp = 0
                            try :
                                for s in str:
                                    s = s.replace(')', '')
                                    if not (s in db.keys()):
                                        print("there is no word in db start with " + s)
                                    else:
                                        i = 0
                                        while True:  # searching word
                                            if i >= len(db[s]) and tmp != 0:
                                                input_word = "GG"
                                                break
                                            if db[s][i] in history:
                                                i += 1
                                            else:
                                                input_word = db[s][i]
                                                print(db[s][i])
                                                break
                                    tmp += 1
                            except e as e:
                                errorMsg(e)
                                continue

                        else :
                            try:
                                if not (lastWord in db.keys()):
                                    print("there is no word in db start with " + lastWord)
                                else:
                                    i = 0
                                    while True:  # searching word
                                        if i > len(db[lastWord]):
                                            input_word = "GG"
                                            break
                                        if db[lastWord][i] in history:
                                            i += 1
                                        else:
                                            print(db[lastWord][i])
                                            input_word = db[lastWord][i]
                                            break
                            except e as e:
                                errorMsg(e)
                                continue

                        lastWordTemp = lastWord
                        input_box = driver.find_element_by_css_selector('.product-body>input')
                        input_box.send_keys(input_word)
                        chat_btn = driver.find_element_by_css_selector('#ChatBtn')
                        chat_btn.click()
                        history.append(input_word)
            time.sleep(0.5)
