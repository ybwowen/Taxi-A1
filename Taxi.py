import csv
import random
import time

wordlist = []
currentlist = []
collections = []
num = 0
n = 0
level = ""
findindex = lambda self, i, value: sorted(self, key = lambda x:x[i] != value)[0]
    
def shuffleWords():
    global currentlist, num, n
    random.shuffle(currentlist)
    n = len(currentlist)
    num = 0

def initWordlist():
    global wordlist, level, collections
    csv_file = open("./Taxi! " + level + ".csv", encoding = "UTF-8", newline = "")
    csv_reader = csv.reader(csv_file)
    
    wordlist.clear()

    for word in csv_reader: 
        wordlist.append(word)

    csv_file.close()

    collections_file = open("Collections.txt", encoding = "UTF-8", newline = "")
    collections = collections_file.read().split()

def generateWordlist(status):
    global currentlist

    currentlist.clear()

    if status == "nouns_only":
        for word in wordlist:
            # print(word)
            if(word[1][0:2] == "n."):
                currentlist.append(word)
    elif status == "all_words": 
        for word in wordlist:
            # print(word)
            if(word[0] != "" and word[0] != " " and word[0][0:5] != "Leçon" and word[0] != "\ufeff词汇"):
                currentlist.append(word)
    elif status == "collections":
        for word in collections:
            currentlist.append(findindex(wordlist, 0, word))
            
    elif status[0:5] == "Leçon":
        flag = False
        lecon_idx = int(status[6:])
        for word in wordlist:
            if word[0] == "Leçon " + str(lecon_idx + 1):
                flag = False
                break
            if flag:
                currentlist.append(word)
            if word[0] == status:
                flag = True

    shuffleWords()

def savefile():
    global collections

    collections_file = open("Collections.txt", "w", encoding = "UTF-8", newline = "")
    for word in collections:
        collections_file.write(word + "\n")
    collections_file.close()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def getnumber(inputstr, minnum, maxnum):
    if not is_number(inputstr):
        print("无效操作，请根据提示输入" + str(minnum) + "-" + str(maxnum) + "中的一个数字。")
        time.sleep(1)
        return 0
    else:
        opt = int(inputstr)
        if opt < minnum or opt > maxnum:
            print("无效操作，请根据提示输入" + str(minnum) + "-" + str(maxnum) + "中的一个数字。")
            time.sleep(1)
            return 0
        else:
            return opt

def showWordlist():
    if len(currentlist) == 0:
        print("暂无单词！")
        time.sleep(1)
        return

    listlen = len(currentlist)

    while True:
        global num
        print("当前单词: " + currentlist[num][0])
        if currentlist[num][0] in collections:
            print("当前单词已收藏")
        else:
            print("当前单词未收藏")
        print("当前进度：" + str(num + 1) + "/" + str(listlen)) 
        print("1. 显示词性 2. 显示词义/用法 3. 显示变位/特殊阴阳性 4. 上一个单词 5. 下一个单词 6. 收藏单词 7. 取消收藏单词 8. 返回")

        while True:
            opt = getnumber(input(), 1, 8)

            if opt == 0:
                continue
            elif opt == 1:
                print(currentlist[num][1])
            elif opt == 2:
                print(currentlist[num][2])
            elif opt == 3:
                print(currentlist[num][3])
            elif opt == 4: 
                if num != 0:
                    num -= 1
                    break
                else: 
                    print("已经是第一个单词！")
            elif opt == 5:
                if num != n - 1:
                    num += 1
                    break
                else:
                    print("已经是最后一个单词！")
            elif opt == 6:
                if currentlist[num][0] in collections:
                    print("已经收藏了该单词！")
                else:
                    collections.append(currentlist[num][0])
                    print("收藏成功！")
            elif opt == 7:
                if currentlist[num][0] in collections:
                    collections.remove(currentlist[num][0])
                    print("取消收藏成功！")
                else:
                    print("暂未收藏该单词！")
            elif opt == 8:
                return

def checklecon():
    while True:
        if level == "A1":
            print("请输入查询第几课，支持第1-35课, 或者输入-1来返回")
            inputstr = input()
            if inputstr == "-1":
                return False
            lecon_idx = getnumber(inputstr, 1, 35)
            if lecon_idx == 0:
                continue
            else:
                return lecon_idx
        elif level == "A2":
            print("功能暂未开放，敬请期待！")
            

def mainPanel():
    while True:
        print("1. 查看所有单词 2. 查看所有名词 3. 查看收藏夹 4. 查询某一课的单词 5. 返回")
        opt = getnumber(input(), 1, 5)
        
        if opt == 0:
            continue
        if opt == 1:
            generateWordlist("all_words")
        elif opt == 2:
            generateWordlist("nouns_only")
        elif opt == 3:
            generateWordlist("collections")
        elif opt == 4:
            if(lecon_idx := checklecon()):
                generateWordlist("Leçon " + str(lecon_idx))
            else:
                continue

        if opt == 5:
            return
        else:
            showWordlist()

        savefile()

def chooselevel():
    global level
    while True:
        print("1. A1词汇 2. A2词汇（暂未开放） 3. 退出程序")
        opt = getnumber(input(), 1, 3)

        if opt == 1:
            level = "A1"
            initWordlist()
            mainPanel()
        elif opt == 2:
            level = "A2"
            print("暂未开放，敬请期待！")
            # initWordlist()
            # mainPanel()
        elif opt == 3:
            print("Bye~")
            time.sleep(1)
            exit(0)                

if __name__ == "__main__":
    print("Assistante de Vocabularie Français")
    print("Authored by ybw")
    time.sleep(1)

    chooselevel()