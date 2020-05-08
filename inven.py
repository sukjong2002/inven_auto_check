import sys
from selenium import webdriver
import time, os, requests, glob
import pycryptodome
import autologin
from getpass import getpass
from datetime import datetime

class MyWindow():
    def __init__(self):
        super().__init__()
        self.set_credential()

    def create_text(self, userid, password):
        save = 'true'
        pi = pycryptodome
        key = '12345678901234567890123456789012'
        encid = pi.AESCipher(key).encrypt(userid)
        encpass = pi.AESCipher(key).encrypt(password)
        encsave = pi.AESCipher(key).encrypt(save)

        if not os.path.isfile(os.path.abspath(".\\")+'\login.txt'):
            f = open('login.txt', 'wb')
            f.write(encid.encode())
            f.write('\n'.encode())
            f.write(encpass.encode())
            f.write('\n'.encode())
            f.write(encsave.encode())
            f.close()
        elif os.path.isfile(os.path.abspath(".\\")+'\login.txt'):
            self.delete_text
            f = open('login.txt', 'wb')
            f.write(encid.encode())
            f.write('\n'.encode())
            f.write(encpass.encode())
            f.write('\n'.encode())
            f.write(encsave.encode())
            f.close()

    def delete_text(self):
        if self.checkBox1.isChecked() == False:
            for root, dir, files in os.walk(os.getcwd()):
                for f in files:
                    a = os.path.splitext(f)[-1]
                    if a == '.txt':
                        os.remove(f)

    def btn_login(self, userid, password):
        start_time = time.time()
        self.create_text(userid, password)

        #크롬 옵션(gpu 사용 x, 창 없음)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')


        driv = webdriver.Chrome('./ChromeDriver.exe', chrome_options=options)

        url = 'https://member.inven.co.kr/user/scorpio/mlogin'
        driv.implicitly_wait(3)
        driv.get(url)


        #아이디 입력
        driv.find_element_by_name('user_id').send_keys(userid)
        print('아이디 입력..')

        #패스워드 입력
        driv.find_element_by_name('password').send_keys(password)
        print('비밀번호 입력..')

        #로그인 버튼 클릭
        driv.find_element_by_xpath('//*[@id="loginBtn"]').click()
        print('로그인 버튼 클릭..')
        if len(driv.find_elements_by_id('btn-securitypw')) > 0:     #비밀번호 변경 창이 있는지 확인
            driv.find_element_by_xpath('//*[@id="btn-extend"]').click()           #다음에 변경 클릭
        time.sleep(3)

        #로그인 실패 조건
        if(driv.current_url == url):
            driv.service.stop()
            print('stop chrome')
            print('로그인 실패..')
            print('(아이디와 비밀번호를 확인해주세요)대기..')
            print("--- %s seconds ---" %(time.time() - start_time))
            os.remove(os.path.abspath(".\\")+'\login.txt')
            self.set_credential()

        #정상 로그인 이후 동작
        else:
            print('로그인 성공..')
            driv.get('http://imart.inven.co.kr/attendance/')
            print('아이마트 이동..')
            driv.find_element_by_xpath('//*[@id="invenAttendCheck"]/div/div[2]/div/div[3]/div[1]/div[4]/a').click()
            print('출석 체크 버튼 클릭..')
            time.sleep(1)
            #driv.close()
            driv.service.stop()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' (출석 체크 완료)대기..')

            print("--- %s seconds ---" %(time.time() - start_time))


    
    def set_credential(self):
        auto = autologin
        key = '12345678901234567890123456789012'
        loc = os.path.abspath(".\\")+'\login.txt'
        userid = ''
        password = ''
        if auto.check(key, loc, 'getkey') == True:
            userid = auto.check(key, loc, 'getid')
            password = auto.check(key, loc, 'getpass')
        else:
            userid = input("ID입력: ")
            password = getpass("PW입력: ")
        self.btn_login(userid, password)
            
if __name__ == "__main__":
    while True:
        mywindow = MyWindow()
        time.sleep(60*60*24)
