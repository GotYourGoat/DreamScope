import tkinter as tk
import datetime as dt
import time
import requests
import json

datetime_now = dt.datetime.now()

# https://openweathermap.org request
url_base = 'https://api.openweathermap.org/data/2.5/onecall?'
lat = 'lat=33.05'
lon = '&lon=-97.00'
exclude = '&exclude=minutely,daily'
api = '&appid=0ab54173237cb859631183149512cef7'

open_weather_request = url_base + lat + lon + exclude + api
response = requests.get(open_weather_request)
open_weather = response.json()


# Returns a string for the time of day. morning/afternoon/evening
def time_of_day():
    full_hour_now = datetime_now.strftime("%H")  # A 23hr format
    morning_times = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    afternoon_times = ['12', '13', '14', '15', '16', '17']
    evening_times = ['18', '19', '20', '21', '22', '23']

    if full_hour_now in morning_times:
        return ("morning")
    elif full_hour_now in afternoon_times:
        return ("afternoon")
    elif full_hour_now in evening_times:
        return ("evening")


# The main app.

class DreamScopeApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.block_PhotoImage = tk.PhotoImage(file='images/block_image.gif')
        self.backdrop_PhotoImage = tk.PhotoImage(file='images/mastercloudv2.gif')
        self.master = master
        self.footer_clock_str = ""

    def initialize(self):
        self.generate_canvas()
        self.generate_footer()
        self.set_clock()
        self.place(x=0, y=0)
        self.forecast_blocks()

    def generate_canvas(self):
        self.backdrop_canvas = tk.Canvas(self, width=500, height=500, highlightthickness=0, borderwidth=0)
        self.backdrop_canvas.pack()
        self.backdrop_canvas.create_image(0, 0, image=self.backdrop_PhotoImage, anchor="nw")

    def generate_footer(self):
        self.current_temp = str(round((open_weather["current"]["temp"] - 273.15) * 9 / 5 + 32)) + "°F"
        self.footer_canvas = tk.Canvas(self.backdrop_canvas, bg="black", height=80, width=500, highlightthickness=0,
                                       borderwidth=0)
        self.footer_canvas.place(y=420, x=0)
        self.footer_block = self.footer_canvas.create_text(40, 10, text="Now:", font=("Verdana", 13, "bold"),
                                                           fill="white")
        self.footer_clock = self.footer_canvas.create_text(400, 10, text=self.footer_clock_str,
                                                           font=("Verdana", 13, "bold"),
                                                           fill="white", anchor="center", )
        self.footer_temp = self.footer_canvas.create_text(400, 40, text=self.current_temp,
                                                          font=("Verdana", 13, "bold"),
                                                          fill="white", anchor="center", )
        self.footer_conditions = self.footer_canvas.create_text(400, 60,
                                                                text=open_weather['current']['weather'][0]['main'],
                                                                font=("Verdana", 13, "bold"),
                                                                fill="white", anchor="center")

    def set_clock(self):
        self.this_hour = time.strftime("%#I")
        self.this_minute = time.strftime("%M")
        self.this_second = time.strftime("%#S")
        self.am_pm = time.strftime(" %p")
        self.tick_tock = ":"
        if int(self.this_second) % 2 == 0:
            self.tick_tock = " "
        else:
            self.tick_tock = ":"

        self.completed_clock = str(self.this_hour + self.tick_tock + self.this_minute + self.am_pm)
        self.footer_clock_str = self.completed_clock
        self.footer_canvas.itemconfigure(self.footer_clock, text=self.completed_clock)
        self.after(1000, self.set_clock)

    def forecast_blocks(self):
        self.these_times = []
        self.these_temps = []
        self.these_conditions = []

        for i in range(12):
            self.temp_response = int(open_weather['hourly'][i]['temp'])
            self.temp_f = str(round((self.temp_response - 273.15) * 9 / 5 + 32)) + '°F'
            self.these_temps.append(self.temp_f)

            self.current_time_int = int(time.strftime("%#I"))
            self.new_time = self.current_time_int + i + 1
            self.new_am_pm = time.strftime("%p")
            if self.new_time > 12:
                self.new_time -= 12
                if time.strftime("%p") == "AM":
                    self.new_am_pm = "PM"
                elif time.strftime("%p") == "PM":
                    self.new_am_pm = "AM"

            self.new_time_string = str(self.new_time) + ' ' + self.new_am_pm
            self.these_times.append(self.new_time_string)

            self.condition = open_weather['hourly'][i]['weather'][0]['main']
            self.these_conditions.append(self.condition)

        self.block_anchors = [
            (74, 89), (167, 89), (260, 89), (353, 89),
            (74, 182), (167, 182), (260, 182), (353, 182),
            (74, 275), (167, 275), (260, 275), (353, 275)
        ]

        self.forecast_block_1 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[0] +
                                              '\n\n' + self.these_temps[0] +
                                              '\n' + self.these_conditions[0],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_2 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[1] +
                                              '\n\n' + self.these_temps[1] +
                                              '\n' + self.these_conditions[1],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_3 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[2] +
                                              '\n\n' + self.these_temps[2] +
                                              '\n' + self.these_conditions[2],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_4 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[3] +
                                              '\n\n' + self.these_temps[3] +
                                              '\n' + self.these_conditions[3],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_5 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[4] +
                                              '\n\n' + self.these_temps[4] +
                                              '\n' + self.these_conditions[4],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_6 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[5] +
                                              '\n\n' + self.these_temps[5] +
                                              '\n' + self.these_conditions[5],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_7 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[6] +
                                              '\n\n' + self.these_temps[6] +
                                              '\n' + self.these_conditions[6],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_8 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[7] +
                                              '\n\n' + self.these_temps[7] +
                                              '\n' + self.these_conditions[7],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_9 = tk.Label(self,
                                         font=("Verdana", 9, 'bold'),
                                         text=self.these_times[8] +
                                              '\n\n' + self.these_temps[8] +
                                              '\n' + self.these_conditions[8],
                                         justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_10 = tk.Label(self,
                                          font=("Verdana", 9, 'bold'),
                                          text=self.these_times[9] +
                                               '\n\n' + self.these_temps[9] +
                                               '\n' + self.these_conditions[9],
                                          justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_11 = tk.Label(self,
                                          font=("Verdana", 9, 'bold'),
                                          text=self.these_times[10] +
                                               '\n\n' + self.these_temps[10] +
                                               '\n' + self.these_conditions[10],
                                          justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_12 = tk.Label(self,
                                          font=("Verdana", 9, 'bold'),
                                          text=self.these_times[11] +
                                               '\n\n' + self.these_temps[11] +
                                               '\n' + self.these_conditions[11],
                                          justify='center', height=5, width=9, relief="ridge", bd=5)

        self.forecast_block_1.place(x=self.block_anchors[0][0], y=self.block_anchors[0][1])
        self.forecast_block_2.place(x=self.block_anchors[1][0], y=self.block_anchors[1][1])
        self.forecast_block_3.place(x=self.block_anchors[2][0], y=self.block_anchors[2][1])
        self.forecast_block_4.place(x=self.block_anchors[3][0], y=self.block_anchors[3][1])
        self.forecast_block_5.place(x=self.block_anchors[4][0], y=self.block_anchors[4][1])
        self.forecast_block_6.place(x=self.block_anchors[5][0], y=self.block_anchors[5][1])
        self.forecast_block_7.place(x=self.block_anchors[6][0], y=self.block_anchors[6][1])
        self.forecast_block_8.place(x=self.block_anchors[7][0], y=self.block_anchors[7][1])
        self.forecast_block_9.place(x=self.block_anchors[8][0], y=self.block_anchors[8][1])
        self.forecast_block_10.place(x=self.block_anchors[9][0], y=self.block_anchors[9][1])
        self.forecast_block_11.place(x=self.block_anchors[10][0], y=self.block_anchors[10][1])
        self.forecast_block_12.place(x=self.block_anchors[11][0], y=self.block_anchors[11][1])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("DreamScope")
    root.resizable(False, False)
    root.geometry('500x500')

    Forecast = DreamScopeApp(root)

    Forecast.initialize()
    root.mainloop()
