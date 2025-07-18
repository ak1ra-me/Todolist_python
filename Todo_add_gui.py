import datetime
import tkinter as tk
import tkinter.ttk as ttk

#メニューボタン押したときの動作
def add_menu():
    frame_s.pack()
def top_menu():
    frame_s.place_forget()
# def list_menu():

# def remove_menu():

root = tk.Tk()
root.title("python製 ToDoリスト")
root.minsize(height=400,width=410)

title = tk.Label(root,text="ToDoリスト")

#メニュー
frame_m = tk.Frame(root)
frame_m.pack(pady=10)
menu = tk.Label(frame_m,text="メニュー")
menu.grid(row=0,column=0,padx=0,pady=0)
btn1 = tk.Button(frame_m,text="トップ",command=top_menu)
btn1.grid(row=1,column=0,padx=5,pady=10)
btn2 = tk.Button(frame_m,text=u"追加",command=add_menu)
btn2.grid(row=1,column=1,padx=5,pady=10)
btn3 = tk.Button(frame_m,text=u"一覧表示")
btn3.grid(row=1,column=2,padx=5,pady=10)
btn4  = tk.Button(frame_m,text=u"削除")
btn4.grid(row=1,column=3,padx=5,pady=10)

#描画画面(メニューボタン押したら切り替わるように)
frame_s = tk.Frame(root)
sj = tk.Label(frame_s,text="内容")
sj.pack()
entry_sj = tk.Entry(frame_s)
entry_sj.pack()
date = tk.Label(frame_s,text="期限")
date.pack()
entry_year = tk.Entry(frame_s) 
entry_year.pack()
entry_month = ttk.Combobox(frame_s)
entry_month["values"]=("00","01","02","03","04","05","06","07","08","09","10","11","12")
entry_month.current(0)
entry_month.pack()
entry_day = ttk.Combobox(frame_s)
entry_day["values"]=("00","01","02","03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29","30","31")
entry_day.current(0)
entry_day.pack()
btn_add = tk.Button(frame_s,text="追加")
btn_add.pack()










root.mainloop()
