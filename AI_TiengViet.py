import os
import playsound
import speech_recognition as sr
import time 
# import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
import random
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
from time import process_time_ns, strftime
# from gtts import gTTS
from youtube_search import YoutubeSearch
import pyttsx3
import subprocess
import mysql.connector
import random
from tkinter import *
import tkinter as tk
from unidecode import unidecode
from threading import Thread
import threading
from ProcessingInput import response, response_tag
#from GUI import Record
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="tro_li_ao"
)
wikipedia.set_lang('vi')
language = 'vi'
#path = ChromeDriverManager().install()
def unicode(text):
    word = unidecode(text)
    words = word.lower()
    return words
def subspace(text):
    return re.sub("\s+","",text)   
def Assist_GUI(Gui,text):
    frame= Frame(Gui)
    Scroll = tk.Scrollbar(frame)
    assistant_text = tk.Text(frame, height=8, width=30,bd=0,bg='white',font=("Courier", 13 ,"bold"),wrap = WORD)
    Scroll.pack(side=tk.RIGHT, fill=tk.Y)
    assistant_text.pack(side=tk.LEFT, fill=tk.Y)
    Scroll.config(command=assistant_text.yview,bd=0)
    assistant_text.config(yscrollcommand=Scroll.set)
    assistant_text.insert(tk.END, text)
    frame.place(x=160,y=250)         
def speak(Gui,text):
    Assist_GUI(Gui,text)
    print("Trợ lí ảo : "+text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume - 0.0 ) # tu 0.0 -> 1.0
    engine.setProperty('rate', rate - 70)
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    # engine.stop()
    # tts =gTTS(text=text,lang=language,slow=False)
    # n = str(random.randint(1,100000))+"bot.mp3"
    # tts.save(n)
    # playsound.playsound(n,True)
    # time.sleep(2)
    # os.remove(n)
def mail(Gui,user,passmail,user_sent,content):
    mail = smtplib.SMTP("smtp.gmail.com" ,587)
    mail.ehlo()
    mail.starttls()
    mail.login(user,passmail)
    mail.sendmail(user,user_sent,str(content).encode("utf-8"))
    mail.close()
    speak(Gui,"Email đã được gửi đi")   

def get_audio(Gui):
    
    ear_robot = sr.Recognizer()
    with sr.Microphone() as mic:
        #audio = ear_robot.adjust_for_ambient_noise(mic,duration=5)
        print("\nTrợ lí ảo đang lắng nghe ...")
        audio = ear_robot.listen(mic,phrase_time_limit= 5)
        try :
            text = ear_robot.recognize_google(audio,language= "vi-VN")
            user_text = Text(Gui,height=2, width=40,bd=0,font=("Courier", 13 ,"bold"))
            user_text.insert(tk.END,text)
            user_text.place(x=160,y=200)
            print("\nNgười dùng : "+text)
            return text
        except:
            #print("Trợ lí ảo : Vui lòng nói lại tôi không thể nghe")
            return 0
def stop(Gui):
    speak(Gui,"Hẹn gặp lại bạn sau nhé ! Tạm biệt ...")  
def get_textout(Gui):
    texT = get_audio(Gui)
    if texT:
       text = response_tag(texT)
       if text:
          return [text.lower(),response(texT)]
       if text==None:
          return texT.lower()    
    else :
        speak(Gui,'Vui lòng nói lại tôi không thể nghe')        
def get_text(Gui):
    for i in range(3):
        text = get_audio(Gui)
        if text:
            return text.lower()
        elif i<2:
            speak(Gui,"Vui lòng nói lại tôi không thể nghe")
    time.sleep(2)
    stop()
    return 0   
def get_mailadress(Gui):
    voice = get_text(Gui)
    uni = unicode(voice)
    subuser = subspace(uni)
    mail_adress =subuser+"@gmail.com"     
    return mail_adress    
def hello(Gui):
    hour = int(strftime('%H'))
    if 0<= hour < 11 :
        speak(Gui,f'Chào bạn. Chúc bạn có một buổi sáng tốt lành !')
    elif 11<= hour < 13 :
        speak(Gui,f'Chào bạn . Chúc bạn có một buổi trưa thật vui vẻ !')  
    elif 13<= hour < 17 :
        speak(Gui,f'Chào bạn . Chúc bạn có một buổi chiều vui vẻ !')  
    elif 17<= hour <21 :
        speak(Gui,f'Chào bạn . Chúc bạn có một buổi tối vui vẻ !')    
    elif 21<= hour <=23 :   
        speak(Gui,f'Chào bạn . Khuya thế ! Bạn nên đi ngủ sớm đi nhé !')
    else :
        speak(Gui,"Hệ lỗi đang lỗi ! Vui lòng kiểm tra lại ")  
def get_time(Gui,text) :
    now = datetime.datetime.now()
    if 'hour' in text :
        speak(Gui,f'Bây giờ là {now.hour} giờ {now.minute} phút {now.second} giây')
    elif 'day' in text :
        speak(Gui,f'Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}')
    else :
        speak(Gui,"Xin lỗi , tôi vẫn chưa hiểu ý của bạn")          
def open_application(Gui,text):
    if "google" in text:
        speak(Gui,"Mở Google Chrome")
        os.startfile(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        #webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("http://google.com")
    elif "cốc cốc" in text:
        speak(Gui,"Mở Cốc Cốc")   
        os.startfile(r"C:\Program Files (x86)\CocCoc\Browser\Application\browser.exe") 
    elif "casio" in text:
        speak(Gui,"Mở máy tính Casio")    
        subprocess.Popen("D:\\Casio fx-570VN PLUS\\Casio fx570vn plus.exe")
    else :
        speak(Gui,"Ứng dụng chưa cài đặt . Vui lòng cài đặt vào hệ thống")    
def open_website(Gui,text):
    reg_ex = re.search('mở (.+)' ,text)
    if reg_ex :
        domain = reg_ex.group(1)
        url = "https://www."+domain
        print(url)
        webbrowser.open(url)
        speak(Gui,f"Đã mở trang web {text}")
        return True
    else:  
        speak(Gui,f"Không tìm thấy trang web {text}")
        return False     
def search_google(Gui,text):
    inform = text.split("kiếm",1)
    url = f"https://www.google.com/search?q={inform[1]}"
    webbrowser.open(url)
    speak(Gui,"Thông tin đã được tìm kiếm trên Google")
def search_google2(Gui):
    speak(Gui,"Vui lòng cho biết điều bạn muốn tìm kiếm")
    inform = get_text(Gui)
    url = f"https://www.google.com/search?q={inform}"
    webbrowser.open(url)
    speak(Gui,"Thông tin đã được tìm kiếm trên Google")
def send_email(Gui):
    speak(Gui,"Tôi đang thực hiện kiểm tra dữ liệu ?")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT user, pass FROM user_gmail")
    myresult = mycursor.fetchall()
    if len(myresult)>0 :
        speak(Gui,f"Vui lòng chọn các tài khoản sau")  
        for user in myresult:
           
          
           speak(Gui,user[0])
        dieukien = True
        while dieukien : 
          
          mail_adress = get_mailadress(Gui)  
          print(mail_adress)
          for user in myresult:
            if mail_adress == user[0]:
               speak(Gui,"Vui lòng cho biết địa chỉ cần gửi")
               mail_sent = get_mailadress(Gui)
               print(mail_sent)
               speak(Gui,"Vui lòng cho biết nội dung cần gửi")
               content = get_text(Gui)
               mail(Gui,mail_adress,"01665574505a",mail_sent,content)
               dieukien = False
               break
          if dieukien:
              speak(Gui,"Vui lòng chọn lại tên người dùng cho chính xác")    
    else :
        speak(Gui,"Chưa có dữ liệu vui lòng cung cấp tài khoản và mật khẩu") 
def current_weather(Gui):
    speak(Gui," Bạn muốn xem thời tiết ở đâu nhỉ ?")
    city = get_text(Gui)
    ow_url = "https://api.openweathermap.org/data/2.5/weather?"
    if not city:
        pass
    api_key = "8f5bac908d0f7a4fee99b45ca5e820d4"    
    call_url = ow_url+"q="+city+"&appid="+api_key+"&lang=vi"+"&units=metric"
    res = requests.get(call_url)
    data = res.json()
    if data["cod"] == 200:
       weather = data['weather']
       weather_descrip = weather[0]['description']
       weather_city = data['name']
       main = data['main']
       weather_temperature = round(main['temp'])
       weather_humidity = round(main['humidity'])
       wind = data['wind']
       wind_speed = wind['speed']
       content = f"Hôm nay {weather_city} có {weather_descrip}, nhiệt độ là {weather_temperature} độ C , độ ẩm là {weather_humidity} phần trăm , tốc độ gió là {wind_speed} mét trên giây"
       speak(Gui,content)
    else:
       speak(Gui,"Dữ liệu chưa được tìm thấy vui lòng kiểm tra lại địa chỉ cần tìm !")    
def search_youtobe1(Gui):
    speak(Gui,"Vui lòng cho biết nội dung bạn muốn tìm kiếm")
    search = get_text(Gui)
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak(Gui,"Đây là nội dung tôi đã tìm kiếm được")
def search_youtobe2(Gui):
    speak(Gui,"Vui lòng cho biết nội dung bạn muốn tìm kiếm")
    search = get_text(Gui)
    result = YoutubeSearch(search,max_results=10).to_dict()
    link = result[0]['url_suffix']
    url = f"https://www.youtube.com{link}"    
    webbrowser.get().open(url)    
def change_wallpaper(Gui) :
    api_key = "sk4fvPX2uYY-M0rIgiPwG3cGjt_9jm8Jv16T3pENUKg"   
    url = f'https://api.unsplash.com/photos/random?client_id={api_key}'
    response = urllib2.urlopen(url)
    json_string = response.read()
    response.close()
    parse_json = json.loads(json_string)
    photo = parse_json['urls']['full']
    urllib2.urlretrieve(photo,r"E:\Troliao\image_change.png")
    image = os.path.join(r"E:\Troliao\image_change.png")
    ctypes.windll.user32.SystemParametersInfoW(20,0,image,3)
    speak(Gui,"Tôi đã thực hiện thay đổi hình nền")
def search_wiki(Gui):
    try:
        speak(Gui,"Hãy nói cho tôi biết bạn muốn tìm gì ?")
        text = get_text(Gui)
        contents = wikipedia.summary(text).split('\n')
        speak(Gui,contents[0])
        dem = 0
        for content in contents[1:]:
            if dem < 2:
                speak(Gui,"Bạn có muốn biết thêm không ???")
                ans = get_text(Gui)
                if 'có' not in ans:
                    break
            dem += 1
            speak(Gui,content)
        speak(Gui,"Đây là nội dung tôi vừa tìm được cảm ơn bạn đã lắng nghe")  
    except: 
        speak(Gui,"Nội dung của bạn không được tìm kiếm trong wiki ")   
def sing_song(Gui):
     speak(Gui,"Hãy nghe tôi hát")
     rd = random.randint(1,4)
     print(rd)
     playsound.playsound(rf"E:\Troliao\music\{rd}.mp3")     
def listen_label1(Gui):
    time.sleep(4)
    listen_label = Label(Gui,text="Trợ lí ảo đang lắng nghe .....",border=0,bg='white',font=("Courier", 13 ,"bold"))
    listen_label.place(x=150,y=445)  
    #listen_label.configure(text=text)  
def listen_label2(Gui):
    listen_label = Label(Gui,text="Trợ lí ảo ngừng hoạt động ! ",border=0,bg='white',font=("Courier", 13 ,"bold"))
    listen_label.place(x=150,y=445)                
def main_brain(Gui,Record):
        Record['state']=DISABLED
        speak(Gui,f'Tôi có thể giúp gì được cho bạn ?')
        while True:
            
            text = get_textout(Gui)
            if not text:
                listen_label2(Gui)
                Record['state']= NORMAL
                break
            elif 'greeting' in text[0]:
                hello(Gui)
                listen_label2(Gui)
                Record['state']= NORMAL
                break
            elif ('hour' in text[0]) or ('day' in text[0]):
                get_time(Gui,text[0]) 
                listen_label2(Gui)
                Record['state']= NORMAL
                break
            elif 'mở' in text:
                if '.' in text:
                    open_website(Gui,text)
                    listen_label2(Gui)
                    Record['state']= NORMAL
                    break
                else:    
                    open_application(Gui,text)  
                    listen_label2(Gui)  
                    Record['state']= NORMAL  
                    break 
            elif 'thank' in text[0]:
                speak(Gui,text[1])  
                listen_label2(Gui)   
                Record['state']= NORMAL  
                break
            elif 'mail' in text[0]:
                send_email(Gui) 
                listen_label2(Gui) 
                Record['state']= NORMAL 
                break 
            elif 'thời tiết' in text:
                current_weather(Gui)  
                listen_label2(Gui) 
                Record['state']= NORMAL
                break  
            elif 'tìm kiếm' in text :
                if "tìm kiếm" == text:
                    search_google2(Gui)  
                    listen_label2(Gui) 
                    Record['state']= NORMAL 
                    break
                else:
                    search_google(Gui,text)
                    listen_label2(Gui)
                    Record['state']= NORMAL
                    break
            elif 'youtube' in text:
                speak(Gui,"Bạn có muốn tìm kiếm nội dung nâng cao không ?")
                yesOrNo = get_text(Gui) 
                if 'có' in yesOrNo:
                    search_youtobe2(Gui)
                    listen_label2(Gui)
                    Record['state']= NORMAL
                    break
                else :
                    search_youtobe1(Gui) 
                    listen_label2(Gui) 
                    Record['state']= NORMAL 
                    break
            elif 'hình nền' in text:
                change_wallpaper(Gui)
                listen_label2(Gui) 
                Record['state']= NORMAL 
                break
            elif 'hát' in text:
                sing_song(Gui)
                listen_label2(Gui)
                Record['state']= NORMAL  
                break
            elif 'wiki' in text:
                search_wiki(Gui) 
                listen_label2(Gui) 
                Record['state']= NORMAL  
                break                
            elif 'goodbye' in text:
                speak(Gui,text[1])  
                listen_label2(Gui)
                Record['state']= NORMAL  
                break
            elif 'sad' in text:
                speak(Gui,text[1])

                listen_label2(Gui)
                Record['state']= NORMAL  
                break
            elif 'love' in text:
                speak(Gui,text[1])
                listen_label2(Gui)
                Record['state']= NORMAL  
                break
            elif 'story' in text:
                speak(Gui,text[1])
                listen_label2(Gui)
                Record['state']= NORMAL  
                break
            else:
                speak(Gui,"Chức năng chưa có . Bạn vui lòng chọn lại chức năng đã có trong menu.")
                listen_label2(Gui)
                Record['state']= NORMAL  
                break

def thread_mutiii(Gui,Record):
	t1 = threading.Thread(target=listen_label1, args=(Gui,))
	t2 = threading.Thread(target=main_brain,args=(Gui,Record,))
	t1.start()
	t2.start()
    
    
   
                  