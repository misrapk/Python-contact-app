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
        self.viewRecords()
     
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
        Button(labelframe, text='Add Contact', command= self.onAddContactClicked,bg = "blue", fg = 'white').grid(row=4, column =2, sticky=E, pady=2, padx=15)
        
        
        
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
        Button(text='Delete Selected', command=self.onDeleteButtonClicked, bg="red", fg="white").grid(row=8, column=0, sticky=W, pady=10, padx=20)
        Button(text='Modify Selected', command=self.onModifySelected, bg="purple", fg="white").grid(row=8, column=2, sticky=W)
    
    def onAddContactClicked(self):
        self.addnewContact()
        
    def onDeleteButtonClicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = "Please select atleast one contact to delete!"
            return 
        self.deleteRecords()
        
    def onModifySelected(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = "Nothing is selected to Modify"
            return 
        self.openModifyWindow()
      
    def addnewContact(self):
        if self.newContactsValidated():
            query = 'INSERT INTO contactList VALUES(NULL,?,?,?)'        
            parameters = (self.namefield.get(), self.emailfield.get(), self.numfield.get())
            self.executeDbQuery(query, parameters)
            
            #message after a contact is added
            self.message['text'] = "New Contact {} added".format(self.namefield.get())
            
            #checks that record is cleared before entring or not
            self.emailfield.delete(0, END) 
            self.namefield.delete(0, END)
            self.numfield.delete(0, END)
            self.viewRecords()
            
        else:
            self.message['text'] = "Fields can't be blank!"
            self.viewRecords()   #fuction that fetch record from db and display
            
            
    #this function checks if the input is enetered or not
    def newContactsValidated(self):
        return len(self.namefield.get()) !=0 and len(self.emailfield.get()) !=0 and len(self.numfield.get()) != 0
    
    
    #function to fetch the data from db and display
    def viewRecords(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
            
        query = 'SELECT * FROM contactList ORDER BY name desc'
        contactEntries = self.executeDbQuery(query)
        for row in contactEntries:
            #row 1 is name 2 is email and 3 is number
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3]))
        
    #TODO: function to delete Records
    def deleteRecords(self):
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contactList WHERE name = ?'
        self.executeDbQuery(query, (name,))
        self.message['text'] = 'Contacts for {} Succesfully Deleted!'.format(name)
        self.viewRecords()
        
    #TODO: function to modify the selected record
    #to open the window
    def openModifyWindow(self):
        name = self.tree.item(self.tree.selection())['text']
        oldNumber = self.tree.item(self.tree.selection())['values'][1]
        self.transient = Toplevel()
        self.transient.title("Update Contact")
        Label(self.transient, text = 'Name: ').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(self.transient, value = name), state = 'readonly').grid(row=0, column=2)
        Label(self.transient, text = 'Old Contact number: ').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(self.transient, value = oldNumber), state = 'readonly').grid(row=1, column=2)
        
        Label(self.transient, text = 'New phone Number:  ').grid(row=2, column=1)
        newPhoneEntryWidget =  Entry(self.transient)
        newPhoneEntryWidget.grid(row =2, column=2)
        
        # Button(labelframe, text='Add Contact', command= self.onAddContactClicked,bg = "blue", fg = 'white').grid(row=4, column =2, sticky=E, pady=2, padx=15)
        
        Button(self.transient, text = 'Update Contact', command=lambda: self.updateContact(
            newPhoneEntryWidget.get(), oldNumber, name
        ), bg = "blue",fg="white" ).grid(row=3, column=2, sticky=E)
        
        self.transient.mainloop()
        
    #function to update contact (query)
    def updateContact(self, newPhone, oldPhone, name):
        query = 'UPDATE contactList SET number = ? WHERE number =? AND name = ?'
        parameters = (newPhone, oldPhone, name)
        self.executeDbQuery(query, parameters)
        self.transient.destroy()
        self.message['text'] = 'Phone Number of {} is modified Successfull!'.format(name)
        self.viewRecords() 
        
        
    
        
if __name__ == '__main__':
    root=Tk()
    root.title('Contact List')
    root.geometry("650x450")
    root.resizable(width=False, height=False)
    application = Contacts(root)
    root.mainloop()
    