import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import subprocess
import urllib.request
import sys
import importlib
def install_pip():
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_script = "get-pip.py"
    try:
        print("Скачивание get-pip.py...")
        urllib.request.urlretrieve(get_pip_url, get_pip_script)
        print("Скрипт get-pip.py успешно скачан.")
        print("Установка pip...")
        subprocess.check_call([sys.executable, get_pip_script])
        print("pip успешно установлен.")
        if os.path.exists(get_pip_script):
            os.remove(get_pip_script)
            print("Скрипт get-pip.py удален.")
    except Exception as e:
        print(f"Ошибка при установке pip: {e}")
        exit(1)
def check_pip():
    try:
        import pip
        print("pip уже установлен.")
    except:
        print("pip не установлен.")
        install_pip()
check_pip()
try:subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
except: None

if not os.path.exists("config.txt"):
    with open("config.txt", 'w', encoding='utf-8') as file:
        file.write("last_name:None\noffline_recognition_install:False")
def check_internet_connection():
    url = "http://www.google.com"
    timeout = 2
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            #print("Подключение к интернету установлено")
            return True
    except requests.ConnectionError:
        print("Нет подключения к интернету")
        return False
def update_config():
    global last_name, offline_recognition_install
    config = []
    with open('config.txt', 'r', encoding='utf-8') as file:
        for line in (file):
            config.append(line)
        for i in range(len(config)):
            config[i] = config[i].split(sep="\n")[0]
        print(config)
        last_name = config[0].split(sep=":")[1]
        offline_recognition_install = config[1].split(sep=":")[1]
        print(last_name, offline_recognition_install)
    return
update_config()
def install(package):
    try:
        print(f"Установка, {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Установлен, {package}")
    except: exit(1)
    return
import zipfile
def model_install():
    if check_internet_connection()==True:
        model_dir = "vosk-model"
        print("Модель не найдена. Начинаю загрузку...")
        model_url = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
        model_zip = "model.zip"
        urllib.request.urlretrieve(model_url, model_zip)
        print("Модель скачана. Распаковка...")
        with zipfile.ZipFile(model_zip, "r") as zip_ref:
            zip_ref.extractall(model_dir)
        os.remove(model_zip)
        print("Модель готова к использованию.")
    return
def active_vosk():
    global vosk
    try:
        import vosk
        print("Vosk импортирован")
    except:
        if check_internet_connection() == True:
            install("vosk")
    if offline_recognition_install == "False":
        model_install()
        with open("config.txt", 'w', encoding='utf-8') as file:
            file.write(f"last_name:{last_name}\noffline_recognition_install:True")
        update_config()
    else:
        print("Модель уже установлена")
    return

import re
import random
import time
from threading import Thread
from tkinter import *
from tkinter import ttk, Checkbutton, IntVar, StringVar
from tkinter.messagebox import showerror, showwarning, showinfo
import json
from datetime import date
try:
    import requests
except:
    install("requests")
    import site
    importlib.reload(site)
    import requests
try:
    import websocket
except:
    install("websocket")
    import websocket
try:
    import urllib3
except:
    install("urllib3")
    import urllib3
try:
    import numpy
except:
    install("numpy")
    import numpy
try:
    import sounddevice as sd
except:
    install("sounddevice")
    import sounddevice as sd
try:
    import speech_recognition as sr
except:
    install("SpeechRecognition")
    import speech_recognition as sr
try:
    from PIL import ImageTk, Image
except:
    install("Pillow")
    from PIL import ImageTk, Image
import base64
refresh_token = '1//0cgK_buCBgecvCgYIARAAGAwSNwF-L9IrB1ExKyYhM167qKdJo94ObQ9ZBmbdrIQz9-FhrK0s143jZooNvTpZtCm_E5Q7rZUWCq8'
client_id = base64.b64decode("ODI0MTQxNTk1ODk1LWpxb2pydDRtOG9icDM2MGh0cjY2c21wZTNsNG9zZzVqLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29t").decode()
client_secret = base64.b64decode("R09DU1BYLVJTVGJWQjJrZ1JucTJ3Y2pmVjYxeXFsSzZSVkY=").decode()
def token():
    global access_token
    r = requests.post(
        'https://www.googleapis.com/oauth2/v4/token',
        headers={'content-type': 'application/x-www-form-urlencoded'},
        data={
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }
    )
    tokens = r.json()
    access_token = tokens.get('access_token')
    #print(access_token)
    return
def images_in_google():
    token()
    file_id=["1hSk23XqvAG2NwLDKnBbbhuxCjYHt-3l_","10HooU78BxDd9tR2VmdlVFlYVwAb79xbL","12WjFnnPL51TSVJ5ZOr9QYpt8FI0Bx2eE"]
    file_names=["task1.png","task2.png","task3.png"]
    headers = {"Authorization": "Bearer " + access_token}
    for i in range(len(file_id)):
        url = f"https://www.googleapis.com/drive/v3/files/{file_id[i]}?alt=media"
        file_name = file_names[i]
        print(url)
        print(file_name)
        response = requests.get(url, headers=headers, stream=True)
        with open("images/"+file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    return
def check_images():
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Папка images создана")
        images_in_google()
    return
check_images()
global root, title
root = Tk()
running = False
start_time = 0
elapsed_time = 0


def update_clock():
    global elapsed_time, start_time, title, minutes, seconds
    title.config(text='00:00')
    if running:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        title.config(text=f"{minutes:02}:{seconds:02}")
        root.after(10, update_clock)
def  start():
    global running, start_time, elapsed_time
    if not running:
        start_time = time.time() - elapsed_time
        running = True
        update_clock()
def stop():
    global running
    if running:
        running = False

def task1():
    global Answer
    Primer1 = []
    Answer1 = []
    Primer2 = []
    Answer2 = []
    Primer3 = []
    Answer3 = []
    Answer = []
    a=1
    for i in range(3):
        for i in range(16):
            Number1 = random.randint(0, 18)
            Number2 = random.randint(0, 18)
            Operators = ['+', '-', '*']
            Operators_number = random.randint(0, 2)
            Operator = Operators[Operators_number]
            while Number1 > 10 or Number2 > 10 and Operator == '*':
                Number1 = random.randint(0, 18)
                Number2 = random.randint(0, 18)
            while Number1 < Number2 and Operator == '-':
                Number1 = random.randint(0, 18)
                Number2 = random.randint(0, 18)
            PrZ = f'{Number1} {Operator} {Number2} ='
            if Operator == '+':
                answer = (int(Number1) + int(Number2))
            elif Operator == '-':
                answer = (int(Number1) - int(Number2))
            else:
                answer = (int(Number1) * int(Number2))
            if a == 1:
                Primer1.append(PrZ)
                Answer1.append(answer)
            if a == 2:
                Primer2.append(PrZ)
                Answer2.append(answer)
            if a == 3:
                Primer3.append(PrZ)
                Answer3.append(answer)
        if a == 1:
            Primer1 = str('\n'.join(Primer1))
        if a == 2:
            Primer2 = str('\n'.join(Primer2))
        if a == 3:
            Primer3 = str('\n'.join(Primer3))
        a=a+1
    Answer.append(Answer1)
    Answer.append(Answer2)
    Answer.append(Answer3)
    Answer = str(Answer).replace('[', '')
    Answer = Answer.replace(']', '')
    Answer = Answer.replace(',', '')
    Answer = Answer.split()
    Answer = ', '.join(Answer)
    Answer = Answer.split(', ')
    print(Answer)
    def task():
        global title
        root.title('Задание 1')
        root.geometry('800x600')

        frame1 = Frame(root, bg='white')
        frame1.place(relwidth=0.33, relheight=1)
        title1 = Label(frame1, bg='white')
        title1.configure(text=Primer1, font=("Arial", 16), justify="right")
        title1.pack(fill="both")

        frame2 = Frame(root, bg='white')
        frame2.place(relwidth=0.33, relheight=1, relx=0.33)
        title2 = Label(frame2, bg='white')
        title2.configure(text=Primer2, font=("Arial", 16), justify="right")
        title2.pack(fill="both")

        frame3 = Frame(root, bg='white')
        frame3.place(relwidth=0.34, relheight=1, relx=0.66)
        title3 = Label(frame3, bg='white')
        title3.configure(text=Primer3, font=("Arial", 16), justify="right")
        title3.pack(fill="both")

        frame4 = Frame(root, bg='white')
        frame4.place(relwidth=0.33, relx=0.33, rely=0.9, relheight=0.1)
        title = Label(frame4, bg='white')
        title.configure(text='00:00', font=("Arial", 16))
        title.pack(fill="both")
        def resize_text(event):
            height = event.height
            new_font_size = int(height / 32)
            # print('new_font_size: ', new_font_size)
            title1.config(font=("Arial", new_font_size))
            title2.config(font=("Arial", new_font_size))
            title3.config(font=("Arial", new_font_size))
            title.config(font=("Arial", new_font_size))
        root.bind('<Configure>', resize_text)
        start()
        recognition(task=1)

    def manual():
        root.title('Инструкция')
        root.geometry('900x700')
        root.minsize(900, 700)
        frame = Frame(root, bg='white')
        frame.place(relwidth=1, relheight=1)
        label1=Label(root,text="Задание 1. Решение простых примеров", bg="white", font=("Arial", 24))
        label1.place(relwidth=1, relheight=0.08)

        image = Image.open("images/task1.png")
        new_width = 320
        new_height = 220
        resized_image = image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(resized_image)
        label2 = Label(root, image=photo, bg="white")
        label2.image = photo
        label2.place(relx=0.05, rely=0.2)
        def update_message_width(event):
            if event.width>100:
                label3.config(width=event.width - 400)
        label3=Message(root, width=400, bg="white",anchor=W, font=("Arial", 14), text="При решении примеров на время работает зрительная кора, отвечающая за обработку визуальной информации, нижняя височная извилина, отвечающая за хранение в памяти значения цифр, область Вернике, отвечающая за понимание смысла слов, угловая извилина, ответственная за вычисления, а также префронтальная кора головного мозга, отвечающая за наиболее сложные функции.\n  Упражнения, которые входят в данное задание, — это задания на сложение, умножение и вычитание двух чисел. Такие вычисления сами по себе несложные, но поначалу могут занять некоторое время у человека, не привыкшего считать в уме. Даже низкая скорость выполнения заданий не препятствует тренировке мозга.\n    Важно решать упражнения ежедневно. Идеально, если занятия проходят в первой половине дня, когда активность мозга максимальна. Упражнения нужно выполнять после приема пищи. Постарайтесь по возможности выполнять задания в одно и то же время, так улучшение работы мозга будет более очевидно.\n  При выполнении задания следует вслух произносить только ответ. Читать само упражнение, в том числе и в уме, не надо. С каждым новым выполнением старайтесь превзойти свой предыдущий результат.\n   Количество правильных ответов на упражнения равняется количеству баллов.")
        label3.place(x=320, relx=0.05, rely=0.1)
        root.bind("<Configure>", update_message_width)
        task_create = Button(root, text="Старт", font=("Arial", 14), command=task)
        task_create.place(relwidth=0.08, relx=0.9, rely=0.9, relheight=0.08)
    manual()
    root.mainloop()
    return

def task2():
    global Answer
    words = [
        "песок", "надежда", "степень", "ферма", "теннис",
        "железо", "гора", "вид", "комната", "равнина",
        "кровь", "шанс", "мечта", "субъект", "смех",
        "кристалл", "фигура", "неделя", "шум", "космос",
        "чай", "голос", "козел", "карта", "морковь",
        "возраст", "мотор", "образец", "кольцо", "ботинок",
        "случай", "остров", "продажа", "опасность", "лист",
        "полотенце", "мышь", "книга", "камень", "яблоко",
        "жара", "собака", "стекло", "причина",
        "круг", "газ", "викторина", "полка", "друг",
        "груша", "скала", "желание", "маска", "разговор",
        "лицо", "число", "суп", "год", "кровать",
        "хлеб", "чешуя", "замена", "озеро", "голова",
        "луна", "фактор", "олень", "часы", "корабль",
        "мальчик", "виноград", "стол", "дорога", "пластик",
        "лед", "радость", "небо", "колокол",
        "уровень", "штора", "кусок", "король", "еда",
        "учитель", "ухо", "фермер", "поверхность", "адрес",
        "диета", "шифр", "весна", "угорь", "пол",
        "сердце", "краска", "магнит", "вода", "помидор",
        "тюлень", "золото", "основа", "корона",
        "насекомое", "тип", "улица", "линия", "песня",
        "проект", "брезент", "апельсин", "актер", "мир",
        "член", "область", "сумма", "поездка", "кошелек",
        "парус", "радио", "факт", "день", "самолёт",
        "минута", "тесьма", "зрение", "колония",
        "дюйм", "мужчина", "зерно", "сон", "площадь",
        "погода", "девочка", "рамка", "ягода", "снег",
        "правило", "копия", "работа", "шея", "дом",
        "картина", "лук", "ребенок", "система", "хвост",
        "все", "фильм", "соль", "метка", "текст",
        "весло", "дерево", "волос", "период", "удар",
        "письмо", "фонтан", "запад", "идея", "игра",
        "размер", "лицо", "кость", "трактор", "место",
        "мясо", "племянница", "заказ", "веревка", "вопрос",
        "стрела", "вилка", "одежда", "печь", "чудо"
    ]
    text1 = []
    text2 = []
    text3 = []
    text4 = []
    text5 = []
    lens = len(words)
    #print(lens)
    a=1
    Answer = []
    for i in range(5):
        for j in range(6):
            word = words[random.randint(0,lens-1)]
            while word in Answer:
                word = words[random.randint(0, lens - 1)]
            Answer.append(word)
            if a==1:
                text1.append(word+ '\n'+'\n')
            if a==2:
                text2.append(word+ '\n'+'\n')
            if a==3:
                text3.append(word+ '\n'+'\n')
            if a==4:
                text4.append(word+ '\n'+'\n')
            if a==5:
                text5.append(word+ '\n'+'\n')
        a=a+1
    text1 = ''.join(text1)
    #print(text1)
    text2 = ''.join(text2)
    #print(text2)
    text3 = ''.join(text3)
    #print(text3)
    text4 = ''.join(text4)
    #print(text4)
    text5 = ''.join(text5)
    #print(text5)
    print(Answer)

    def task_start(labels):
        global title
        for i in range(len(labels)):
            labels[i].destroy()
        frame = Frame(root, bg='white')
        frame.place(relwidth=0.33, relx=0.33, rely=0.9, relheight=0.1)
        title = Label(frame, bg='white')
        title.configure(text='00:00', font=("Arial", 16))
        title.pack(fill="both")
        def resize_text(event):
            height = event.height
            new_font_size = int(height / 4)
            title.config(font=("Arial", new_font_size))
        root.bind('<Configure>', resize_text)
        start()
        recognition(task=2)
    def task():
        root.title('Задание 2')
        root.geometry('800x600')
        frame = Frame(root, bg='white')
        frame.place(relwidth=1, relheight=1)
        labels=[]
        a=0
        b=1
        for j in range(5):
            if b==1:
                text = text1
            if b==2:
                text = text2
            if b==3:
                text = text3
            if b==4:
                text = text4
            if b==5:
                text = text5
            #print(text)
            title = Label(frame, text=text, font=("Arial", 20), bg="white")
            title.grid(row=1,column=j)
            title.place(relx=a, relwidth=0.2, relheight=0.75)
            labels.append(title)
            a=a+0.2
            b=b+1
        task_go = Button(root, text="Старт", font=("Arial", 14), command=lambda: task_start(labels))
        task_go.place(relwidth=0.08, relx=0.9, rely=0.9, relheight=0.08)
    def manual():
        root.title('Инструкция')
        root.geometry('900x700')
        frame = Frame(root, bg='white')
        frame.place(relwidth=1, relheight=1)
        label1=Label(root,text="Задание 2. Тест на запоминание слов", bg="white", font=("Arial", 24))
        label1.place(relwidth=1, relheight=0.08)
        image = Image.open("images/task2.png")
        new_width = 320
        new_height = 220
        resized_image = image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(resized_image)
        label2 = Label(root, image=photo, bg="white")
        label2.image = photo
        label2.place(relx=0.05, rely=0.2)

        def update_message_width(event):
            if event.width>100:
                label3.config(width=event.width - 400)
        label3=Message(root, width=400, bg="white",anchor=W, font=("Arial", 16), text=" Этот тест оценивает работу префронтальной коры левого полушария, ответственной за кратковременную память. Задания теста следует выполнять через каждые 5 дней тренировок по Заданию 1.\n    Вашему вниманию будут представлены 30 простых слов. За две минуты необходимо запомнить как можно больше слов. По истечении отведенного времени нажмите на кнопку Старт. Назовите вслух все слова, которые удастся запомнить. Слова можно произносить в произвольном порядке.\n   Максимальное рекомендуемое время, которое отводится на выполнение задания также две минуты.\n   Количество правильно запомненных слов равняется количеству баллов.")
        label3.place(x=320, relx=0.05, rely=0.1)
        root.bind("<Configure>", update_message_width)
        task_create = Button(root, text="Далее", font=("Arial", 14), command=task)
        task_create.place(relwidth=0.08, relx=0.9, rely=0.9, relheight=0.08)
    manual()
    root.mainloop()

def task3():
    global Answer
    words = ["синий", "жёлтый", "красный", "зелёный"]
    colours = ["red","green","yellow","blue"]
    lens = len(words)
    lens1 = len(colours)
    def rgb_to_hex(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'
    root.title('Задание 3')
    root.geometry('900x700')
    root.minsize(900, 700)
    frame = Frame(root, bg='white')
    frame.place(relwidth=1, relheight=1)
    def task():
        global title
        frame = Frame(root, bg='white')
        frame.place(relwidth=1, relheight=1)
        a = 0
        b = 0
        labels = []
        Answer = []
        for i in range(5):
            for j in range(10):
                word = words[random.randint(0,lens-1)]
                color = colours[random.randint(0,lens1-1)]
                if color == "yellow":
                    color = rgb_to_hex(250, 230 , 100)
                title1 = Label(frame, text=word, font=("Arial", 20), bg="white", fg=color)
                title1.grid(row=j, column=i, sticky="nsew")
                title1.place(rely=b, relx=a, relwidth=0.2, relheight=0.05)
                labels.append(title1)
                b=b+0.08
                if color == "red":
                    color="красный"
                elif color == "green":
                    color="зелёный"
                elif color == "#fae664":
                    color = "жёлтый"
                elif color == "blue":
                    color="синий"
                Answer.append(color)
            a=a+0.2
            b=0
        frame4 = Frame(root, bg='white')
        frame4.place(relwidth=0.33, relx=0.33, rely=0.9, relheight=0.1)
        title = Label(frame4, bg='white')
        title.configure(text='00:00', font=("Arial", 16))
        title.pack(fill="both")
        def resize_text(event):
            height = event.height
            if height>100 and height<300:
                new_font_size = int(height / 7)
                title.config(font=("Arial", new_font_size))
                numberlist=0
                new_font_size = int(height/6)
                while numberlist<len(labels):
                    labels[numberlist].configure(font=("Arial", new_font_size))
                    numberlist+=1
        root.bind('<Configure>', resize_text)
        print(Answer)
        start()
        recognition(task=3)
    def manual():
        root.title('Инструкция')
        root.geometry('900x700')
        frame = Frame(root, bg='white')
        frame.place(relwidth=1, relheight=1)
        label1=Label(root,text="Задание 3. Тест Струпа", bg="white", font=("Arial", 24))
        label1.place(relwidth=1, relheight=0.08)
        image = Image.open("images/task3.png")
        new_width = 320
        new_height = 220
        resized_image = image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(resized_image)
        label2 = Label(root, image=photo, bg="white")
        label2.image = photo
        label2.place(relx=0.05, rely=0.2)

        def update_message_width(event):
            if event.width>100:
                label3.config(width=event.width - 400)
        label3=Message(root, width=400, bg="white",anchor=W, font=("Arial", 16), text=" Тест Струпа оценивает общую работу левого и правого полушарий. Задание теста содержит карту слов (названия цветов), напечатанных шрифтом несоответствующих значениям цветов. Встречаются также слова, в которых цвет букв и значение цвета не совпадают.\n  Вам нужно произнести вслух название цвета, которым записано слово. Обратите внимание, что при выполнении теста читать сами слова не нужно.\n    Сначала потренируйтесь, прочитав одну строчку теста. И только затем приступайте к выполнению собственно теста.\n    Скорость выполнения индивидуальна для каждого человека, поэтому здесь нет никаких норм. Каждый раз ориентируйтесь на свой собственный результат выполнения этого теста на предыдущей неделе.\n  Задания теста следует выполнять после выполнения Задания 2 и через каждые 5 дней тренировок по Заданию 1.\n Количество правильно запомненных слов равняется количеству баллов.")
        label3.place(x=320, relx=0.05, rely=0.1)
        root.bind("<Configure>", update_message_width)
        task_create = Button(root, text="Далее", font=("Arial", 14), command=task)
        task_create.place(relwidth=0.08, relx=0.9, rely=0.9, relheight=0.08)
    manual()
    root.mainloop()

def file_scan():
    global r
    global headers
    headers = {"Authorization": "Bearer " + access_token}
    files = {
        "data": ("metadata", json.dumps({"title":"file.txt", "parents": [{"id": "1toMxpPc_CbQRS4xwk3WqSStUFeeiTr5B"}]}), "application/json; charset=UTF-8"),
    }
    #r = requests.post("https://www.googleapis.com/upload/drive/v2/files?uploadType=multipart", headers=headers, files=files)
    #print(r.json())

    params = {
    'q': "mimeType != 'application/vnd.google-apps.folder'",  # Фильтрация только файлов
    'pageSize': 100,  # Количество файлов на странице
    'fields': 'nextPageToken, files(id, name, mimeType)',
    }
    r = requests.get('https://www.googleapis.com/drive/v3/files', headers=headers, params=params)
    r = r.json()
    #print(r)
    return
def file_in_google(arg):
    global file_name
    token()
    file_scan()
    file_id = None
    for file in r['files']:
        if file['name'] == file_name:
            file_id = file['id']
            break
    if file_id:
        print(f"Файл найден в облаке '{file_name}': {file_id}")
        if arg==1:
            os.remove(destination)
            print("Файл удалён из папки")
        url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

        response = requests.get(url, headers=headers, stream=True)
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Файл загружен из облака и сохранён как {destination}")
        print(destination)
    else:
        print(f"Файл с именем '{file_name}' не найден в облаке.")
        if arg==0:
            with open(destination, 'w+'):
                print("Файл создан")
def check_file_in_folder():
    if not os.path.exists("Base"):
        os.makedirs("Base")
        print("Папка Base создана")
    if check_internet_connection() == True and var1.get() == "on":
        if os.path.isfile(destination):
            print(f"Файл '{file_name}' найден в папке.")
            file_in_google(arg=1)
        else:
            print(f"Файл '{file_name}' не найден в папке.")
            file_in_google(arg=0)
    else:
        if os.path.isfile(destination):
            print(f"Файл '{file_name}' найден в папке.")
        else:
            with open(destination,'w+'):
                print("Файл создан")
    return
def get_text():
    global destination, file_name
    if var1.get() == "on":
        user_input = entry.get()
        print(f"Введенный текст: {user_input}")
        with open('config.txt', 'w', encoding='utf-8') as file:
            file.write(f"last_name:{user_input}\noffline_recognition_install:{offline_recognition_install}")
        update_config()
        file_name = user_input+'.txt'
        folder_path = (os.path.abspath('Base')) + '/'
        destination = os.path.join(folder_path, file_name)
    else:
        destination = "default.txt"
        file_name=destination
    check_file_in_folder()
    return
def task(task_number):
    get_text()
    if task_number == 1:
        task1()
    elif task_number == 2:
        task2()
    elif task_number == 3:
        task3()
def statistics():
    get_text()
    root.title('Статистика')
    root.geometry('800x600')
    root.resizable(width=True, height=True)
    root.minsize(800, 600)
    frame = Frame(root, bg='white')
    frame.place(relwidth=1, relheight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14))
    style.configure("Treeview.Heading", font=("Arial", 18, "bold"))

    columns = ("Дата", "Результаты")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.pack(expand=True, side=TOP, fill=BOTH, padx=20, pady=50)

    tree.heading("Дата", text="Дата")
    tree.heading("Результаты", text="Результаты")
    tree.column("Дата", width=200, anchor="center", stretch=False)
    tree.column("Результаты", anchor="center", stretch=True)

    data = []

    with open(destination, 'r') as file:
        for line in file:
            string = line.strip()
            string = string.split(' ')
            string[2]="Задание№1"
            string[5] = "Задание№2"
            string[8] = "Задание№3"
            string_1 = string[0]
            string_2 = string[2:]
            j=7
            for i in range(3):
                if string_2[j]=="x":
                    del string_2[j+1]; del string_2[j]; del string_2[j-1]
                j -= 3
            new = (string_1, string_2)
            data.append(new)

    for item in data:
        tree.insert("", END, values=item)

    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    go_menu = Button(frame, text="В меню", font=("Arial", 16), command=menu)
    go_menu.place(relx=1, rely=1, x=-110, y=-45)

def menu():
    global entry, start_time, elapsed_time, var1, var2, Prav
    entrys = []
    start_time = 0
    elapsed_time = 0
    root.title('Меню')
    root.geometry('800x600')
    root.resizable(width=True, height=True)
    root.minsize(800, 600)
    frame = Frame(root, bg='white')
    frame.place(relwidth=1, relheight=1)
    title = Label(frame,text="Японская система развития интеллекта и памяти",font=("Arial", 20), bg="white")
    title.place(relwidth=1, relheight=0.2)

    def entry_setting(var1, var2):
        global entry
        if var1 == "on":
            entry = Entry(root, font=("Arial", 16), bg="white", bd=3, highlightbackground="lightgray", highlightthickness=1)
            entrys.append(entry)
            entry.place(relwidth=0.4, relx=0.01, rely=0.94, relheight=0.05)
            try:
                if last_name !="None":entry.insert(0, last_name)
            except:None
            check1.place(relwidth=0.26, relx=0.01, rely=0.89, relheight=0.05)
            check2.place(relwidth=0.15, relx=0.41, rely=0.94, relheight=0.05)
        else:
            for i in range(len(entrys)):
                entrys[i].destroy()
            check1.place(relwidth=0.26, relx=0.01, rely=0.94, relheight=0.05)
            check2.place(relwidth=0.14, relx=0.27, rely=0.94, relheight=0.05)
        if var2 == "on":
            Thread(target=active_vosk).start()


    var1 = StringVar(value=0)
    var2 = StringVar(value=0)

    def check():
        # print(var1.get())
        # print(var2.get())
        entry_setting(var1.get(), var2.get())

    check1 = Checkbutton(root, text="Многопользовательский режим", variable=var1, onvalue="on", offvalue="off", command=check)
    check1.place(relwidth=0.26, relx=0.01, rely=0.94, relheight=0.05)
    check2 = Checkbutton(root, text="Офлайн режим", variable=var2, onvalue="on", offvalue="off", command=check)
    check2.place(relwidth=0.14, relx=0.27, rely=0.94, relheight=0.05)

    def resize_text(event):
        width = event.width
        width = width / 1000
        if width > 1:
            title.configure(font=("Arial", int(width*10+14)))
            btn1.configure(font=("Arial", int(width*10)))
            btn2.configure(font=("Arial", int(width * 10)))
            btn3.configure(font=("Arial", int(width * 10)))
            go_statistics.configure(font=("Arial", int(width * 10)))
            check1.configure(font=("Arial", int(width * 10)))
            check2.configure(font=("Arial", int(width * 10)))
        if var1.get() == "on":
            if width>0.35:
                entry.configure(font=("Arial", 20))
            elif width>0.32:
                entry.configure(font=("Arial", 18))
            else:
                entry.configure(font=("Arial", 16))


    btn1 = Button(root, text="Задание 1", command=lambda: task(task_number=1))
    btn1.place(relwidth=0.1, relx=0.35, rely=0.5, relheight=0.06, anchor=CENTER)
    btn2 = Button(root, text="Задание  2", command=lambda: task(task_number=2))
    btn2.place(relwidth=0.1, relx=0.5, rely=0.5, relheight=0.06, anchor=CENTER)
    btn3 = Button(root, text="Задание  3", command=lambda: task(task_number=3))
    btn3.place(relwidth=0.1, relx=0.65, rely=0.5, relheight=0.06, anchor=CENTER)
    go_statistics = Button(root, text="Статистика", command=statistics)
    go_statistics.place(relwidth=0.12, relx=0.86, rely=0.94, relheight=0.05)

    root.bind("<Configure>", resize_text)
    try:
        if Prav != None:showinfo(title="Результат",message=f"Количество правильных ответов: {Prav}, время: {minutes} минут, {seconds} секунд");Prav=None
    except:None
    root.mainloop()

def save_data(task_number):
    global Prav
    today = str(date.today())
    Prav=str(Prav)
    list_strings=[]
    string_file = False
    with open(destination, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            list_strings.append(line)
            if today in line:
                print(f"Найдена строка {line_number}: {line.strip()}")
                string_in_file = line.strip()
                string_file=True
    #print(list_strings)
    string = ""
    if string_file==True:
        string+=string_in_file
        string = string.split(' ')
        if task_number==1:
            try:
                int(string[3])
                print(f"Задание номер {task_number} уже выполнено сегодня")
                return
            except:
                string[3]=Prav
                string[4] = f"{minutes}:{seconds}"
        elif task_number==2:
            try:
                int(string[6])
                print(f"Задание номер {task_number} уже выполнено сегодня")
                return
            except:
                string[6]=Prav
                string[7] = f"{minutes}:{seconds}"
        elif task_number==3:
            try:
                int(string[9])
                print(f"Задание номер {task_number} уже выполнено сегодня")
                return
            except:
                string[9]=Prav
                string[10] = f"{minutes}:{seconds}"
        string = ' '.join(string)
        with open(destination, 'w', encoding='utf-8') as file:
            list_strings[line_number-1] = string
            file.writelines(list_strings)
    else:
        string+=today+" 1 Task_1 x x:x Task_2 x x:x Task_3 x x:x"
        string=string.split(' ')
        if task_number==1:
            string[3]=Prav
            string[4]=f"{minutes}:{seconds}"
        if task_number==2:
            string[6]=Prav
            string[7] = f"{minutes}:{seconds}"
        if task_number==3:
            string[9]=Prav
            string[10] = f"{minutes}:{seconds}"
        string = ' '.join(string)
        with open(destination, 'r', encoding='utf-8') as file:
            line_count = sum(1 for _ in file)
        with open(destination, 'a', encoding='utf-8') as file:
            if line_count>1:
                file.write('\n'+string)
            else:
                file.write(string+'\n'+"")
    print(string)
    return

def recognition(task):
    recognizer = sr.Recognizer()
    SAMPLE_RATE = 16000
    CHANNELS = 1
    DURATION = 1
    recording = False
    audio_frames = []
    def start_recording():
        global recording, audio_frames
        recording = True
        audio_frames = []
        while recording:
            audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
            sd.wait()
            audio_frames.append(audio_data)

    def on_start():
        if not recording:
            Thread(target=start_recording).start()

    def audio_to_text():
        global audio_frames
        sd.wait()
        recognizer = sr.Recognizer()
        if audio_frames:
            combined_audio = b"".join(audio_frames)
            combined_audio = sr.AudioData(combined_audio, SAMPLE_RATE, 2)
            #print(combined_audio,'\n',type(combined_audio))
        else:
            print(f"Ошибка audio_frames")
            stop()
            menu()
        if check_internet_connection() == True:
            try:
                text = recognizer.recognize_google(combined_audio, language="ru-RU")
                text = text.split(' ')
                text = ', '.join(text)
                text = text.split(', ')
                print("Обработка результатов записи")
                return text
            except Exception as e:
                print(f"Ошибка {e}")
                stop()
                menu()
        elif var2.get()=="on" and offline_recognition_install=="True":
            try:
                model_path = "vosk-model/vosk-model-small-ru-0.22"
                model = vosk.Model(model_path)
                recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
                raw_data = combined_audio.get_raw_data()
                recognizer.AcceptWaveform(raw_data)
                result_json = json.loads(recognizer.Result())
                text = result_json['text']
                print("Распознанный текст:", text)
                if task == 1:
                    def text_to_numbers(text):
                        numbers_map = {
                            "ноль": "0",
                            "один": "1",
                            "два": "2",
                            "три": "3",
                            "четыре": "4",
                            "пять": "5",
                            "шесть": "6",
                            "семь": "7",
                            "восемь": "8",
                            "девять": "9",
                            "десять": "10",
                            "одиннадцать": "11",
                            "двенадцать": "12",
                            "тринадцать": "13",
                            "четырнадцать": "14",
                            "пятнадцать": "15",
                            "шестнадцать": "16",
                            "семнадцать": "17",
                            "восемнадцать": "18",
                            "девятнадцать": "19",
                            "двадцать": "20",
                            "тридцать": "30",
                            "сорок": "40",
                            "пятьдесят": "50",
                            "шестьдесят": "60",
                            "семьдесят": "70",
                            "восемьдесят": "80",
                            "девяносто": "90",
                            "сто": "100"
                        }
                        words = text.split()
                        result = []
                        for word in words:
                            if word in numbers_map:
                                result.append(numbers_map[word])
                            else:
                                result.append(word)
                        return result
                    text = text_to_numbers(text)
                    print(text)
                return text
            except Exception as e:
                print(e)
                stop()
                menu()
        else:
            stop()
            menu()


    if task == 1:
        def stop_recording():
            global recording, audio_frames, Prav
            recording = False
            stop()
            text = audio_to_text()
            numberlist = 0
            while numberlist < len(text):
                string = text[numberlist]
                string = re.sub(r'\D', '', string)
                if string == '':
                    del text[numberlist]
                else:
                    text[numberlist] = string
                numberlist += 1
            print(text)
            numberlist = 0
            Prav = 0
            while numberlist != len(text) and numberlist != len(Answer):
                if len(text[numberlist]) > len(Answer[numberlist]):
                    if text[numberlist][0] == Answer[numberlist] and len(text[numberlist]) >= 2:
                        first_part = text[numberlist][0]
                        second_part = text[numberlist][1:]
                        length = len(text)
                        text.append('')
                        while numberlist != length:
                            text[length] = text[length - 1]
                            length -= 1
                        text[numberlist] = first_part
                        text[numberlist + 1] = second_part
                        print(text)
                    elif text[numberlist][0] == Answer[numberlist][0]:
                        first_part = text[numberlist][0] + text[numberlist][1]
                        second_part = text[numberlist][2:]
                        length = len(text)
                        text.append('')
                        while numberlist != length:
                            text[length] = text[length - 1]
                            length -= 1
                        text[numberlist] = first_part
                        text[numberlist + 1] = second_part
                        print(text)

                if len(text[numberlist]) < len(Answer[numberlist]):
                    answer_len = len(Answer[numberlist])
                    index_text = 0
                    all_index = 0
                    string = ''
                    while all_index != answer_len and numberlist + index_text < len(text):
                        text_len = len(text[numberlist + index_text])
                        index = 0
                        for i in range(text_len):
                            if all_index < len(Answer[numberlist]) and str(
                                    text[numberlist + index_text][index]) == str(
                                Answer[numberlist][all_index]):
                                string = string + str(text[numberlist + index_text][index])
                            else:
                                break
                            index += 1
                            all_index += 1
                        index_text += 1
                    if index == text_len and string == Answer[numberlist]:
                        text[numberlist] = string
                        for i in range(index_text - 1):
                            del text[numberlist + 1]
                        print(text)
                if len(Answer[numberlist]) == 2 and len(text[numberlist]) == 2 and Answer[numberlist][1] == '0' and \
                        text[numberlist][1] != '0' and numberlist + 1 < len(Answer) and text[numberlist][1] == Answer[
                    numberlist + 1]:
                    first_part = text[numberlist][0] + "0"
                    second_part = text[numberlist][1]
                    length = len(text)
                    text.append('')
                    while numberlist != length:
                        text[length] = text[length - 1]
                        length -= 1
                    text[numberlist] = first_part
                    text[numberlist + 1] = second_part
                    print(text)
                if text[numberlist] != Answer[numberlist] and text[numberlist] == Answer[numberlist + 1]:
                    length = len(text)
                    text.append('')
                    while numberlist != length:
                        text[length] = text[length - 1]
                        length -= 1
                    text[numberlist] = ''
                    print(text)
                if Answer[numberlist] == text[numberlist]:
                    Prav += 1
                numberlist += 1
            print(Prav)
            save_data(task_number=1)
            menu()

        stop_button = Button(root, text="Стоп", font=("Arial", 14), command=stop_recording)
        stop_button.place(relwidth=0.08, relx=0.9, rely=0.9, relheight=0.08)

        on_start()


    elif task == 2:
        def stop_recording():
            global recording, audio_frames, Prav
            recording = False
            stop()
            text = audio_to_text()
            text = [s.lower () for s in text]
            numberlist = 0
            Prav=0
            answer_out = []
            while numberlist != len(text) and numberlist != len(Answer):
                if text[numberlist] in Answer and text[numberlist] not in answer_out:
                    answer_out.append(text[numberlist])
                    Prav+=1
                numberlist+=1
            print(answer_out)
            print(f"Кол-во прав ответов: {Prav}")
            save_data(task_number=2)
            menu()

        stop_button = Button(root, text="Стоп", font=("Arial", 14), command=stop_recording)
        stop_button.place(relwidth=0.08, relx=0.9, rely=0.9, relheight=0.08)

        on_start()

    elif task==3:
        def stop_recording():
            global recording, audio_frames, Prav
            recording = False
            stop()
            text = audio_to_text()
            numberlist = 0
            Prav = 0
            while numberlist != len(text) and numberlist != len(Answer):
                if text[numberlist] == Answer[numberlist]:
                    Prav += 1
                numberlist += 1
            print(f"Кол-во прав ответов: {Prav}")
            save_data(task_number=3)
            menu()

        stop_button = Button(root, text="Стоп", font=("Arial", 14), command=stop_recording)
        stop_button.place(relwidth=0.08, relx=0.9, rely=0.9, relheight=0.08)

        on_start()



def manual():
    root.title('Инструкция')
    root.geometry('800x600')
    root.resizable(width=True, height=True)
    root.minsize(800, 600)
    frame = Frame(root, bg='white')
    frame.place(relwidth=1, relheight=1)
    title = Label(frame, text="Инструкция по применению", font=("Arial", 20), bg="white")
    title.place(relwidth=1, relheight=0.1)

    def resize_text(event):
        if event.width > 600:
            label3.config(width=event.width - 130)
        new_width = int(event.width/100)+5
        #print(new_width)
        if new_width>14:
            title.config(font=("Arial", new_width+6))
            label3.config(font=("Arial", new_width))
            new_width-=4
            if new_width>16:
                go_menu.config(font=("Arial", new_width))
    root.bind('<Configure>', resize_text)

    label3 = Message(root, bg="white", anchor=W, font=("Arial", 16),text="    Представленное приложение разработано в качестве технической поддержки книги японского нейроучёного, специалиста по томографии мозга Рюта Кавасима «Японская система развития интеллекта и памяти».\n\n   Приложение содержит три вида заданий:\n       1. Решение простых примеров.\n       2. Тест на запоминание слов.\n       3. Тест Струпа.\n\n   Задание 1 следует выполнять ежедневно в первой половине дня после приема пищи, когда активность мозга максимальна.\n\n  Задания 2 и 3 выполняются через каждые 5 дней тренировок по Заданию 1")
    label3.place(relx=0.05, rely=0.1)
    go_menu = Button(root, text="В меню", font=("Arial", 16), command=menu)
    go_menu.place(relwidth=0.1, relx=0.88, rely=0.88, relheight=0.1)
    root.mainloop()
manual()



