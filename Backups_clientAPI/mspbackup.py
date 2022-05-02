import os
import time
import cv2
import pyotp
import pytesseract
import wget
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from LlocDeCopies import LlocDeCopies


class mspbackup(LlocDeCopies):
    def __init__(self, name:str, url:str, user:str, password:str, clautotp:str):
        self._clautotp = clautotp
        super().__init__(name, url, user, password)
    
    def retrieve_copies(self, ruta:str, args)-> None:
        patata = True
        if not(os.path.exists(ruta+"/tesseract")):
            os.mkdir(ruta+"/tesseract")
        else:
            pytesseract.pytesseract.tesseract_cmd =(ruta+"/tesseract/tesseract.exe")
            patata = False
        if os.path.exists("C:\Program Files\Tesseract-OCR") and patata:
            pytesseract.pytesseract.tesseract_cmd =("C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        elif not(os.path.exists(args.tesseractpath)):
            wget.download("https://github.com/NilPujolPorta/CatbackupAPI-NPP/blob/master/CatBackupAPI/tesseract-ocr-w64-setup-v5.0.0-rc1.20211030.exe?raw=true", ruta+"/tesseract-ocr-w64-setup-v5.0.0-rc1.20211030.exe")
            print()
            print("=========================================================")
            print("INSTALA EL TESSERACT EN LA CARPETA CatBackupAPI/tesseract")##revisar
            print("=========================================================")
            time.sleep(20)
            os.popen(ruta+"/tesseract-ocr-w64-setup-v5.0.0-rc1.20211030.exe")
            return
        else:
            pytesseract.pytesseract.tesseract_cmd = (args.tesseractpath)

        options = Options()
        if args.portable_chrome_path != None:
            options.binary_location = args.portable_chrome_path
        if args.graphicUI:
            #options.headless = True
            #options.add_argument('--headless')
            #options.add_argument('--disable-gpu')
            options.add_argument('window-size=1200x600')
            options.add_argument('log-level=1')#INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
        browser = webdriver.Chrome(executable_path = ruta+"/chromedriver.exe", options=options)
        lineabd = 0
        browser.get(super().get_url())

        find_user = browser.find_element(by='id', value="txtLogin")
        find_user.send_keys(super().get_user())

        find_passwd = browser.find_element(by='id', value="txtPassword")
        find_passwd.send_keys(super().get_password())

        find_login = browser.find_element(by='id', value="btnLogin")
        find_login.click()


        time.sleep(5)


        find_key = browser.find_element(by='id', value="txtSecretCode")
        totp = pyotp.TOTP(self._clautotp)
        find_key.send_keys(totp.now())

        find_login2 = browser.find_element(by='id', value="btnLogin")
        find_login2.click()

        time.sleep(20)

        #"/html/body/div[1]/form/div[3]/div[2]/div/div[1]/div[1]/div/div[1]/div/div/div/div/div[3]/section[1]/div/div[3]/span/div[1]/text()"
        browser.save_screenshot('screenshot.png')
        


        img = cv2.imread('screenshot.png')
        text = pytesseract.image_to_string(img)

        if os.path.exists("screenshot.png"):
            os.remove("screenshot.png")
        else:
            print("The file does not exist")

        x = text.find("Success: ")
        if x == -1:
            x = text.find("success: ")
        if x == -1:
            correctes = 0
        else:
            y= x+9
            x= y+2
            correctes = int(text[y:x])

        x = text.find("Failed: ")
        if x == -1:
            x = text.find("Foiled: ")
        if x == -1:
            erronis = 0
        else:
            y= x+8
            x= y+2
            erronis = int(text[y:x])

        x = text.find("Overdue: ")
        if x == -1:
            atrasats = 0
        else:
            y= x+9
            x= y+2
            atrasats = int(text[y:x])

        x = text.find("Warning: ")
        if x == -1:
            advertencies = 0
        else:
            y= x+9
            x= y+2
            advertencies = int(text[y:x])

        if args.quiet:
            print("Correctes: "+str(correctes))
            print("Erronis: "+str(erronis))
            print("Atrasats: "+str(atrasats))
            print("Advertencies: "+str(advertencies))
            print("total: "+str(correctes+erronis+atrasats+advertencies))


        Lcorrectes = []
        x = 0
        while x < correctes:
            Lcorrectes.append({"Status":"Correctes"})
            x = x+1
        Lerronis = []
        x = 0
        while x < erronis:
            Lerronis.append({"Status":"Erronis"})
            x = x+1
        Latrasats = []
        x = 0
        while x < atrasats:
            Latrasats.append({"Status":"Atrasats"})
            x = x+1
        Ladvertencies = []
        x = 0
        while x < advertencies:
            Ladvertencies.append({"Status":"Warning"})
            x = x+1