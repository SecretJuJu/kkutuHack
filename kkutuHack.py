from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import re
import sys
import DBCont
import threading
# from selenium.webdriver.common.by import By

cont = DBCont.DBCont()

url = "https://kkutu.co.kr/"

f = open("driverpath.txt","r")
driverPath = f.readline()
print("driverPath")
print(driverPath)

def errorMsg(e):
    print(str(e))
    print("Please copy this error and comment on GitHub.")

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

def dropTable(TName): #  avoid unknown except tion so
    try:
        cont = DBCont.DBCont()
        cont.dropTable(TName=TName)
    except Exception as e:
        print("...")
    

def processingLastWord(lastword):
    result = lastword
    if "(" in result:
        result = result.split('(')
        for indexOfLW,l in enumerate(result):
            result[indexOfLW] = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》 ]', '', l)
    
    return list(result)
try :
    driver = webdriver.Chrome()
    driver.get(url)
except Exception as e:
    try :
        driver = webdriver.Chrome(driverPath)
        driver.get(url)
    except Exception as ee:
        print ('Please set the chrome driver')
        sys.exit()




user_info = login(driver)  # data type : json
print("join your room")
# user_profiles : game-body


### game start / insert words ###

while True:
    try:
        lastWordTemp = ""
        menu = input("input 'ready' when game is start\n >>>>>>>>>>>> ")
        if  "q" in menu or "exit" in menu or "quit" in menu:
            print("exit! ")
            break
            
        if menu == 'ready':  # if game is started
            isGaming = driver.find_element_by_css_selector("#GameBox").value_of_css_property('display')
            print(isGaming)
            cont.gameSet()
            last_history = ''
            while isGaming == "block":  # game progress checking

                time.sleep(0.01)
                isGaming = driver.find_element_by_css_selector("#GameBox").value_of_css_property('display')
                if (isGaming != "block"):
                    break
                player_list = driver.find_elements_by_css_selector(".game-body>div")
                time.sleep(0.1)
                try:
                    history = driver.find_element_by_css_selector(".history-holder .history .eclipese .history-item .expl-mother").text
                    print(history)
                    if ( last_history != history):
                        cont.removeRow(TName="cpWordList",where="word = '"+history+"'")
                        last_history = history
                except Exception as e:
                    print('...')
                for p_l in player_list:
                    # id : game-user-142191361 : class : game-user game-user-current
                    player_attribute_dict = {'class': p_l.get_attribute("class"), 'id': p_l.get_attribute("id")}
                    # print(player_attribute_dict)
                    if 'game-user-bomb' in player_attribute_dict['class']:
                        try:
                            print("game is done")
                            
                            time.sleep(1)
                        except Exception as e:
                            # print(e)
                            print("error at user-bomb")
                        t = threading.Thread(target=dropTable, args=('cpWordList'))
                        t.start()

                        break

                    if 'game-user-current' in player_attribute_dict['class']:
                        # .jjo-display .ellipse label

                        try :
                            lb = driver.find_element_by_css_selector(".jjo-display .ellipse label")
                            if "game-fail-text" in lb.get_attribute('class').split():
                                print("fail.. wait")
                                time.sleep(0.5)
                        except Exception as e:
                            time.sleep(0.1)

                        if player_attribute_dict['id'].split('-')[2] == user_info['id']:  # player turn
                            try:
                                lastWord = driver.find_element_by_css_selector('.jjo-display.ellipse').text  # load last word
                                lastWord = processingLastWord(lastWord)
                                print(' ------ lastword -----')
                                print (lastWord)
                                if len(lastWord) > 2:
                                    break
                                ableWord = []
                                for l in lastWord:
                                    res = cont.find("cpWordList","word","word like '"+l+"%'",1)
                                    if res != "":
                                        ableWord.append(str(res))
                                try :
                                    if(len(ableWord) < 1):
                                        print("no words..")
                                        time.sleep(1)
                                        break
                                    returnWord = ableWord[0]
                                    print ("--- returnWord ---")
                                    print(returnWord)
                                    cont.removeRow(TName="cpWordList",where="word = '"+returnWord+"'")
                                    ## enter word to input box 
                                    input_box = driver.find_element_by_css_selector('.product-body>input')
                                    input_box.send_keys(returnWord)

                                    ## submit
                                    chat_btn = driver.find_element_by_css_selector('#ChatBtn')
                                    chat_btn.click()
                                    time.sleep(1.5)
                                    break
                                except Exception as e:
                                    # print (e)
                                    print("error at updateDB and word select")
                                    time.sleep(2)
                                    break
                            except Exception as e:
                                # print(e)
                                print("error at find word")
                                break
    except Exception as e:
        # print(e)
        print("error at gaming loop")