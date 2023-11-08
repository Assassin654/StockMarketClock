import customtkinter
import datetime
import pytz
import threading
import os
import time
import keyboard

#pyinstaller --noconsole --onefile --noconfirm --add-data "C:\Users\Paul\AppData\Local\Programs\Python\Python311\Lib\site-packages\customtkinter;customtkinter/" "stockTime.py"
root = customtkinter.CTk()

root.geometry('400x150')
root.attributes('-topmost', True)
root.resizable(False,False)
root.title('Market Clock')

increment = 1

def toggle_timezone(e):
    global zone
    global increment
    global current_zone
    if 'down' not in e: return
    increment += 1
    if increment == 4:
        increment = 0
    zone = pytz.timezone(zones[increment])
    current_zone = zones[increment].split('/')[1] 
    zone_lb.configure(text=f'{current_zone} Time:')

keyboard.hook_key('up', lambda e:toggle_timezone(str(e)))

zones = ['US/Eastern','US/Central','US/Mountain', 'US/Pacific']
zone = pytz.timezone(zones[increment])
current_zone = zones[increment].split('/')[1] 
nyse = pytz.timezone('US/Eastern')

premarket_open = datetime.time(4, 00)
premarket_close = datetime.time(9, 30)
market_open = datetime.time(9, 30)
market_close = datetime.time(16, 0)
aftermarket_open = datetime.time(16, 0)
aftermarket_close = datetime.time(20, 0)

def current_time_zone():
    now = datetime.datetime.now(zone)
    zone_24 = now.strftime('%Y-%m-%d %H:%M:%S')
    zone_12 = now.strftime('%I:%M:%S %p')
    return zone_24, zone_12

def time_remaining(market, now):
    if now >= datetime.time(20,0):
        net = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=1), market)-datetime.datetime.combine(datetime.date.today(), now)
    else:
        net = datetime.datetime.combine(datetime.date.today(), market)-datetime.datetime.combine(datetime.date.today(), now)
    return str(net).split('.')[0]

def market_status():
    now = datetime.datetime.now(nyse).time()
    if premarket_open <= now <= premarket_close:
        net = time_remaining(premarket_close,now)
        return f"({net}) Pre-Market"
    elif market_open <= now <= market_close:
        net = time_remaining(market_close,now)
        return f"({net}) Market"
    elif aftermarket_open <= now <= aftermarket_close:
        net = time_remaining(aftermarket_close,now)
        return f"({net}) After-Market"
    else:
        net = time_remaining(premarket_open,now)
        return f"({net}) Closed"

def current_time_nyse():
    now = datetime.datetime.now(nyse)
    nyse_24 = now.strftime('%Y-%m-%d %H:%M:%S')
    nyse_12 = now.strftime('%I:%M:%S %p')
    return nyse_24, nyse_12


customtkinter.CTkLabel(master=root, text='24-Hour').place(x=125,y=5)
customtkinter.CTkLabel(master=root, text='12-Hour').place(x=300,y=5)
customtkinter.CTkLabel(master=root, text='NYSE Time:').place(x=5,y=25)

zone_lb = customtkinter.CTkLabel(master=root, text='Central Time:')
zone_lb.place(x=5,y=55)

nyse_24_lb = customtkinter.CTkLabel(master=root, text='NYSE Time:')
nyse_24_lb.place(x=125, y=25)
nyse_12_lb = customtkinter.CTkLabel(master=root, text='NYSE Time:')
nyse_12_lb.place(x=300,y=25)
zone_24_lb = customtkinter.CTkLabel(master=root, text='Central Time')
zone_24_lb.place(x=125, y=55)
zone_12_lb = customtkinter.CTkLabel(master=root, text='Central Time')
zone_12_lb.place(x=300, y=55)

customtkinter.CTkLabel(master=root, text='Market Status:').place(x=5,y=125)
market_status_lb = customtkinter.CTkLabel(master=root, text='Status')
market_status_lb.place(x=125,y=125)

def clock():
    while True:
        zone_24, zone_12 = current_time_zone()
        nyse_24, nyse_12 = current_time_nyse()
        status = market_status()
        
        nyse_24_lb.configure(text=f'{nyse_24}')
        nyse_12_lb.configure(text=f'{nyse_12}')
        zone_24_lb.configure(text=f'{zone_24}')
        zone_12_lb.configure(text=f'{zone_12}')
        market_status_lb.configure(text=f'{status}')
        
        time.sleep(.01)

threading.Thread(target=clock).start()

root.mainloop()
os._exit(os.EX_OK)
