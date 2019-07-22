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
        self.bg_color = '#dbe6f0'
        self.configWindow()
        self.setFrames()

    def configWindow(self):
        """Create and set the main window"""
        self.window = Tk()
        self.window.title('ChangeYourFood')
        self.window.geometry('1080x720')
        self.window.minsize(480,360)
        self.window.config(bg=self.bg_color)
        menu_bar = Menu(self.window)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.window.quit)
        file_menu.add_command(label="Importer des produits", 
                              command=self.database.insert_products_from_api)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        self.window.config(menu=menu_bar)

    def setFrames(self):
        """Create the differents frames
        I'm configuring main window col and row to create a skeleton
        interface with header/body/footer
        """
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=10)
        self.window.rowconfigure(2, weight=1)
        self.header_frame = Frame(self.window, bg=self.bg_color)
        self.body_frame = Frame(self.window, bg='red')
        self.footer_frame = Frame(self.window, bg=self.bg_color)
        self.header_frame.grid(row=0)
        self.body_frame.grid(row=1, sticky='news')
        self.footer_frame.grid(row=2)

        self.footer_frame.rowconfigure(0, weight=1)
        self.footer_frame.columnconfigure(0, weight=5)
        self.footer_frame.columnconfigure(1, weight=1)
        self.footer_frame.columnconfigure(2, weight=5)
        self.footer_frame_left = Frame(self.footer_frame)
        self.footer_frame_center = Frame(self.footer_frame)
        self.footer_frame_right = Frame(self.footer_frame)
        self.footer_frame_left.grid(row=0, column=0, sticky='nesw')
        self.footer_frame_center.grid(row=0, column=1, sticky='nesw')
        self.footer_frame_right.grid(row=0, column=2, sticky='nesw')

    def destroyFrames(self):
        """Destroy the frames"""
        self.header_frame.destroy()
        self.body_frame.destroy()
        self.footer_frame.destroy()

    def setPagination(self, category, page):
        prev_page = Button(self.footer_frame_left, text='Précédente',
                           font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                           command= lambda: self.find_select_product(category, page - 1)
                           )
        pagination = Label(self.footer_frame_center, text='Page' + str(page), fg="#222923",
                           font=("Open Sans", 20),
                          )
        next_page = Button(self.footer_frame_right, text='Suivante',
                           font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                           command= lambda: self.find_select_product(category, page+1)
                          )
        if page > 1:
            prev_page.grid(row=0, column=0, sticky='nesw')
            pagination.grid(row=0, column=1, sticky='nesw')
            next_page.grid(row=0, column=2, sticky='nesw')
        elif page == 1:
            pagination.grid(row=0, column=1, sticky='nesw')
            next_page.grid(row=0, column=2, sticky='nesw')

    def setTitle(self, title):
        """Display the title of the page"""
        Label(self.header_frame, 
              text=title,
              font=("Courrier", 35), bg=self.bg_color, fg="#222923"
             ).grid(row=0)

    def setHomeReturn(self):
        """Display a button to come back to home menu"""
        Button(self.header_frame, text="Retourner au menu principal",
                             font=("Courrier", 20), bg=self.bg_color, fg="#222923",
                             command=self.home).grid(row=1)

    def home(self):
        """Home menu with 2 paths :
        FIND products : every method of this path will start with 'find'
        GET saved products : every method of this path will start with 'get'
        """
        self.destroyFrames()
        self.setFrames()
        self.setTitle('Bonjour, bienvenur sur ChangeYourFood')   
        find_path = Button(self.body_frame, text="Trouver un produit de substitution",
                         font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                         command=self.find_select_category)
        get_path = Button(self.body_frame, text="Voir vos produits de substitution",
                         font=("Open Sans", 20), bg=self.bg_color, fg="#222923")
        find_path.pack(expand=YES, side=LEFT)
        get_path.pack(expand=YES, side=LEFT)
        self.window.mainloop()
    
    def find_select_category(self):
        """Select category"""
        self.destroyFrames()
        self.setFrames()
        self.setTitle("Selectionner une categorie")
        self.setHomeReturn()
        content_frame = Frame(self.body_frame)
        content_frame.pack(expand=YES)
        for row, category in enumerate(CATEGORIES):
            Button(content_frame, text=category[0], font=("Open Sans", 20),
                   bg=self.bg_color, fg="#222923", 
                   command= lambda category=category[0]: self.find_select_product(category, 1)
                   ).grid(
                          row=math.floor(row/4), column=row%4,
                          padx=25, sticky='news'
                         )

    def find_select_product(self, category, page):
        """Select the product from the selected catory"""
        self.destroyFrames()
        self.setFrames()
        self.setTitle("Selectionner un produit")
        self.setHomeReturn()
        content_frame = Frame(self.body_frame)
        content_frame.pack(expand=YES)
        products = self.database.get_products_by_category(category, page)
        if products:
            for row, product in enumerate(products):
                Button(content_frame, text=product[1], font=("Open Sans", 15),
                       bg=self.bg_color, fg="#222923", wraplength=400,
                       command= lambda product = product: self.find_save_product(product)
                       ).grid(
                              row=math.floor(row/2), column=row%2,
                              padx=25, pady=15, sticky='ew'
                             )
            self.setPagination(category, page)
        else:
            no_product_title = Label(self.header_frame,
                                     text="Aucun produit trouvé",
                                     font=('Courrier', 35), bg=self.bg_color, fg="#222923"
                                     ).grid(row=0)
            home_button = Button(self.header_frame, text="Retourner au menu principal",
                                 font=("Courrier", 20), bg=self.bg_color, fg="#222923",
                                 command=self.home).grid(row=1)

    def find_save_product(self, product):
        """Show the selected product, and a alternative product for it"""
        self.destroyFrames()
        self.setFrames()
        self.setTitle('Voici le produit selectionné et son subsitut')
        self.setHomeReturn()
        alternative = self.database.get_best_alternative(product)
        product_frame = LabelFrame(self.body_frame, text=product[1], bg='green')
        product_frame.grid(row=0, column=0, sticky='nesw')
        product_info = Label(product_frame, text='test')
        product_info.pack(expand=YES, fill= BOTH)
        alternative_frame = LabelFrame(self.body_frame, text=product[1])
        alternative_frame.grid(row=0, column=1)
        alternative_info = Label(alternative_frame, text='test')
        alternative_info.pack(expand=YES, fill= BOTH)
        print(alternative)
