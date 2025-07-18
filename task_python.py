# execution_n = list(range(1,5))
import datetime

def Todo_view():
            with open("todo_list.csv","r",encoding="utf-8") as itiran:
                for view in itiran: #関数task_jisyoからデータを引っ張るんじゃなく
                    # view = f"{n}.{de}"      #N1で入力→整形→一覧化したcsvファイルからでーたを取ってくる
                    return view
# print("タスクリスト")
# print("1.追加")
# print("2.一覧表示")
# print("3.削除")
# print("4.終了")
# print("実行する作業を選択してください")
# N = int(input("番号を選んでください"))
task_jisyo={}
# num = 1

# 辞書型じゃなくて多重リスト使うといいかもbyT
while True:
    print("タスクリスト")
    print("1.追加")
    print("2.一覧表示")
    print("3.削除")
    print("4.終了")
    print("実行する作業を選択してください")
    N = int(input("番号を選んでください:")) 
    if N == 1:
        print("タスクを追加します")
        name = input("タスクを入力してください:")
        deadline_txt =input("yyyy/mm/dd:")
        deadline = datetime.datetime.strptime(deadline_txt,'%Y/%m/%d')
        task_jisyo[num]= [name,deadline]
        ans = f"{num}.{name}:{deadline}\n"
        with open("todo_list.csv","a",encoding="utf-8") as itiran:
            itiran.write(ans)
        
        print(ans.replace("\n", ""))
        print("追加しました")
        num += 1
        continue  
    elif N == 2:
        print("一覧を表示します")        
        V = Todo_view()
        print(V)
        continue
    elif N == 3:
        print("タスクを削除します")
        continue
    else:
        print("終了します")
        break