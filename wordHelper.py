from tkinter import *
import json
from difflib import get_close_matches
from tkinter import messagebox
import pyttsx3
import nltk
from nltk.corpus import wordnet
import streamlit as st

engine=pyttsx3.init()  #creating instance of engine class

voice=engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)

######   FUNCTIONALITY PART   ######

def search():
    data=json.load(open('images/data.json'))
    word=enterwordEntry.get()
    word=word.lower()
    close_match=get_close_matches(word, data.keys())[0]

#synonyms

    #for first match

    synonyms=[]
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())   
    result=[]
    for i in synonyms:
        if i not in result:
            result.append(i)

    #for close match

    synonyms=[]
    for syn in wordnet.synsets(close_match):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())   
    result3=[]
    for l in synonyms:
        if l not in result3:
            result3.append(l)
    
#antonyms

    #for first match

    antonyms=[]
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    result1=[]
    for j in antonyms:
        if j not in result1:
            result1.append(j)

    # for close match
     
    antonyms=[]
    for syn in wordnet.synsets(close_match):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    result2=[]
    for k in antonyms:
        if k not in result2:
            result2.append(k)

    # main search

    if word in data:
       meaning=data[word]
       textArea1.delete(1.0,END)
       textArea2.delete(1.0,END)
       textArea3.delete(1.0,END)
       for item in meaning:
            textArea1.insert(END,u'\u2022'+ item +'\n\n')
       for item1 in result1:
            textArea2.insert(END,u'\u2022'+ item1 +'\n\n') 
       for item2 in result:
            textArea3.insert(END,u'\u2022'+ item2 +'\n\n')    

    elif len(get_close_matches(word, data.keys()))>0:
        
        res=messagebox.askyesno('Confirm','Did you mean '+close_match+' instead?')

        if res==True:
            enterwordEntry.delete(0,END)
            enterwordEntry.insert(END, close_match)
            meaning=data[close_match]
            textArea1.delete(1.0,END)
            textArea2.delete(1.0,END)
            textArea3.delete(1.0,END)
            for item in meaning:
                textArea1.insert(END,u'\u2022'+ item +'\n\n')
            for item3 in result2:
                textArea2.insert(END,u'\u2022'+ item3 +'\n\n') 
            for item4 in result3:
                textArea3.insert(END,u'\u2022'+ item4 +'\n\n')  
        else:
            messagebox.showerror('Error','The word does not exist. Please double check it')
            enterwordEntry.delete(0,END)
            textArea1.delete(1.0,END)
            textArea2.delete(1.0,END)
            textArea3.delete(1.0,END)
    else:
        messagebox.showinfo('Information','The word does not exist')
        enterwordEntry.delete(0,END)
        textArea1.delete(1.0,END)
        textArea2.delete(1.0,END)
        textArea3.delete(1.0,END)  

def clear():
    enterwordEntry.delete(0,END)
    textArea1.delete(1.0,END)
    textArea2.delete(1.0,END)
    textArea3.delete(1.0,END) 

def iexit():
    res=messagebox.askyesno('Confirm','Do you want to Exit?')
    if res==True:
        root.destroy()
    else:
        pass

def wordaudio():
    engine.say(enterwordEntry.get())
    engine.runAndWait()

def meaningaudio():
    engine.say(textArea1.get(1.0,END))
    engine.runAndWait()

def antonymaudio():
    engine.say(textArea2.get(1.0,END))
    engine.runAndWait() 

def synonymaudio():
    engine.say(textArea3.get(1.0,END))
    engine.runAndWait()  


######   GUI PART   ######

root=Tk() #create window

root.geometry('1450x626+60+100')

root.title('Word Helper - The Audio Dictionary')

root.resizable(0,0) #no changes when maximized

root.configure(bg='white')
#background image

bgImage=PhotoImage(file='images/bg.png')
bgLabel=Label(root,image=bgImage,bd=0)
bgLabel.place(x=0,y=0)

#enter the word

enterWordLabel=Label(root,text='ENTER THE WORD',font=('Britannic Bold',25,'bold'),fg='red3',bg='whitesmoke')
enterWordLabel.place(x=630,y=20)

enterwordEntry=Entry(root,font=('arial',23,'bold'),justify=CENTER,bd=8,relief=GROOVE)
enterwordEntry.place(x=600,y=80)

#search

searchimage=PhotoImage(file='images/search.png')
searchButton=Button(root,image=searchimage,bd=0,bg='whitesmoke',cursor='hand2',activebackground='whitesmoke'
                ,command=search)
searchButton.place(x=700,y=150)

#mic

micimage=PhotoImage(file='images/mic.png')
micButton=Button(root,image=micimage,bd=0,bg='whitesmoke',cursor='hand2',activebackground='whitesmoke',command=wordaudio)
micButton.place(x=810,y=153)

#meaning

meaningLabel=Label(root,text='MEANING',font=('Britannic Bold',25,'bold'),fg='red3',bg='whitesmoke')
meaningLabel.place(x=170,y=240)

textArea1=Text(root,width=34, height=8,font=('arial',18,'bold'),bd=8,relief=GROOVE,wrap=WORD)
textArea1.place(x=30,y=300)

#microphone out
audioimage1=PhotoImage(file='images/microphone.png')
audioButton1=Button(root,image=audioimage1,bd=0,bg='whitesmoke',cursor='hand2',activebackground='whitesmoke',command=meaningaudio)
audioButton1.place(x=230,y=555)

audioimage2=PhotoImage(file='images/microphone.png')
audioButton2=Button(root,image=audioimage2,bd=0,bg='whitesmoke',cursor='hand2',activebackground='whitesmoke',command=antonymaudio)
audioButton2.place(x=680,y=555)

audioimage3=PhotoImage(file='images/microphone.png')
audioButton3=Button(root,image=audioimage3,bd=0,bg='whitesmoke',cursor='hand2',activebackground='whitesmoke',command=synonymaudio)
audioButton3.place(x=1160,y=555)

#clear

clearimage=PhotoImage(file='images/clear.png')
clearButton=Button(root,image=clearimage,bd=0,bg='whitesmoke',cursor='hand2',activebackground='whitesmoke',
            command=clear)
clearButton.place(x=1300,y=40)

#exit 

exitimage=PhotoImage(file='images/exit.png')
exitButton=Button(root,image=exitimage,bd=0,bg='whitesmoke',cursor='hand2',activebackground='whitesmoke',
                command=iexit)
exitButton.place(x=1300,y=150)

#antonym

antonymLabel=Label(root,text='ANTONYM',font=('Britannic Bold',25,'bold'),fg='red3',bg='whitesmoke')
antonymLabel.place(x=640,y=240)

textArea2=Text(root,width=34, height=8,font=('arial',18,'bold'),bd=8,relief=GROOVE)
textArea2.place(x=500,y=300)

#synonym

synonymLabel=Label(root,text='SYNONYM',font=('Britannic Bold',25,'bold'),fg='red3',bg='whitesmoke')
synonymLabel.place(x=1100,y=240)

textArea3=Text(root,width=34, height=8,font=('arial',18,'bold'),bd=8,relief=GROOVE)
textArea3.place(x=970,y=300)

#enter key

def enter_function(event):
    searchButton.invoke()

root.bind('<Return>',enter_function)


root.mainloop() 
