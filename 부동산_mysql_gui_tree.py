# GUI를 활용한 부동산 가격 조회
from math import *
from tkinter import *
import tkinter.ttk as ttk
import pymysql

values = ['두정동', '백석동', '불당동', '성거읍', '성성동', '성정동', '성환읍', '신당동', '쌍용동', '와촌동', '입장면', '직산읍', '차암동']
space = 30

class Cont1:
    def __init__(self, frame):
        self.inframe = Frame(frame)
        self.inframe.pack(fill=X, anchor=N)
        
        # 읽기만 되는 combobox (쓰기 안됨)
        self.label1 = Label(self.inframe, width=5, text='읍면동')
        self.label1.pack(side=LEFT)
        self.readonly_combobox1 = ttk.Combobox(self.inframe, width=5, values=values, state='readonly')
        self.readonly_combobox1.current(0) # 0번째 인덱스값 선택
        self.readonly_combobox1.pack(side=LEFT)
        
        self.label2 = Label(self.inframe, width=10, text='금액(거래가)')
        self.label2.pack(side=LEFT)
        self.acount1 = Entry(self.inframe, width=10)
        self.acount1.insert(0, 0)
        self.acount1.pack(side=LEFT)
        self.label2 = Label(self.inframe, width=2, text='~')
        self.label2.pack(side=LEFT)
        self.acount2 = Entry(self.inframe, width=10)
        self.acount2.insert(0, 30000)
        self.acount2.pack(side=LEFT)
        
        self.label7 = Label(self.inframe, width=10, text='금액(월세)')
        self.label7.pack(side=LEFT)
        self.rent1 = Entry(self.inframe, width=10)
        self.rent1.insert(0, 0)
        self.rent1.pack(side=LEFT)
        self.label8 = Label(self.inframe, width=2, text='~')
        self.label8.pack(side=LEFT)
        self.rent2 = Entry(self.inframe, width=10)
        self.rent2.insert(0, 100)
        self.rent2.pack(side=LEFT)
        
        self.label3 = Label(self.inframe, width=10, text='면적(평)')
        self.label3.pack(side=LEFT)
        self.area1 = Entry(self.inframe, width=10)
        self.area1.insert(0, 0)
        self.area1.pack(side=LEFT)
        self.label4 = Label(self.inframe, width=2, text='~')
        self.label4.pack(side=LEFT)
        self.area2 = Entry(self.inframe, width=10)
        self.area2.insert(0, 100)
        self.area2.pack(side=LEFT)
        
        self.label5 = Label(self.inframe, width=5, text='층')
        self.label5.pack(side=LEFT)
        self.floor1 = Entry(self.inframe, width=10)
        self.floor1.insert(0, 0)
        self.floor1.pack(side=LEFT)
        self.label6 = Label(self.inframe, width=2, text='~')
        self.label6.pack(side=LEFT)
        self.floor2 = Entry(self.inframe, width=10)
        self.floor2.insert(0, 50)
        self.floor2.pack(side=LEFT)

class Cont2:
    def __init__(self, frame):
        global chkr, chkc, chkt, chksf, chkst
        self.inframe = Frame(frame)
        self.inframe.pack(fill=X, anchor=N)
        
        self.label = Label(self.inframe, width=8, text='날짜 (월)')
        self.label.pack(side=LEFT)
        self.month1 = Entry(self.inframe, width=10)
        self.month1.insert(0, 1)
        self.month1.pack(side=LEFT)
        self.label2 = Label(self.inframe, width=2, text='~')
        self.label2.pack(side=LEFT)
        self.month2 = Entry(self.inframe, width=10)
        self.month2.insert(0, 10)
        self.month2.pack(side=LEFT)

        self.chkbox1 = Checkbutton(self.inframe, text='매매', variable=chkt)
        self.chkbox1.select()
        self.chkbox1.pack(side=LEFT, padx=5, pady=10)
        
        self.chkbox2 = Checkbutton(self.inframe, text='전세', variable=chkc)
        self.chkbox2.pack(side=LEFT, padx=5, pady=10)
        
        self.chkbox3 = Checkbutton(self.inframe, text='월세', variable=chkr)
        self.chkbox3.pack(side=LEFT, padx=5, pady=10)
        
        self.rbtn1 = Radiobutton(self.inframe, text='역세권', value=1, variable=chkst)
        self.rbtn1.pack(side=LEFT, padx=5, pady=10)
        self.rbtn1.select()
        self.rbtn2 = Radiobutton(self.inframe, text='비역세권', value=2, variable=chkst)
        self.rbtn2.pack(side=LEFT, padx=5, pady=10)
        
        self.rbtn2 = Radiobutton(self.inframe, text='가격낮은순', value=2, variable=rcost)
        self.rbtn2.pack(side=RIGHT, padx=5, pady=10)
        self.rbtn1 = Radiobutton(self.inframe, text='가격높은순', value=1, variable=rcost)
        self.rbtn1.pack(side=RIGHT, padx=5, pady=10)
        self.rbtn1.select()
        
        self.btn1 = Button(self.inframe, width=10, text='조회', command=selectData)
        self.btn1.pack(side=RIGHT, padx=5, pady=10)

class Cont3:
    def __init__(self, frame):
        self.inframe = Frame(frame)
        self.inframe.pack(fill=X, anchor=N)
        
        self.btn1 = Button(self.inframe, width=10, text='최고가조회', command=search_acount_max)
        self.btn1.pack(side=LEFT, padx=5, pady=10)
        
        self.btn2 = Button(self.inframe, width=10, text='평균가조회', command=search_acount_avg)
        self.btn2.pack(side=LEFT, padx=5, pady=10)
        
        self.btn3 = Button(self.inframe, width=10, text='최저가조회', command=search_acount_min)
        self.btn3.pack(side=LEFT, padx=5, pady=10)
        
        self.btn4 = Button(self.inframe, width=25, text='거래량이 가장 많은 아파트', command=search_buy_max)
        self.btn4.pack(side=LEFT, padx=5, pady=10)
        
        self.btn5 = Button(self.inframe, width=25, text='거래량이 가장 적은 아파트', command=search_buy_min)
        self.btn5.pack(side=LEFT, padx=5, pady=10)

def deal(chk, s):
    if chk:
        return s
    return ''

def station(chk):
    if chk == 1:
        return "%역"
    return ''

def ordercost(chk):
    print(chk)
    if chk == 1:
        return 'DESC'
    return 'ASC'

def search_acount_max():
    global treelist
    dong = str(container1.readonly_combobox1.get())
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='estate', charset='utf8')

    cur = conn.cursor()
    
    sql = "SELECT dong, address, name, year, deal, area, MAX(acount), MAX(rent), month, floor, station_area  FROM all_view WHERE dong LIKE %s AND deal IN (%s, %s, %s) GROUP BY name, deal ORDER BY name"
    
    data = (dong + "%", deal(chkt.get(), '매매'), deal(chkc.get(), '전세'), deal(chkr.get(), '월세'))
    print(data)
    cur.execute(sql, data)
    
    # sql 데이터 추출
    row = cur.fetchall()
    
    # treeview 데이터 초기화
    treeview.delete(*treeview.get_children())
    
    # 튜플 형태의 데이터를 리스트로 만들어 면적을 평으로 바꿈
    treelist = [list(row[x]) for x in range(len(row))]
    for i in range(len(treelist)):
        treelist[i][5] = int(round(treelist[i][5]) / 3.3)
        treelist[i][8] = ''
        treelist[i][9] = ''
        
    # 표에 데이터 삽입0
    for i in range(len(treelist)):
        treeview.insert('', 'end', text=i+1, values=treelist[i])
    conn.close()
    
def search_acount_avg():
    global treelist
    dong = str(container1.readonly_combobox1.get())
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='estate', charset='utf8')

    cur = conn.cursor()
    
    sql = "SELECT dong, address, name, year, deal, area, AVG(acount), AVG(rent), month, floor, station_area  FROM all_view WHERE dong LIKE %s AND deal IN (%s, %s, %s) GROUP BY name, deal ORDER BY name"
    
    data = (dong + "%", deal(chkt.get(), '매매'), deal(chkc.get(), '전세'), deal(chkr.get(), '월세'))
    print(data)
    cur.execute(sql, data)
    
    # sql 데이터 추출
    row = cur.fetchall()
    
    # treeview 데이터 초기화
    treeview.delete(*treeview.get_children())
    
    # 튜플 형태의 데이터를 리스트로 만들어 면적을 평으로 바꿈
    treelist = [list(row[x]) for x in range(len(row))]
    for i in range(len(treelist)):
        treelist[i][5] = int(round(treelist[i][5]) / 3.3)
        treelist[i][6] = int(round(treelist[i][6]))
        treelist[i][7] = int(round(treelist[i][7]))
        treelist[i][8] = ''
        treelist[i][9] = ''
        
    # 표에 데이터 삽입
    for i in range(len(treelist)):
        treeview.insert('', 'end', text=i+1, values=treelist[i])
    conn.close()
    
def search_acount_min():
    global treelist
    dong = str(container1.readonly_combobox1.get())
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='estate', charset='utf8')

    cur = conn.cursor()
    
    sql = "SELECT dong, address, name, year, deal, area, MIN(acount), MIN(rent), month, floor, station_area  FROM all_view WHERE dong LIKE %s AND deal IN (%s, %s, %s) GROUP BY name, deal ORDER BY name"
    
    data = (dong + "%", deal(chkt.get(), '매매'), deal(chkc.get(), '전세'), deal(chkr.get(), '월세'))
    print(data)
    cur.execute(sql, data)
    
    # sql 데이터 추출
    row = cur.fetchall()
    
    # treeview 데이터 초기화
    treeview.delete(*treeview.get_children())
    
    # 튜플 형태의 데이터를 리스트로 만들어 면적을 평으로 바꿈
    treelist = [list(row[x]) for x in range(len(row))]
    for i in range(len(treelist)):
        treelist[i][5] = int(round(treelist[i][5]) / 3.3)
        treelist[i][8] = ''
        treelist[i][9] = ''
        
    # 표에 데이터 삽입
    for i in range(len(treelist)):
        treeview.insert('', 'end', text=i+1, values=treelist[i])
    conn.close()
    
def search_buy_max():
    global treelist
    dong = str(container1.readonly_combobox1.get())
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='estate', charset='utf8')

    cur = conn.cursor()
    
    sql = "SELECT dong, address, name, year, name, COUNT(name) FROM all_view  WHERE dong LIKE %s GROUP BY name ORDER BY COUNT(name) DESC LIMIT 1"
    
    data = (dong + "%")
    print(data)
    cur.execute(sql, data)
    
    # sql 데이터 추출
    row = cur.fetchall()
    
    # treeview 데이터 초기화
    treeview.delete(*treeview.get_children())
    
    # 튜플 형태의 데이터를 리스트로 만들어 면적을 평으로 바꿈
    treelist = [list(row[x]) for x in range(len(row))]
    for i in range(len(treelist)):
        treelist[i][4] = '통합'
        
    # 표에 데이터 삽입
    for i in range(len(treelist)):
        treeview.insert('', 'end', text=i+1, values=treelist[i])
    conn.close()
    
def search_buy_min():
    global treelist
    dong = str(container1.readonly_combobox1.get())
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='estate', charset='utf8')

    cur = conn.cursor()
    
    sql = "SELECT dong, address, name, year, name, COUNT(name) FROM all_view  WHERE dong LIKE %s GROUP BY name ORDER BY COUNT(name) LIMIT 1"
    
    data = (dong + "%")
    print(data)
    cur.execute(sql, data)
    
    # sql 데이터 추출
    row = cur.fetchall()
    
    # treeview 데이터 초기화
    treeview.delete(*treeview.get_children())
    
    # 튜플 형태의 데이터를 리스트로 만들어 면적을 평으로 바꿈
    treelist = [list(row[x]) for x in range(len(row))]
    for i in range(len(treelist)):
        treelist[i][4] = '통합'
        
    # 표에 데이터 삽입
    for i in range(len(treelist)):
        treeview.insert('', 'end', text=i+1, values=treelist[i])
    conn.close()

def selectData():
    global treelist
    dong = str(container1.readonly_combobox1.get())
    acount1 = str(container1.acount1.get())
    acount2 = str(container1.acount2.get())
    rent1 = str(container1.rent1.get())
    rent2 = str(container1.rent2.get())
    month1 = str(container2.month1.get())
    month2 = str(container2.month2.get())
    floor1 = str(container1.floor1.get())
    floor2 = str(container1.floor2.get())
    area1 = str(int(int(container1.area1.get()) * 3.3))
    area2 = str(int(int(container1.area2.get()) * 3.3))
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='estate', charset='utf8')

    cur = conn.cursor()
    
    sql = "SELECT * FROM all_view WHERE dong LIKE %s AND deal IN (%s, %s, %s) AND acount BETWEEN %s AND %s AND rent BETWEEN %s AND %s AND month BETWEEN %s AND %s AND floor BETWEEN %s AND %s AND area BETWEEN %s AND %s AND station_area LIKE %s ORDER BY acount"
    
    if rcost.get() == 1:
        sql += ' DESC'
    
    data = (dong + "%", deal(chkt.get(), '매매'), deal(chkc.get(), '전세'), deal(chkr.get(), '월세'), acount1, acount2, rent1, rent2, month1, month2, floor1, floor2, area1, area2, station(chkst.get()))
    print(data)
    cur.execute(sql, data)
    
    # sql 데이터 추출
    row = cur.fetchall()
    
    # treeview 데이터 초기화
    treeview.delete(*treeview.get_children())
    
    # 튜플 형태의 데이터를 리스트로 만들어 면적을 평으로 바꿈
    treelist = [list(row[x]) for x in range(len(row))]
    for i in range(len(treelist)):
        treelist[i][5] = int(round(treelist[i][5]) / 3.3)
        
    # 표에 데이터 삽입
    for i in range(len(treelist)):
        treeview.insert('', 'end', text=i+1, values=treelist[i])
    conn.close()

def tv():
    treeview.column("#0", width=50, anchor="center")
    treeview.heading("#0", text="번호")

    treeview.column("#1", width=100, anchor="center")
    treeview.heading("one", text="읍면동")

    treeview.column("#2", width=100, anchor="center")
    treeview.heading("two", text="주소", anchor="center")
    
    treeview.column("#3", width=200, anchor="center")
    treeview.heading("three", text="단지명", anchor="center")

    treeview.column("#4", width=100, anchor="center")
    treeview.heading("four", text="건축 연도", anchor="center")

    treeview.column("#5", width=100, anchor="center")
    treeview.heading("five", text="매매전월세", anchor="center")
    
    treeview.column("#6", width=50, anchor="center")
    treeview.heading("six", text="평 수", anchor="center")

    treeview.column("#7", width=50, anchor="center")
    treeview.heading("seven", text="금액", anchor="center")
    
    treeview.column("#8", width=50, anchor="center")
    treeview.heading("eight", text="월세", anchor="center")
    
    treeview.column("#9", width=50, anchor="center")
    treeview.heading("nine", text="계약 월", anchor="center")
    
    treeview.column("#10", width=50, anchor="center")
    treeview.heading("ten", text="계약 층", anchor="center")
    
    treeview.column("#11", width=100, anchor="center")
    treeview.heading("eleven", text="역", anchor="center")

root = Tk()
root.geometry('1100x500')
root.title('천안시 서북구 부동산 거래가 확인 프로그램')
root.resizable(False, False)

# 체크박스 값 저장 변수
chkt, chkc, chkr, chkst, chksf, rvy, rcost = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
testch = IntVar()
dong = ''

edtFrame = Frame(root)
edtFrame.pack()

# 위젯 틀
container1 = Cont1(edtFrame)
container2 = Cont2(edtFrame)
container3 = Cont3(edtFrame)

# 데이터 출력 틀
treeview = ttk.Treeview(root, columns=["one", "two","three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven"], 
                        displaycolumns=["one","two","three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven"])
treeview.pack(side = BOTTOM, fill=BOTH, expand=1)
tv()

root.mainloop()