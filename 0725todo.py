import datetime
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import sqlite3
root = tk.Tk()

#<----↓----初起動時の動作---↓---＞
def initialize_database():
    """アプリケーション起動時にデータベース接続を確立し、テーブルがなければ作成する"""
    global conn
    global tree
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

#<----↓----追加の動作---↓---＞
def add_menu():
    frame_s.pack()
    frame_list.pack_forget()
def add():
    task=entry_sj.get().strip()
    year=entry_year.get().strip()
    month=entry_month.get().strip()
    day=entry_day.get().strip()
    date=datetime.datetime.strptime(f"{year}/{month}/{day}",'%Y/%m/%d').date()
    created_date=datetime.datetime.now().date()
    try:
        conn.execute("INSERT INTO todo (task,due_date,created_date) values(?,?,?)",(task, date.isoformat(), created_date.isoformat()))
        conn.commit()
    except:
        if conn:
            conn.rollback()
        tkinter.messagebox.showerror("タスクの追加", "失敗しました")
    else:
        entry_sj.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_month.set()
        entry_day.set()
        tkinter.messagebox.showinfo("タスクの追加", "成功しました")
#<---↑----追加の動作----↑---＞

#<----↓---トップの動き----↓---＞
def top_menu():
    frame_s.pack_forget()
    frame_list.pack_forget()
#<------↑トップの動き↑------＞

#<---↓一覧表示の動き↓---＞
def display_list():
    frame_list.pack_forget()
    frame_s.pack_forget()
    frame_list.pack(expand=True, fill='both')
    sort_option = serect_sort.get()

    # Treeviewの既存データをすべてクリア
    for item in tree.get_children():
        tree.delete(item)
    query = "SELECT id, task, due_date FROM todo" 
    if sort_option == "追加古い":
        query += " ORDER BY created_date ASC"
    elif sort_option == "新規追加順": 
                query += " ORDER BY id DESC"
    elif sort_option == "期日が近い":
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
            tree.insert("", "end", values=(i,row[1], row[2]))
    except sqlite3.Error as e:
        tkinter.messagebox.showerror("データ取得エラー", f"データベースからのデータ取得に失敗しました: {e}")


#<---↑一覧表示の動き↑---＞

#<---↓---見栄え---↓--->
root.title("python製 ToDoリスト")
root.minsize(height=400,width=410)
title = tk.Label(root,text="ToDoリスト")

all_frame = tk.Frame(root)
all_frame.pack()
#メニュー
frame_m = tk.Frame(all_frame)
frame_m.pack(pady=10)
menu = tk.Label(frame_m,text="メニュー")
menu.grid(row=0,column=0,padx=0,pady=0)

btn1 = tk.Button(frame_m,text="トップ",command=top_menu)
btn1.grid(row=1,column=0,padx=5,pady=10)

btn2 = tk.Button(frame_m,text=u"追加",command=add_menu)
btn2.grid(row=1,column=1,padx=5,pady=10)

btn3 = tk.Button(frame_m,text=u"一覧表示",command=display_list)
btn3.grid(row=1,column=2,padx=5,pady=10)

btn4  = tk.Button(frame_m,text=u"削除")
btn4.grid(row=1,column=3,padx=5,pady=10)

#描画画面(メニューボタン押したら切り替わるように)

#追加画面
frame_s = tk.Frame(all_frame)
sj = tk.Label(frame_s,text="内容")
sj.pack()
entry_sj = tk.Entry(frame_s)
entry_sj.pack()
date = tk.Label(frame_s,text="期限")
date.pack()
entry_year = tk.Entry(frame_s) 
entry_year.pack()
entry_month = ttk.Combobox(frame_s)
entry_month["values"]=("01","02","03","04","05","06","07","08","09","10","11","12")
entry_month.current(0)
entry_month.pack()
entry_day = ttk.Combobox(frame_s)
entry_day["values"]=("01","02","03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29","30","31")
entry_day.current(0)
entry_day.pack()
btn_add = tk.Button(frame_s,text="追加",command=add)
btn_add.pack()

#リスト一覧表示
frame_list = ttk.Frame(all_frame, padding=10)

serect_sort = ttk.Combobox(frame_list)
serect_sort["values"] = ("---","期日が近い","期日が遠い")
serect_sort.current(0)
serect_sort.grid(row=0, column=0, pady=0, sticky="e")
sort_btn = tk.Button(frame_list,text="並び替え",command=display_list)
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

initialize_database()
root.mainloop()
conn.close()