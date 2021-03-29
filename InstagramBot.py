from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import PySimpleGUI as sg

class Instagram:
    def __init__(self):
        sg.theme('Reddit')
        #Layout
        layout = [
            [sg.Text('Usuario'), sg.Input(key='user')],
            [sg.Text('Senha'), sg.Input(key='password',password_char='•')],
            [sg.Text('Hashtag'), sg.Input(key='hashtag')],
            [sg.Button('Enviar')]
        ]
        #Janela
        self.janela = sg.Window("Robo Instagram").layout(layout)
        #Extracao
        self.button, self.valores = self.janela.Read()
        self.user = self.valores['user']
        self.password = self.valores['password']
        self.hashtag = self.valores['hashtag']

        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver')
        print(self.valores)

    def login(self):
        user = self.user
        password = self.password
        hashtag = self.hashtag
        driver = self.driver
        self.driver.get('https://www.instagram.com/')
        time.sleep(4)
        #Abre a pagina do instagram
        loginUser = self.driver.find_element_by_xpath("//input[@name='username']") 
        time.sleep(1); loginUser.click()
        loginUser.send_keys(user)
        #Clica na caixa de login "usuario", e insere o usuario (self.user)
        passUser = self.driver.find_element_by_xpath("//input[@name='password']")
        passUser.click(); time.sleep(1)
        passUser.send_keys(password)
        #Clica na caixa de login "senha", e insere a senha (self.password)
        login = self.driver.find_element_by_xpath("//button[@type='submit']")
        time.sleep(1); login.click();time.sleep(4)
        #clica no botao entrar para efetuar o login
        self.likeFollow(hashtag)

    def likeFollow(self, hashtag):
        driver = self.driver
        driver.get('https://www.instagram.com/explore/tags/' + hashtag.replace(" ", "") + '/')
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        hrefs = driver.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        [href for href in pic_hrefs if hashtag in href]
        print(hashtag + 'fotos' + str(len(pic_hrefs)))
        contador = 0
        for pic_href in pic_hrefs:
            
            driver.get(pic_href)
            
            liked = driver.find_element_by_css_selector("[aria-label=Curtir]")
            follow = driver.find_element_by_xpath("//button[@class='sqdOP yWX7d    y3zKF     ']")
            follow.click(); time.sleep(3);liked.click(); time.sleep(20)
            
            driver.execute_script("window.scrollTo(0, 300);")
            contador += 1

            if contador == 300:
                popup = sg.popup_ok_cancel("Limite de 300 curtidas atingidas, se continuar estará sujeito a ser silenciado pelo instagram\n\nClique OK para continuar curtindo" ) 
                if popup == sg.METER_REASON_CANCELLED:
                    break
                else:
                    continue
            else:
                continue
        

bot = Instagram()
bot.login()
bot.likeFollow()
