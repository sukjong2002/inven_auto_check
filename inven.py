import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from selenium import webdriver
import time, os, requests, glob
import pycryptodome
import autologin

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('인벤 자동 출첵')
        self.setGeometry(800, 200, 300, 130)
        auto = autologin
        key = '12345678901234567890123456789012'
        loc = os.path.abspath(".\\")+'\login.txt'


        self.checkBox1= QCheckBox("아이디 및 비밀번호 저장")
        self.checkBox1.stateChanged.connect(self.delete_text)

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setEchoMode(QLineEdit.Password)

        #아이디 및 비밀번호 저장 체크박스
        if auto.check(key, loc, 'getkey') == True:
            self.checkBox1.setChecked(True)
            #ID 텍스트박스
            self.lineEdit1.setText(auto.check(key, loc, 'getid'))

            #PW 텍스트박스
            self.lineEdit2.setText(auto.check(key, loc, 'getpass'))
            self.lineEdit2.setEchoMode(QLineEdit.Password)
        else:
            self.lineEdit1.setText("")
            self.lineEdit2.setText("")
            self.checkBox1.setChecked(False)

        self.statusbar = QStatusBar(self)
        self.statusbar.showMessage('대기..')

        #라벨
        self.label1 = QLabel("아이디 : ")
        self.label2 = QLabel("패스워드 : ")

        #Login 버튼
        self.pushButton1= QPushButton("로그인")
        self.pushButton1.clicked.connect(self.btn_login)

        #Quit 버튼
        self.pushButton2= QPushButton("종료")
        self.pushButton2.clicked.connect(QCoreApplication.instance().quit)

        layout = QGridLayout()

        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.lineEdit2, 1, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        layout.addWidget(self.pushButton2, 1, 2)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.checkBox1, 2, 0, 2, 3)
        layout.addWidget(self.statusbar, 3, 0, 3, 3)

        self.setLayout(layout)



    def create_text(self, userid, password):
        save = 'true'
        pi = pycryptodome
        key = '12345678901234567890123456789012'
        encid = pi.AESCipher(key).encrypt(userid)
        encpass = pi.AESCipher(key).encrypt(password)
        encsave = pi.AESCipher(key).encrypt(save)

        if  self.checkBox1.isChecked() == True:
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

    def btn_login(self):
        start_time = time.time()
        userid = self.lineEdit1.text()
        password = self.lineEdit2.text()
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
        self.statusbar.showMessage('아이디 입력..')

        #패스워드 입력
        driv.find_element_by_name('password').send_keys(password)
        self.statusbar.showMessage('비밀번호 입력..')

        #로그인 버튼 클릭
        driv.find_element_by_xpath('//*[@id="loginBtn"]').click()
        self.statusbar.showMessage('로그인 버튼 클릭..')
        time.sleep(3)

        #로그인 실패 조건
        if(driv.current_url == url):
            driv.service.stop()
            print('stop chrome')
            self.statusbar.showMessage('로그인 실패..')
            self.statusbar.showMessage('(아이디와 비밀번호를 확인해주세요)대기..')
            print("--- %s seconds ---" %(time.time() - start_time))

        #정상 로그인 이후 동작
        else:
            self.statusbar.showMessage('로그인 성공..')
            driv.get('http://imart.inven.co.kr/attendance/')
            self.statusbar.showMessage('아이마트 이동..')
            driv.find_element_by_xpath('//*[@id="invenAttendCheck"]/div/div[2]/div/div[3]/div[1]/div[4]/a').click()
            self.statusbar.showMessage('출석 체크 버튼 클릭..')
            time.sleep(1)
            #driv.close()
            driv.service.stop()
            self.statusbar.showMessage('(출석 체크 완료)대기..')

            print("--- %s seconds ---" %(time.time() - start_time))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
