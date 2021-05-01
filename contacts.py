from tkinter import EXCEPTION, NoDefaultRoot, Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar, Scrollbar, Toplevel
from tkinter import ttk
import sqlite3  #for database connection


class Contacts:
    dbFilename = 'contacts.db' #variable that stores the database
    def __init__(self, root):
        self.root = root 
        # self.createLeftIcon()
        self.createGui()
        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=('helvetica', 10))
        ttk.style.configure("Treeview.Heading", font=('helvetica', 12, 'bold'))
        
    def createGui(self):
        self.createLabelFrame()
        self.createMessageArea()
        self.createTreeView()
        self.createScrollBar()
        self.createBottomButton()  
     
     #function that interacts with database   
    def executeDbQuery(self, query, parameters=()):
        with sqlite3.connect(self.dbFilename) as conn:
            print(conn)
            print('You have successfull connected to DB')
            cursor = conn.cursor()
            qureyResult = cursor.execute(query, parameters)
            conn.commit()
        return qureyResult
        
    
        
    # def createLeftIcon(self):
    #     photo = PhotoImage(file = 'icons/logo.png')
    #     label = Label(image = photo)
    #     label.image = photo
    #     label.grid(row=0, column=0)
        
    def createLabelFrame(self):
        labelframe = LabelFrame(self.root, text = "Create New Contact", bg = "sky blue", font = "helvetica 10")
        labelframe.grid(row=0, column=1, padx =8, pady=8, sticky='ew')
        Label(labelframe, text='Name: ', bg='green', fg = 'white').grid(row=1, column =1, sticky=W, pady=2, padx=15)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1, column=2, sticky=W, padx=5, pady=2)
        Label(labelframe, text='Email: ', bg='brown', fg = 'white').grid(row=2, column =1, sticky=W, pady=2, padx=15)
        
        self.emailfield = Entry(labelframe)
        self.emailfield.grid(row=2, column=2, sticky=W, padx=5, pady=2)
        Label(labelframe, text='Number : ', bg='black', fg = 'white').grid(row=3, column =1, sticky=W, pady=2, padx=15)
        
        self.numfield = Entry(labelframe)
        self.numfield.grid(row=3, column=2, sticky=W, padx=5, pady=2)
        Button(labelframe, text='Add Contact', command=2,bg = "blue", fg = 'white').grid(row=4, column =2, sticky=E, pady=2, padx=15)
        
        
        
    def createMessageArea(self):
        self.message = Label(text = '', fg='red')
        self.message.grid(row=3, column=1, sticky=W)
        
    def createTreeView(self):
        self.tree = ttk.Treeview(height =10, columns=("email", "number"), style='Treeview')
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading('#0', text='Name', anchor=W)
        self.tree.heading("email", text='Email Address', anchor=W)
        self.tree.heading("number", text = "Contact Number", anchor=W )
        
    #TODO: ScrollBar
    def createScrollBar(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=6, column=3, rowspan=10, sticky='sn')
        
        
    def createBottomButton(self):
        Button(text='Delete Selected', command="", bg="red", fg="white").grid(row=8, column=0, sticky=W, pady=10, padx=20)
        Button(text='Modify Selected', command="", bg="purple", fg="white").grid(row=8, column=2, sticky=W)
        
    def addnewContact(self):
        if self.newContactsValidated():
            query = "INSERT INTO contacts"            
            
    def newContactsValidate(self):
        return len(self.namefield.get()) !=0 and len(self.emailfield.get()) !=0 and len(self.numfield.get()) !=-0
    
        
if __name__ == '__main__':
    root=Tk()
    root.title('Contact List')
    application = Contacts(root)
    root.mainloop()
    