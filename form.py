
from os import error
from sqlite3.dbapi2 import connect
from tkinter import*
from tkinter import messagebox
import sqlite3
import tkinter  
from datetime import date


top=Tk()
top.title('Teacher Assistant ')
top.resizable(False, False)

months = [
    "Jan",
    "Feb",
    "Mar",
    'Apr',
    'May',
    'Jun',
    'Jul',
     'Aug',
     'Sep',
     'Oct',
     'Nov',
     'Dec',   
] 

dropvar = StringVar()
dropvar.set("أختر مجموعه")
def do(x):
    db.execute(f'create table if not exists "{dropvar.get()}" (id integer,name text , phone integer, gender text,homephone)')

w = OptionMenu(top, dropvar,*months,command=do )

w.grid(column=6,row=0)

lapelid=tkinter.Label(text='id').grid(column=0,row=0)
lapelname=tkinter.Label(text='الاسم').grid(column=0,row=1)
lapelimg=tkinter.Label(text='الشهاده').grid(column=0,row=3)
entryid=Entry(top)
entryid.grid(column=1,row=0)
entryname=Entry(top)
entryname.grid(column=1,row=1)
entryphone=Entry(top)
entryphone.grid(column=1,row=2)
entryhomephone=Entry(top)
entryhomephone.grid(column=1,row=3)
var1 = tkinter.IntVar()
var2 = tkinter.IntVar()
variable=StringVar(top)

db = sqlite3.connect("state.db")
cr=db.cursor()

def chick():
    cr.execute(f"select * from '{dropvar.get()}' where id='{entryid.get().strip()}' ")
    data=cr.fetchall()
    if len(data)==0:
        return False
    else:
        return True
        
def add():            
        iduser=entryid.get().strip()
        if chick() ==False and  iduser!="":
            cr.execute(f"alter table '{dropvar.get()}' add column  'attend{entryid.get()}' 'str'" )
            cr.execute(f"alter table '{dropvar.get()}' add column  'Mmoney{entryid.get()}' 'str'" )
            cr.execute(f"alter table '{dropvar.get()}' add column  'Bmoney{entryid.get()}' 'str'" )
            cr.execute(f"""insert into '{dropvar.get()}'(id,name , phone,homephone,'attend{entryid.get()}' , 'Mmoney{entryid.get()}','Bmoney{entryid.get()}') 
            values(
            '{str(iduser)}',
            
            '{str(entryname.get().capitalize().strip())}',
           
            '{str(entryphone.get().strip())}',
           
            '{str(entryhomephone.get().strip())}',
           
            'حضور:الطالب',
            
            'دفع:الشهر',

            'دفع:الكتب')""")
            db.commit()
            if var1.get()==1 and var2.get()==0:
                cr.execute(f"update {dropvar.get()} set gender = 'ولد' where id = '{entryid.get()}'")
            elif var2.get()==1 and var1.get()==0:
                cr.execute(f"update {dropvar.get()} set gender = 'بنت' where id = '{entryid.get()}'")
            else:
                cr.execute(f"update {dropvar.get()} set gender = 'لم يتم الادخال' where id = '{entryid.get()}'")
        else:
            show()

def gender():
    ge=''
    if var1.get() ==1 and var2.get()==0:
        ge='ولد' 
        cr.execute(f"update {dropvar.get()} set gender = '{ge}' where id = '{entryid.get()}'")
        db.commit()
    elif var2.get()==1 and var1.get()==0:
        ge='بنت'
        cr.execute(f"update {dropvar.get()} set gender = '{ge}' where id = '{entryid.get()}'")
        db.commit()
def show():
    statwindow=Toplevel( )
    s = entryid.get()
    cr.execute(f'select * from {dropvar.get()} where id="{s}"')
    result=cr.fetchall()
    cr.execute(f"select attend{entryid.get()} from {dropvar.get()}")
    atte=cr.fetchall()
    a=1
    backg=''
    for i in atte:
     if i[0] !=None :
        x=i[0].split(':')
        if x[1]=="حضور":
            backg='green'
        elif x[1]=="غياب":
            backg="red"
        else:
            backg='white'
        lblattend=Label(statwindow, bg=backg,width=16, text=f'{i[0]}' )
        lblattend.grid(row=a,column=3)
        a+=1
    cr.execute(f"select Mmoney{entryid.get()} from {dropvar.get()}")
    atte=cr.fetchall()
    a=1
    backg='snow'
    for i in atte:
     if i[0] !=None :
        lblattend=Label(statwindow, bg=backg, text=f'{i[0]}' )
        lblattend.grid(row=a,column=2)
        a+=1
    cr.execute(f"select Bmoney{entryid.get()} from {dropvar.get()}")
    atte=cr.fetchall()
    a=1
    backg='snow'
    for i in atte:
     if i[0] !=None :
        lblattend=Label(statwindow, bg=backg, text=f'{i[0]}' )
        lblattend.grid(row=a,column=1)
        a+=1
           
    phon=0
    nam=''
    gen=''
    homenum=0
    for row in result:
        nam=row[1]
        phon=row[2]
        gen=row[3]
        homenum=row[4]
    if nam!='':
        lblname=Label(statwindow,bg='green',height=3, width=15,text=f'الاسم: {nam} ')
        lblname.grid(row=0,column=3)
        lblhomephone=Label(statwindow,text=f'رقم المنزل: {homenum} ')
        lblhomephone.grid(row=0,column=2)
        lblphone=Label(statwindow,text=f'رقم الطالب:0{phon} ')
        lblphone.grid(row=0,column=1)
        lblgender=Label(statwindow,text=f'الجنس: {gen} ')
        lblgender.grid(row=0,column=0)
    else:
        messagebox.showerror('id not found ','id : غير صحيح')

def showall():
    s = entryid.get()
    cr.execute(f'select * from {dropvar.get()}')
    result=cr.fetchall()
    phon=0
    nam=''
    gen=''
    homenum=0   
    statwindow=Toplevel( )
    for row in range(len(result)+1) :
        nam=result[row][1]
        phon=result[row][2]
        gen=result[row][3]
        homenum=result[row][4]
        if nam!=None:    
            lblname=Label(statwindow,bg='green',height=5, width=15,text=f'الاسم: {nam} ')
            lblname.grid(row=row,column=3)
            lblhomephone=Label(statwindow,text=f'رقم المنزل: {homenum} ')
            lblhomephone.grid(row=row,column=2)
            lblphone=Label(statwindow,text=f'رقم الطالب:{phon} 0')
            lblphone.grid(row=row,column=1)
            lblgender=Label(statwindow,text=f'الحنس: {gen} ')
            lblgender.grid(row=row,column=0)

def nset():
    cr.execute(f"select id from {dropvar.get()} where name='{entryname.get().capitalize()}' ")
    data=cr.fetchall()
    id=0
    for row in data:
        id=row[0]
    if id!=0 and id!='':
      messagebox.showinfo(id,f'{id} ')
    else:
        messagebox.showinfo('id none','اسم غير موجود')

   
def phon():
    cr.execute(f"update {dropvar.get()} set phone = '{str(entryphone.get())}' where id = '{entryid.get()}'")
    db.commit()
def homephon():
    cr.execute(f"update {dropvar.get()} set homephone = '{str(entryhomephone.get())}' where id = '{entryid.get()}'")
    db.commit()
def attend():
    today = date.today()
    cr.execute(f"insert into '{dropvar.get()}'(attend{entryid.get()}) values('{today}:حضور')")
    db.commit()
def leave():  
    today = date.today()
    cr.execute(f"insert into '{dropvar.get()}'(attend{entryid.get()}) values('{today}:غياب')")
    db.commit()
def MonthMoney():
    today = date.today()
    cr.execute(f"insert into '{dropvar.get()}'(Mmoney{entryid.get()}) values('{today}: دفع الشهر ')")
    db.commit()
def BookMoney():  
    today = date.today()
    cr.execute(f"insert into '{dropvar.get()}'(Bmoney{entryid.get()}) values('{today}: دفع الملزمه ')")
    db.commit()
def clearall():
   cr.execute(f"delete from {dropvar.get()}")
   cr.execute(f'DROP column atend125')
   db.commit()


addbutton=tkinter.Button(text=' ادخال البيانات',command=add, width=30,bg='green' ,border=15).grid(column=1,row=7)
showbutton=tkinter.Button(text='عرض بيانات الطالب',command=show,width=19 ,bg='snow').grid(column=6,row=1)
idbutton=tkinter.Button(text=' id عرض',command=nset).grid(column=6,row=6,sticky=E)
phonebutton=tkinter.Button(text='رقم الطالب',command=phon).grid(column=0,row=2)
homephonebutton=tkinter.Button(text='رقم المنزل',command=homephon).grid(column=0,row=3)
showallbutton=tkinter.Button(text=' عرض بيانات المجموعه ', command=showall ,width=19 ,bg='snow').grid(column=6,row=2)
c=Checkbutton(top, text="ولد",variable=var1, onvalue=1, offvalue=0,command=gender)
c.grid(row=4, sticky=W)
c=Checkbutton(top, text="بنت",variable=var2, onvalue=1, offvalue=0,command=gender)
c.grid(row=4, column=1,sticky=W)
attendbutton=tkinter.Button(text='حضور',command=attend,width=16).grid(row=6,column=0 )
leavebutton=tkinter.Button(text='غياب',command=leave,width=15).grid(row=6,column=1)
leavebutton=tkinter.Button(text='الشهر',command=MonthMoney).grid(row=6,column=3)
leavebutton=tkinter.Button(text='الملزمه',command=BookMoney).grid(row=6,column=4)
clearbutton=tkinter.Button(text='clearall',command=clearall,width=15 ).grid(row=4,column=6,sticky=E)

top.mainloop()

  