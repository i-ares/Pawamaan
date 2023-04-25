 #!/usr/bin/python3
import pyrebase
import serial
import time
from firebase import firebase
from datetime import datetime
import calendar
import tkinter
from tkinter import *
import tkinter.ttk
import time
import sys
import os
time.sleep(1)
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

from PIL import ImageTk,Image
tk= tkinter.Tk()
tk.attributes('-fullscreen',True)
tk.geometry("480x320")
tk.configure(bg='black')
dn=datetime.today().weekday()
lvar=0

def bfunc(): #This is what will happen when we press the button on the touch screen display (This is covered in the future prospects of the project, where we can control a vent wirelessly)
	global lvar
	if lvar==0:
		lvar=1
		db.child("switches").child("0").update({"state":1})
	elif lvar==1:
		lvar=0
		db.child("switches").child("0").update({"state":0})
#GUI of the touch screen display
w='white'
b='black'
g="green"
p=55
pc=7
px=120
s=30
ts=20
ti = datetime.now()
tme = time.localtime()
ct = time.strftime("%H:%M", tme)
mn=calendar.month_name[ti.month]
c1=Canvas(tk,width=240,height=320,bg=b,bd=0, highlightthickness=0, relief='ridge')
c2=Canvas(tk,width=240,height=320,bg=w,bd=0, highlightthickness=0, relief='ridge')
c1.grid(row=0,column=0)
c1.create_oval(40,0,200,160,fill="white")
c1.create_oval(40+pc+1,0+pc+1,200-pc-1,160-pc-1,fill=b)
c1.create_text(120,66,text='AQI',fill=w,font=('Helvetica','30','bold'))
AQI=Label(text="435",font=('Helvetica',ts,'bold'),fg='orange',bg=b)
AQI.place(x=100,y=96)
hur=Label(text=ct,font=('Helvetica',40,'bold'),fg=w,bg=b)
hur.place(x=55,y=185)
mo=Label(text=calendar.day_name[4]+","+mn+" "+str(ti.day)+","+str(ti.year),font=('Helvetica',10,'bold'),fg=w,bg=b)
mo.place(x=35,y=250)
li=Label(text="light intensity",font=('Helvetica',12,'bold'),fg=w,bg=b)
li.place(x=35,y=280)
#liv=Label(text="light intensity",font=('Helvetica',18,'bold'),fg=w,bg=b)
global liv
liv=Button(text="ekefhbv",borderwidth=0,fg="white",bg="black",command=bfunc)
liv.place(x=150,y=280)
c2.grid(row=0,column=1)
cdt=Label(text='  ppm',font=('Helvetica',ts,'bold'),bg=w,fg=g)

#these images have to be downloded on RPI in order for the GUI to display them properly
cd= ImageTk.PhotoImage(Image.open(r"/home/pi/finale/co2newgui3.png")) #Location of file
c2.create_image(10,8,anchor=NW,image=cd)
cdt.place(x=270+px,y=64-p)
cov=Label(text='ppb',font=('Helvetica',ts,'bold'),bg=w,fg=g)
cov.place(x=270+50,y=64-p)
tp=ImageTk.PhotoImage(Image.open(r"/home/pi/finale/humiditynew.jpg"))#Location of file
c2.create_image(8,60,anchor=NW,image=tp)
t=Label(text="  'C",font=('Helvetica',ts,'bold'),bg=w,fg=g)
t.place(x=270+px,y=192-p)
tv=Label(text="'C",font=('Helvetica',ts,'bold'),bg=w,fg=g)
tv.place(x=270+50,y=192-p)
hm=ImageTk.PhotoImage(Image.open(r"/home/pi/finale/tempnewgui.jpg"))#Location of file
c2.create_image(10,125,anchor=NW,image=hm)
h=Label(text='  ppb',font=('Helvetica',ts,'bold'),bg=w,fg=g)
h.place(x=270+px,y=256-p)
vov=Label(text='ppb',font=('Helvetica',ts,'bold'),bg=w,fg=g)
vov.place(x=270+50,y=256-p)
voc=ImageTk.PhotoImage(Image.open(r"/home/pi/finale/vocnew.jpg"))#Location of file
c2.create_image(10,200,anchor=NW,image=voc)
v=Label(text='  ppm',font=('Helvetica',ts,'bold'),bg=w,fg=g)
v.place(x=270+px,y=320-p)
pmv=Label(text='ppm',font=('Helvetica',ts,'bold'),bg=w,fg=g)
pmv.place(x=270+50,y=320-p)
pm=ImageTk.PhotoImage(Image.open("/home/pi/finale/pmnew.png"))#Location of file
c2.create_image(10,265,anchor=NW,image=pm)
pmt=Label(text='  %',font=('Helvetica',ts,'bold'),bg=w,fg=g)
pmt.place(x=270+px,y=128-p)
hv=Label(text='%',font=('Helvetica',ts,'bold'),bg=w,fg=g)
hv.place(x=270+50,y=128-p)

#Configurating access to the firebase account
#Make sure the device is connected to a WiFi network named "iPhone" with password "parth2222" (without quotes)
config = {
  "apiKey": "AIzaSyCBMoMS-zz_Ji0sJ169IysHVqH8bVHHWs8",
  "authDomain": "smart-home-db-80bd0.firebaseapp.com",
  "databaseURL": "https://smart-home-db-80bd0-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "smart-home-db-80bd0.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db=firebase.database()

ad=serial.Serial('/dev/ttyUSB0',9600,timeout=1) #reding serial data from the ESP8266
while 1:
	try:
		inp=ad.readline().decode('ascii')
		print(inp)
		arr=(inp.strip()).split("@")
		
		if (len(arr)>1): #Used to eliminate redundencies at first run of the code
			print ("CO2:"+arr[0])
			db.child("sensors").child("Co2 Level").update({"0":arr[0]})
			if (int(arr[1])<101): #used to eliminate unsuitable values
				print ("Humidity:"+arr[1])
				db.child("sensors").child("Humidity").update({"0":arr[1]})
				hv.config(text=arr[1])
		
			print ("PM2.5"+arr[2])
			db.child("sensors").child("Particulate matter").update({"0":arr[2]})
			
			if(int(arr[3])<101): #used to eliminate unsuitable values
				print ("Temp:"+arr[3])
				db.child("sensors").child("Temperature").update({"0":arr[3]})
				tv.config(text=arr[3])
			print ("VOC:"+arr[4])
			db.child("sensors").child("Volatile Compounds").update({"0":arr[4]})
			print ()
			dn=datetime.today().weekday()
			ti = datetime.now()
			tme = time.localtime()
			ct = time.strftime("%H:%M", tme)
			mn=calendar.month_name[ti.month]
			hur.config(text=ct)
			mo.config(text="Friday"+","+mn+" "+str(ti.day)+","+str(ti.year))
			cov.config(text=arr[0])
			pmv.config(text=arr[2])
			vov.config(text=arr[4])
			tmplight=0
			tmplight= 1024-int(arr[5])
			tl=str(tmplight)
			liv.config(text=tl,bg="black",fg="white")
			db.child("sensors").child("Light Intensity").update({"0":tl})
			AQI.config(text=arr[2])
			tk.update()
		time.sleep(2)
	except:
		continue
tk.mainloop()
