import datetime
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import sqlite3
from tkcalendar import Calendar

root = tk.Tk()

#<----↓----初起動時の動作---↓---＞
def initialize_database():
    """アプリケーション起動時にデータベース接続を確立し、テーブルがなければ作成する"""
    global conn,tree
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            due_date TEXT NOT NULL,
            created_date TEXT NOT NULL
            )
        ''')
    conn.commit()
#<---↑----初起動時の動作----↑---＞
0

#<----↓----追加の動作---↓---＞
def add_menu():
    frame_s.pack()
    frame_list.pack_forget()
    frame_delete.pack_forget()
    t_year = datetime.datetime.year
    t_month = datetime.datetime.month
    t_day= datetime.datetime.day
    entry_year.set(t_year)
    entry_month.set(t_month)
    entry_day.set(t_day)

def date_select_calender(event):
    select_d_str=calen.get_date()
    print(select_d_str)
    select_y,select_m,select_d = select_d_str.split("/")
    set_data(select_y,select_m,select_d)

def set_data(y=datetime.date.today().year,m=datetime.date.today().month,d=datetime.date.today().day):
    entry_year.set(y)
    entry_month.set(m)
    entry_day.set(d)

def add():
    task=entry_sj.get().strip()
    year=entry_year.get().strip()
    month=entry_month.get().strip()
    day=entry_day.get().strip()
    date=datetime.datetime.strptime(f"{year}/{month}/{day}",'%Y/%m/%d').date()
    created_date=datetime.datetime.now().date()
    if date<created_date:
        tkinter.messagebox.showerror("日付の入力","期限の入力が不正です。")
    else:
        try:
            conn.execute("INSERT INTO todo (task,due_date,created_date) values(?,?,?)",(task, date.isoformat(), created_date.isoformat()))
            conn.commit()
        except:
            if conn:
                conn.rollback()
            tkinter.messagebox.showerror("タスク追加失敗", "失敗しました")
        else:
            entry_sj.delete(0, tk.END)
            entry_year.delete(0, tk.END)
            entry_month.set("01")
            entry_day.set("01")
            tkinter.messagebox.showinfo("タスク追加成功", "成功しました")
#<---↑----追加の動作----↑---＞

#<----↓---トップの動き----↓---＞
def top_menu():
    frame_s.pack_forget()
    frame_delete.pack_forget()
    frame_list.pack_forget()
#<------↑トップの動き↑------＞

#<---↓一覧表示の動き↓---＞
def display_list():
    frame_list.pack_forget()
    frame_s.pack_forget()
    frame_delete.pack_forget()
    frame_list.pack(expand=True, fill='both')
    set_data()

    sort()
def sort():
    
    # Treeviewの既存データをすべてクリア
    for item in tree.get_children():
        tree.delete(item)
    sort_option = serect_sort.get()
    query = "SELECT id, task, due_date FROM todo" 
    if sort_option == "期日が近い":
        query += " ORDER BY due_date ASC" # 期日が近い順はASCが正しい
    elif sort_option == "期日が遠い":
        query += " ORDER BY due_date DESC"
    else:
        query += " ORDER BY due_date ASC" 
    try:
        cur = conn.execute(query)
        i=0
        for row in cur.fetchall():
            i+=1
            tree.insert("", "end",iid=row[0],values=(i,row[1], row[2]))
    except sqlite3.Error as e:
        tkinter.messagebox.showerror("データ取得エラー", f"データベースからのデータ取得に失敗しました: {e}")
#<---↑一覧表示の動き↑---＞

#<--↓-削除-↓-->
# def delete():
    
def delete_menu():
    display_list()
    frame_delete.pack()
    
def delete():
    select_i = tree.selection()
    for i in select_i:
        record_id = i
    try:
        conn.execute("DELETE FROM todo WHERE id = ?", (record_id,))
        conn.commit()
    except:
        tkinter.messagebox.showerror("削除の失敗", f"削除できなかった")
        conn.rollback()
    else:
        tkinter.messagebox.showerror("削除成功", f"削除しました")
        display_list()
        frame_delete.pack()
#<↑--削除---↑>

#<---↓---見栄え---↓--->
root.title("python製 ToDoリスト")
root.minsize(height=400,width=410)
title = tk.Label(root,text="ToDoリスト")

all_frame = tk.Frame(root)
all_frame.pack()
#メニュー
frame_m = tk.Frame(all_frame)
frame_m.pack()
menu = tk.Label(frame_m,text="メニュー")
menu.grid(row=0,column=0,padx=0,pady=0)

btn1 = tk.Button(frame_m,text="トップ",command=top_menu)
btn1.grid(row=1,column=0,padx=5,pady=10)

btn2 = tk.Button(frame_m,text=u"追加",command=add_menu)
btn2.grid(row=1,column=1,padx=5,pady=10)

btn3 = tk.Button(frame_m,text=u"一覧表示",command=display_list)
btn3.grid(row=1,column=2,padx=5,pady=10)

btn4  = tk.Button(frame_m,text=u"削除",command=delete_menu)
btn4.grid(row=1,column=3,padx=5,pady=10)

#描画画面(メニューボタン押したら切り替わるように)

#トップ画面（今日の日付と今日期限のタスクがあれば表示）

#追加画面
frame_s = ttk.Frame(all_frame,padding=10)

sj = tk.Label(frame_s,text="内容",bg="pink")
sj.grid(row=0, column=1)

entry_sj = tk.Entry(frame_s)
entry_sj["width"] = 40
entry_sj.grid(row=1, column=1)

date = tk.Label(frame_s,text="期限",bg="pink")
date.grid(row=2, column=1)

frame_daytime = ttk.Frame(frame_s,padding=10)
frame_daytime.grid(row=3, column=1)

entry_year = ttk.Combobox(frame_daytime)
entry_year_val=list(map(str,range(2025,3000)))
entry_year_val.insert(0,"-")
entry_year["width"] = 4
entry_year["values"]=entry_year_val
entry_year.grid(row=0, column=1)

entry_month = ttk.Combobox(frame_daytime)
entry_month["width"] = 2
entry_month["values"]=("-","01","02","03","04","05","06","07","08","09","10","11","12")
entry_month.grid(row=0, column=2)

entry_day = ttk.Combobox(frame_daytime)
entry_day["width"] = 2
entry_day["values"]=("-","01","02","03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29","30","31")
entry_day.grid(row=0, column=3)

today_b = tk.Button(frame_daytime,text="今日",command=set_data)
today_b.grid(row=0, column=4)

calen = Calendar(frame_s,)
calen.bind("<<CalendarSelected>>",date_select_calender)
calen.grid(row=4,column=1,pady=0)


btn_add = tk.Button(frame_s,text="追加",command=add)
btn_add.grid(row=5, column=1,pady=5)

#リスト一覧表示
frame_list = ttk.Frame(all_frame, padding=10)

serect_sort = ttk.Combobox(frame_list)
serect_sort["values"] = ("---","期日が近い","期日が遠い")
serect_sort.current(0)
serect_sort.grid(row=0, column=0, pady=0, sticky="e")
sort_btn = tk.Button(frame_list,text="並び替え",command=sort)
sort_btn.grid(row=0, column=1, pady=0, sticky="e")

columns = ("num","task","kijitu")
tree = ttk.Treeview(frame_list,columns=columns,show="headings")
tree.heading("num",text="番号")
tree.heading("task",text="タスク")
tree.heading("kijitu",text="期日")
tree.column("num",width=60,anchor="center")
tree.column("task",width=150)
tree.column("kijitu",width=80,anchor="e")

scrollbar = ttk.Scrollbar(frame_list,orient="vertical",command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.grid(row=1,column=0,sticky="nsew")
scrollbar.grid(row=1,column=1,sticky="ns")
frame_list.grid_rowconfigure(0,weight=1)
frame_list.grid_columnconfigure(0,weight=1)

#削除画面
frame_delete = ttk.Frame(all_frame, padding=10)
# entry_num = tk.Entry(frame_delete)
# entry_num.grid(row=0, column=0, pady=0,sticky="e")
del_btn = tk.Button(frame_delete,text=u"削除",command=delete)
del_btn.grid(row=0, column=0, pady=0,sticky="e")
"""IDの情報自体はh画面には出てないけど持ってきてる、選択させて、その隠れたIDをもとにDBのほうはいじらせよう"""

initialize_database()
root.mainloop()
conn.close()