from pydoc import visiblename
import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
from django import views
import requests


sg.theme("black")
def get_weather(location):
    url = f'https://www.google.com/search?q=weather+{location.replace(" ","+")}'
    session = requests.Session()
    session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    source = session.get(url)
    soup = bs(source.text, "lxml")
    loca = soup.find("div", attrs={"id":"wob_loc"}).text
    day = soup.find("div", attrs={"id":"wob_dts"}).text
    temp = soup.find("span", attrs={"id":"wob_tm"}).text
    weather = soup.find("span", attrs={'id': 'wob_dc'}).text
    return loca,day,temp,weather

image = sg.Column([[sg.Image(key="-IMAGE-", visible=False)]])
data = sg.Column([
    [sg.Text("", key="-LOC-", visible=False)],
    [sg.Text("", key ="-DAY-", visible=False)],
    [sg.Text("", key = "-TEMP-", visible=False), sg.Text("", key="-WEATHER-", visible=False)]
    ])
layout = [
    [sg.Text("Enter the location of the city you want to see weather of!")],
    [sg.Input(key="-INPUT-", expand_x=True), sg.Button("Search", key = "-SEARCH-")],
    [sg.Text("", key = "-WARN-",visible=False, expand_x=True, justification="left")],
    [image, data]
]

window = sg.Window("Weather", layout, alpha_channel=0.7)

while True:
    event, value = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "-SEARCH-":
        try:
            loca,day,temp,weather = get_weather(value["-INPUT-"])
            window["-LOC-"].update(loca, visible=True)
            window["-DAY-"].update(day, visible=True)
            window["-TEMP-"].update(f"{temp}°C", visible=True)
            window["-WEATHER-"].update(weather, visible=True)
            window["-WARN-"].update(visible = False)
            if weather in ('Sun','Sunny','Clear','Clear with periodic clouds', 'Mostly sunny'):
                window['-IMAGE-'].update('icons/sunny.png', visible=True)

            if weather in ('Partly Sunny','Mostly Sunny','Partly cloudy','Mostly cloudy','Cloudy','Overcast'):
                window['-IMAGE-'].update('icons/cloudy-day.png', visible=True)

            if weather in ('Rain','Chance of Rain','Light Rain','Showers','Scattered Showers','Rain and Snow','Hail'):
                window['-IMAGE-'].update('icons/rain.png', visible=True)

            if weather in ('Scattered Thunderstorms','Chance of Storm','Storm','Thunderstorm','Chance of TStorm'):
                window['-IMAGE-'].update('icons/storm.png', visible=True)

            if weather in ('Mist','Dust','Fog','Smoke','Haze','Flurries'):
                window['-IMAGE-'].update('icons/mist.png', visible=True)
                    
            if weather in ('Freezing Drizzle','Chance of Snow','Sleet','Snow','Icy','Snow Showers'):
                window['-IMAGE-'].update('icons/snowy.png', visible=True)
        except Exception as e:
            window["-WARN-"].update(f"""
            Error:{e}
            It looks like you had a typo.
            Please enter the name of the place you want to see the weather correctly.
            """, visible = True)
            window["-LOC-"].update(visible=False)
            window["-DAY-"].update(visible=False)
            window["-TEMP-"].update(visible=False)
            window["-WEATHER-"].update(visible=False)
            window["-IMAGE-"].update(visible=False)


window.close()