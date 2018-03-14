from tkinter import *
root=Tk()

vscrollbar = Scrollbar(root)

c= Canvas(root,background = "#D2D2D2",yscrollcommand=vscrollbar.set)

vscrollbar.config(command=c.yview)
vscrollbar.pack(side=LEFT, fill=Y)


f=Frame(c) #Create the frame which will hold the widgets

c.pack(side="left", fill="both", expand=True)
c.create_window(0,0,window=f, anchor='nw')

testcontentA = Label(f,wraplength=350 ,text=r"Det er en kendsgerning, at man bliver distraheret af læsbart indhold på en side, når man betragter dens websider, som stadig er på udviklingsstadiet. Der har været et utal af websider, som stadig er på udviklingsstadiet. Der har været et utal af variationer, som er opstået enten på grund af fejl og andre gange med vilje (som blandt andet et resultat af humor).")
testcontentB = Button(f,text="anytext")
testcontentA.pack()
testcontentB.pack()

# f.pack()
root.update()
c.config(scrollregion=c.bbox("all"))

root.mainloop()