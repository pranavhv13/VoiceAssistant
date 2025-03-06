import speech_recognition as sr
import os, datetime, webbrowser, openai, random
from config import apikey

chatStr = ""
count = random.randint(1, 100000)

def say(text):
    os.system(f'say -v Sangeeta "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            say("I didn't catch that. Could you please repeat?")
            return "stop chat"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            say("Service is down, please try again later.")
            return "stop chat"
        except Exception as e:
            print(f"Some error occurred: {e}")
            say("Some error occurred. Please try again.")
            return "stop chat"

def ai(prompt,qry):
    global count
    count += 1
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {qry} \n *************************\n\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    # Retrieve the assistant's response
    completion = response["choices"][0]["message"]["content"]
    text += completion

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    filename = f"Openai/{count}.txt"
    # Save the response to a file
    with open(filename, "w") as f:
        f.write(text)

    print(f"Response saved to {filename}")
    say(f"Response saved")
    os.system(f"open {filename}")


def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\n NEENU: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "User: is user and NEENU: is his personal assistant you answer to pranav within 30 words "},
            {"role": "user", "content": chatStr}
        ]
    )
    completion = response["choices"][0]["message"]["content"]
    say(completion)
    chatStr += f"{completion}\n"
    return completion

if __name__ == '__main__':
    say("Hello I am NEENU, How may I help you")

    query = takeCommand()

    if "the time" in query:
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"Sir time is {hour} and {min} minutes")

    sites = [["youtube", "https://www.youtube.com"], ["college portal", "https://jams-jnnce.in/jams/login.html"],
        ["google", "https://www.google.com"], ]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])
            exit()

    if "the time" in query:
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"Sir time is {hour} and {min} minutes")
        print(f"Sir time is {hour} and {min} minutes sir..")

    elif "play music" in query:
        musicPath = "/Users/admin/Downloads/Uppiginta.mp3"
        os.system(f"open {musicPath}")
        say("Playing music sir..")
        print("Playing Music sir..")

    elif "open photos".lower() in query.lower():
        os.system(f"open /System/Applications/Photos.app")
        say("Opening photos sir..")
        print("Opening photos sir..")

    elif "artificial intelligence".lower() in query.lower():
        query2 = query + " Within 100 tokens "
        ai(prompt=query2, qry=query)

    elif "Stop chat".lower() in query.lower():
        say("Byee")

    else:
        print("Chatting...")
        chat(query)
        print(chatStr)