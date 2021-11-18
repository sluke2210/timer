import tkinter as tk
from tkinter import ttk
from tkinter import *
# import time
# import datetime
# from datetime import date
import re
from datetime import *
from playsound import playsound
from threading import Thread
import os
#This dictionary will store the alarms
alarms = {}
listID = 0

# this is a function to get the selected list box value
def getListboxValue():
	itemSelected = listBoxOne.curselection()
	return itemSelected

# this is a function to check the status of the checkbox (1 means checked, and 0 means unchecked)
def getCheckbox1Value():
	checkedOrNot = cbVariable1.get()
	return checkedOrNot

# this is a function to check the status of the checkbox (1 means checked, and 0 means unchecked)
def getCheckbox2Value():
	checkedOrNot = cbVariable2.get()
	return checkedOrNot

# this is the function called when the button is clicked
def btnClickFunction():
	newAlarmPopup2()

#this function creaates a popup dialog
def newAlarmPopup():
	popup = tk.Toplevel()
	popup.wm_title("!")
	label = ttk.Label(popup, text=msg, font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
	B1.pack()
	popup.mainloop()

def alarmStartPopup(alarm_data):
	list_id, start_time, duration, msg ,passed= alarm_data;

	if getCheckbox1Value() == 1:
		playSound()

	def btnClickFunctionPopup():
		alarm_data[4] = 1;
		popup.destroy();
		main_loop();

	popup = tk.Toplevel()
	popup.wm_title("Time Complete")
	popup.geometry('800x400')

	popup.attributes('-alpha', 0.5)
	popup.attributes("-topmost", True)

	setNewBtn = Button(popup, text='Dismiss', bg='#F0F8FF', font=('arial', 24, 'normal'),
					   command=btnClickFunctionPopup)
	setNewBtn.place(x=350, y=200)
	popup.after(5000, btnClickFunctionPopup)
	label_txt= "Start: ", str(msg)
	popupLbl = Label(popup, text=label_txt, bg='#F0F8FF', font=('arial', 16, 'normal'))
	popup['bg']='#90ee90'
	popupLbl.place(x=300,y=100)
	popup.mainloop()


def playSound():
	#audio_file = os.path.dirname(__file__) + 'TF010.WAV'
	#playsound(audio_file)
	T = Thread(target=playsound, args=("TF010.WAV",))
	T.start();
	return



def alarmCompletePopup(alarm_data):
	list_id , start_time, duration, msg,passed = alarm_data;
	if getCheckbox1Value() == 1:
		playSound();

	def repopulateListView():
		#count=0;
		for key in alarms:
			list_id , start_time, duration, msg, passed = alarms[key];
			##alarms[key][0] = count;
			#count+=1;
			alarm_str=start_time.strftime("%H:%M"), "msg:",alarms[key][3],"\n"
			alarm_list.insert(END,alarm_str)



	def btnClickFunctionPopup():
		#alarm_list.delete(list_id);
		#alarm_list.clear()
		alarm_list.delete(0, END)
		del alarms[start_time]
		repopulateListView()
		popup.destroy();
		main_loop();

	def closePopup():
		#alarm_list.delete(list_id);
		#alarm_list.clear()
		alarm_list.delete(0, END)
		del alarms[start_time]
		repopulateListView()
		popup.destroy();
		main_loop();

	popup = tk.Toplevel()
	popup.wm_title("Time Complete")
	popup.geometry('800x400')

	popup.attributes('-alpha', 0.5)
	popup.attributes("-topmost", True)

	setNewBtn = Button(popup, text='Dismiss', bg='#F0F8FF', font=('arial', 30, 'normal'),
						   command=btnClickFunctionPopup)
	setNewBtn.place(x=350, y=200)
	label_txt= "End: ", str(msg)
	popupLbl = Label(popup, text=label_txt, bg='#F0F8FF', font=('arial', 16, 'normal'))
	popup['bg']='#ffcccb'
	popupLbl.place(x=300,y=100)
	popup.after(5000,btnClickFunctionPopup)
	popup.mainloop()

def has_started(alarm_data):
	list_id , start_time, duration, msg, passed = alarm_data;
	return start_time < datetime.now()

def has_finished(alarm_data):
	list_id , start_time, duration, msg, passed = alarm_data;
	end_time = start_time + timedelta(minutes=duration)
	return end_time < datetime.now()

def newAlarmPopup2():
	popup = tk.Toplevel()
	popup.wm_title("Create New")
	popup.geometry('300x300')
	def on_closing():
		popup.destroy();
		main_loop()
	popup.protocol("WM_DELETE_WINDOW", on_closing)

	def clearErrLable():
		errMsgLbl['text'] =''
	def checkStartTimeFromPopup(start_time):
		todatStr = now.strftime("%Y-%m-%d")
		try:
			datetime_obj = now.strptime(todatStr +" "+ start_time, '%Y-%m-%d %H:%M')
			return datetime_obj;
		except ValueError:
			return None;
		
	def checkDurationFromPopup(duration):
		mins = re.search('^\d+$',duration)
		hrsNmins = re.search('^\d:\d\d|^\d\d:\d\d',duration)
		if mins is not None:
			if int(mins.group(0)) < 1440:
				return int(mins.group(0));
		elif hrsNmins is not None:
			dura = hrsNmins.group(0).split(':')
			print(dura)
			if (int(dura[0])*60)+int(dura[1]) < 1440:
				return (int(dura[0])*60)+int(dura[1])
		else:
			return None;

	def btnClickFunctionPopup():
		global listID
		stime = checkStartTimeFromPopup(sTime.get());
		dtime = checkDurationFromPopup(iDuration.get());
		if sTime.get() == '' or iDuration.get() == '':
			print("time a duration needed")
			errMsgLbl['text'] = "Either Start time or Duration were blank"
			popup.after(2000, clearErrLable)
		elif stime is not None and dtime is not None:
			alarms[stime] = [listID,stime,dtime,tInput.get(), 0]
			alarm_str=stime.strftime("%H:%M"), "msg:",tInput.get(),"\n"
			alarm_list.insert(listID,alarm_str)
			listID += 1
			popup.destroy();
			main_loop()
		else:
			errMsgLbl['text'] = "Either Start time or Duration were incorectly formatted"
			popup.after(2000, clearErrLable)


	setNewBtn = Button(popup, text='Set', bg='#F0F8FF', font=('arial', 12, 'normal'), command=btnClickFunctionPopup)
	setNewBtn.place(x=140, y=260)
	tInput = Entry(popup)
	tInput.place(x=50, y=160)
	sTime = Entry(popup)
	sTime.place(x=50, y=40)
	iDuration = Entry(popup)
	iDuration.place(x=50, y=100)
	startTimeLbl=Label(popup, text='start time / HH:mm 24hr (09:30)', bg='#F0F8FF', font=('arial', 12, 'normal'))
	durationLbl=Label(popup, text='duration / mins or hrs:mins (1:20 or 80)', bg='#F0F8FF', font=('arial', 12, 'normal'))
	msgTxtLbl=Label(popup, text='reminder text', bg='#F0F8FF', font=('arial', 12, 'normal'))
	errMsgLbl=Label(popup, text='', bg='#F0F8FF', font=('arial', 10, 'normal'))
	startTimeLbl.place(x=35, y=10)
	durationLbl.place(x=35, y=70)
	msgTxtLbl.place(x=35, y=130)
	errMsgLbl.place(x=35, y=190)
	popup.mainloop()

root = Tk()
#this is the declaration of the variable associated with the checkbox
cbVariable1 = tk.IntVar()

#this is the declaration of the variable associated with the checkbox
cbVariable2 = tk.IntVar()

# This is the section of code which creates the main window
root.geometry('400x400')
root.configure(background='#F0F8FF')
root.title('Timey')

# This is the section of code which creates the a label
now = datetime.now()
time_text=now.strftime("%d/%m/%Y %A %H:%M:%S");
time_lbl =Label(root, text=time_text, bg='#F0F8FF', font=('arial', 14, 'normal'))
time_lbl.place(x=20, y=10)

# This is the section of code which creates a checkbox
CheckBoxOne=Checkbutton(root, text='Sound', variable=cbVariable1, bg='#F0F8FF', font=('arial', 12, 'normal'))
CheckBoxOne.place(x=20, y=40)

# This is the section of code which creates a checkbox
CheckBoxTwo=Checkbutton(root, text='Popup', variable=cbVariable2, bg='#F0F8FF', font=('arial', 12, 'normal'))
CheckBoxTwo.place(x=20, y=60)

# This is the section of code which creates a button
Button(root, text='Create new', bg='#F0F8FF', font=('arial', 12, 'normal'), command=btnClickFunction).place(x=250, y=40)

#This list box will hold show  alift of the currently set alarms
alarm_list = Listbox(root)
alarm_list.place(x=50,y=100 ,height=250, width=300)

sb = Scrollbar(alarm_list)
sb.pack(side=RIGHT, fill=Y);
sb.config(command=alarm_list.yview())
alarm_list.config(font = ("Courier New", 10), yscrollcommand = sb.set)

root.update()
def main_loop():
	while True:
		now = datetime.now()
		time_text = now.strftime("%A, %b (%d/%m/%Y)  %H:%M:%S");
		time_lbl.config(text=time_text)
		for key in alarms:
			if has_started(alarms[key]) and alarms[key][4] == 0:
				if getCheckbox2Value()==1:
					alarmStartPopup(alarms[key])
			if has_finished(alarms[key]):
				if getCheckbox2Value()==1:
					alarmCompletePopup(alarms[key])
		root.update()
main_loop();
root.mainloop()
