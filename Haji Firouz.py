import wikipedia
import pyttsx3
import datetime
import speech_recognition as sr
import smtplib

engine = pyttsx3.init()

voices = engine.getProperty('voices')
new_voice_rate = 180
engine.setProperty('rate',new_voice_rate)
engine.setProperty('voice',voices[26].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def say_time():
    time_now = datetime.datetime.now().strftime("%I:%M:%S")
    hour , miniute , second = time_now.split(":")

    print(hour)
    speak(" ساعت "
     + hour
     + "او"
     + miniute
     + "دقیقه او"
     + second
     + "ثانیه")

def say_date():
    year_now = datetime.datetime.now().year
    month_now = datetime.datetime.now().month
    day_now = datetime.datetime.now().day
    
    print(year_now , month_now , day_now)
    speak("امروز "
     + str(day_now)
     + 'ام ه ماهه' 
     + str(month_now)
     + 'ه سال'
     + str(year_now))
    
def greeting():

    speak("سلام مهدی")

    hour = datetime.datetime.now().hour

    if hour >= 6 and hour < 12:
        speak("صبحت بخیر")
    elif hour >= 12 and hour < 18:
        speak("ظهرت بخیر")
    elif hour >= 18 and hour <= 24:
        speak("عصرت بخیر")
    else:
        speak("شبت بخیر")


def presentation():
    speak("حاجی فیروزم من. سالی یه روزم من")
    
    

# welcome()

def bye():
    speak("روز خوبی داشته باشی")

def wikipedia_searching(command):
    command = command.replace('Wikipedia' , '')
    if command ==  '' or command == ' ':
        return 0
    engine.setProperty('voice',voices[13].id)
    new_voice_rate = 130
    engine.setProperty('rate',new_voice_rate)  
    result = wikipedia.summary(command , sentences = 2)
    speak(result)
    engine.setProperty('voice',voices[26].id)
    new_voice_rate = 180
    engine.setProperty('rate',new_voice_rate)

def command_operator(command):


    switcher = {
        0: ['hi'],
        1: ["time"],
        2: ["date"],
        3: ['you' , 'who are you'],
        4: ['bye' , 'offline'],
        5: ['Wikipedia'],
        6: ['email']
    }

    if any(x in command for x in switcher[0]):
        greeting()
    elif any(x in command for x in switcher[1]):
        say_time()
    elif any(x in command for x in switcher[2]):
        say_date()
    elif any(x in command for x in switcher[3]):
        presentation()
    elif any(x in command for x in switcher[4]):
        bye()
        return 1
    elif any(x in command for x in switcher[5]):

        wikipedia_searching(command)
    elif any(x in command for x in switcher[6]):

        try:
            speak("چی براش بفرستم؟")
            content = take_command()
            to = 'jopperdeveloper@gmail.com'
            send_email(to , content)
            speak('با موفقیت فرستادم')
        except Exception as e:
            speak("نتونستم بفرستم")
            print(e)

    else:
        speak('خب که چی')

    return 0


def take_command():

    r = sr.Recognizer()
    m = sr.Microphone()


    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))

    print("Haji Firouz...")
    speak("بگو")

    with m as source: audio = r.listen(source)
    
    try:
        value = r.recognize_google(audio)
        speak(" گرفتم")
        print('you : ', value)
        return value
        
        
    except sr.UnknownValueError:
        speak("نگرفتم چی گفتی دوباره بگو")
        return 1

    except sr.RequestError as e:
        speak("متاسفانه سرویس گوگل جواب نداد")
        return 1



def start():

    
   
    speak("چه کاری از دستم برمیاد؟")
    is_end = 0
    
    while is_end == 0:
        command = take_command()
        if command != 1:
            is_end = command_operator(command)
        
        

def send_email(to , content):
    server = smtplib.SMTP('smtp.gmail.com')
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com'  , 'password')
    server.sendmail('youremail@gmail.com' , to , content)    
    server.close()
   
start()


