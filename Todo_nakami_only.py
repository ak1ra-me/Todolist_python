import datetime

# class display:  クラスとか作るほどでもないかも、まとめたいなら自作関数調べてみようｂｙT 07/09

def load_tasks():
    global task_list
    task_list=[]

    with open("todo_itiran.csv","r",encoding="utf-8") as itiran:
        for read_line in itiran:
            line = read_line.strip().split(":")
            task_list.append(line)  
        unique_tasks_as_tuples = set(tuple(task) for task in task_list)
        task_list = [list(t) for t in unique_tasks_as_tuples]
        #日付順ソートしたいならfor文もう一回回す、うえで作ったlineりすとのline[1]をソートしたリストを作り直し、
        #for文でviewの形に直してprintしていく(データベース使うともっと楽らしい)7/15(7/17済)
        task_list.sort(key=lambda x:datetime.datetime.strptime(x[1], "%Y/%m/%d"))
        # task_list.reverse()
        for i,v in enumerate(task_list):
            name = v[0]
            deadline = v[1]
            view = f"{i+1}.{name}:{deadline}"
            print(view)
            #printは変数に代入できない！returnなしでこのdefは終了7/15
        return task_list
def save_tasks():
    with open("todo_itiran.csv","w",encoding="utf-8") as itiran:
        for task in task_list:
            itiran.write(f"{task[0]}:{task[1]}\n")
        
while True:
    print("タスクリスト")
    print("1.追加")
    print("2.一覧表示")
    print("3.削除")
    print("4.終了")
    print("実行する作業を選択してください")
    N = int(input("番号を選んでください")) 
    if N == 1:
        print("タスクを追加します")
        name = input("タスクを入力してください:")
        deadline_txt =input("yyyy/mm/dd:")
        try:
            deadline = datetime.datetime.strptime(deadline_txt,'%Y/%m/%d').date()
            task = [name,deadline.strftime('%Y/%m/%d')]
            # task_list.append(task)
            with open("todo_itiran.csv","a") as itiran:
                itiran.write(f"{task[0]}:{task[1]}\n")
            print("追加しました")
            print(f"{task[0]}:{task[1]}")
        except ValueError:
            print("入力方法を確認してください")
        else:
            continue 
    elif N == 2:
        print("一覧を表示します")
        load_tasks()
                # 辞書型じゃなくて多重リスト使うといいかもbyT←リストで保存から外部のエクセルファイル保存に改修しました、最終的にデータベース保存にする予定7/15
                # 多重リストから要素抜き出してる、最終的にname,deadlineを並べてprintしたい2025/07/07
        continue 
    elif N == 3:
        print("タスクを削除します")
        print("一覧を表示します")
        v = load_tasks()
        print("選んでください")
        try:
            remove_n = int(input())
            v.pop(remove_n-1)
        except ValueError:
            print("入力方法を確認してください")
        else:
            save_tasks()
            continue 
    #させたい動きはするようになった、N1のprint()みため要修正、数字インデックスを可変にする一覧表示は何度か使うのでクラス作ってみてもいいかも、try文も追加できるところしたい07/08
    elif N == 4:
        print("終了します")
        break
    else:
        print("エラーが起こりました")
        print("トップに戻る場合はtopと入力してください")
        t = input()
        if t=="top":
            print("トップに戻ります")
            continue
        else:
            print("終了します")
            break