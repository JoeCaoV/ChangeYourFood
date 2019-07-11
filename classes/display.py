"""Import the CONSTANTS Var containing the list of Categories"""
from config import CATEGORIES
from classes.database import Database
from tkinter import *
import math
import webbrowser

class Display:
    """This class will be used for any render"""
    def __init__(self):
        """Create the window with basic settings"""
        self.database = Database()
        self.window = Tk()
        self.window.title('ChangeYourFood')
        self.window.geometry('1080x720')
        self.window.minsize(480, 360)
        #self.window.iconbitmap('logo.ico')
        self.window.config(bg='#F7EEAF')
        menu_bar = Menu(self.window)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.window.quit)
        file_menu.add_command(label="Importer des produits", 
                              command=self.database.insert_products_from_api)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        self.window.config(menu=menu_bar)
        self.setFrames() 

    def setFrames(self):
        """Create the differents frame"""
        self.header_frame = Frame(self.window, bg='#F7EEAF')
        self.body_frame = Frame(self.window, bg='#F7EEAF')
        self.footer_frame = Frame(self.window, bg='#A7EEAF')

    def destroyFrames(self):
        """Destroy the frames"""
        self.header_frame.destroy()
        self.body_frame.destroy()
        self.footer_frame.destroy()

    def setPagination(self, products):
        self.pagination = Label(self.footer_frame, text='blue', bg='red', fg="#222923").grid(row=0)

    def home(self):
        """Home menu"""
        self.destroyFrames()
        self.setFrames()
        label_title = Label(self.header_frame, 
                            text="Bonjour, bienvenue sur ChangeYourFood",
                            font=("Courrier", 35), bg='#F7EEAF', fg="#222923")     
        action1 = Button(self.body_frame, text="Trouver un produit de substitution",
                         font=("Open Sans", 20), bg='#F7EEAF', fg="#222923",
                         command=self.find_select_category)
        action2 = Button(self.body_frame, text="Voir vos produits de substitution",
                         font=("Open Sans", 20), bg='#F7EEAF', fg="#222923")
        label_title.grid(row=0)
        action1.grid(row=1, column=0, padx=25)
        action2.grid(row=1, column=1, padx=25)
        self.header_frame.pack(pady=25)
        self.body_frame.pack(expand=YES)
        self.window.mainloop()
    
    def find_select_category(self):
        """Select category"""
        self.destroyFrames()
        self.setFrames()
        label_title = Label(self.header_frame, 
                            text="Selectionner une categorie",
                            font=("Courrier", 35), bg='#F7EEAF', fg="#222923")
        home_button = Button(self.header_frame, text="Retourner au menu principal",
                             font=("Courrier", 20), bg='#F7EEAF', fg="#222923",
                             command=self.home)
        for row, category in enumerate(CATEGORIES):
            Button(self.body_frame, text=category, font=("Open Sans", 20),
                   bg='#F7EEAF', fg="#222923", 
                   command= lambda: self.find_select_product(category[0], 1)
                   ).grid(row=math.floor(row/4), column=row%4, padx=25)
        label_title.grid(row=0)
        home_button.grid(row=1)
        self.header_frame.pack(pady=25)
        self.body_frame.pack(expand=YES)

    def find_select_product(self, category, page):
        self.destroyFrames()
        self.setFrames()
        label_title = Label(self.header_frame, 
                            text="Selectionner un produit",
                            font=("Courrier", 35), bg='#F7EEAF', fg="#222923")
        products = self.database.get_products_by_category(category, page)
        if products:
            for row, product in enumerate(products):
                Button(self.body_frame, text=product[1], font=("Open Sans", 15),
                       bg='#F7EEAF', fg="#222923",
                       ).grid(row=math.floor(row/2), column=row%2, padx=25)
        else:
            print('what')
            no_product_title = Label(self.header_frame,
                                     text="Aucun produit trouvé",
                                     font=('Courrier', 35), bg='#F7EEAF', fg="#222923"
                                     ).grid(row=0)
            home_button = Button(self.header_frame, text="Retourner au menu principal",
                                 font=("Courrier", 20), bg='#F7EEAF', fg="#222923",
                                 command=self.home).grid(row=1)
        self.header_frame.pack(pady=25)
        self.body_frame.pack(expand=YES)

