"""Import the CONSTANTS Var containing the list of Categories"""
import math
import requests
import tkinter as tk
import webbrowser

from config import CATEGORIES
from classes.database import Database
from PIL import Image, ImageTk

class Display:
    """This class will be used for any render"""
    def __init__(self):
        """Create the window with basic settings"""
        self.database = Database()
        self.bg_color = '#dbe6f0'
        self.config_window()
        self.set_frames()

    @staticmethod
    def open_url(url):
        """function that open the user's browser to the url"""
        webbrowser.open_new(url)

    @staticmethod
    def get_image(image_url):
        """to insert it into a canvas, we need to convert the wanted image
        into a tkimage Object
        """
        response = requests.get(image_url, stream=True)
        image = Image.open(response.raw)
        tkimage = ImageTk.PhotoImage(image)
        return tkimage

    def config_window(self):
        """Create and set the main window"""
        self.window = tk.Tk()
        self.window.title('ChangeYourFood')
        self.window.geometry('1080x720')
        self.window.minsize(480, 360)
        self.window.config(bg=self.bg_color)
        menu_bar = tk.Menu(self.window)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.window.quit)
        file_menu.add_command(label="Importer des produits",
                              command=self.database.insert_products_from_api)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        self.window.config(menu=menu_bar)

    def set_frames(self):
        """Create the differents frames
        I'm configuring main window col and row to create a skeleton
        interface with header/body/footer
        """
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=10)
        self.window.rowconfigure(2, weight=1)
        self.header_frame = tk.Frame(self.window, bg=self.bg_color, bd=2, relief='groove')
        self.body_frame = tk.Frame(self.window, bg=self.bg_color)
        self.footer_frame = tk.Frame(self.window, bg=self.bg_color)
        self.header_frame.grid(row=0, sticky='news')
        self.body_frame.grid(row=1, sticky='news')
        self.content_frame = tk.Frame(self.body_frame, bg=self.bg_color)
        self.content_frame.pack(expand='YES')
        self.footer_frame.grid(row=2)
        self.footer_frame.rowconfigure(0, weight=1)
        self.footer_frame.columnconfigure(0, weight=5)
        self.footer_frame.columnconfigure(1, weight=1)
        self.footer_frame.columnconfigure(2, weight=5)
        self.footer_frame_left = tk.Frame(self.footer_frame)
        self.footer_frame_center = tk.Frame(self.footer_frame)
        self.footer_frame_right = tk.Frame(self.footer_frame)
        self.footer_frame_left.grid(row=0, column=0, sticky='nesw')
        self.footer_frame_center.grid(row=0, column=1, sticky='nesw')
        self.footer_frame_right.grid(row=0, column=2, sticky='nesw')

    def destroy_frames(self):
        """Destroy the frames"""
        self.header_frame.destroy()
        self.body_frame.destroy()
        self.footer_frame.destroy()

    def set_pagination_product(self, category, page):
        """We need a pagination for the selected category for the products"""
        prev_page = tk.Button(self.footer_frame_left, text='Précédente',
                              font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                              command=lambda: self.find_select_product(category, page - 1)
                              )
        pagination = tk.Label(self.footer_frame_center, text='Page' + str(page), fg="#222923",
                              font=("Open Sans", 20),
                              )
        next_page = tk.Button(self.footer_frame_right, text='Suivante',
                              font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                              command=lambda: self.find_select_product(category, page+1)
                              )
        if page > 1:
            prev_page.grid(row=0, column=0, sticky='nesw')
            pagination.grid(row=0, column=1, sticky='nesw')
            next_page.grid(row=0, column=2, sticky='nesw')
        elif page == 1:
            pagination.grid(row=0, column=1, sticky='nesw')
            next_page.grid(row=0, column=2, sticky='nesw')

    def set_pagination_alternative(self, category, page):
        """We need a pagination for the selected category for the alternative"""
        prev_page = tk.Button(self.footer_frame_left, text='Précédente',
                              font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                              command=lambda: self.get_select_alternative(category, page - 1)
                              )
        pagination = tk.Label(self.footer_frame_center, text='Page' + str(page), fg="#222923",
                              font=("Open Sans", 20),
                              )
        next_page = tk.Button(self.footer_frame_right, text='Suivante',
                              font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                              command=lambda: self.get_select_alternative(category, page+1)
                              )
        if page > 1:
            prev_page.grid(row=0, column=0, sticky='nesw')
            pagination.grid(row=0, column=1, sticky='nesw')
            next_page.grid(row=0, column=2, sticky='nesw')
        elif page == 1:
            pagination.grid(row=0, column=1, sticky='nesw')
            next_page.grid(row=0, column=2, sticky='nesw')

    def set_title(self, title):
        """Display the title of the page"""
        tk.Label(self.header_frame,
                 text=title,
                 font=("Courrier", 25), bg=self.bg_color, fg="#222923"
                ).pack(expand='YES')

    def set_home_return(self):
        """Display a button to come back to home menu"""
        tk.Button(self.header_frame, text="Retourner au menu principal",
                  font=("Courrier", 20), bg=self.bg_color, fg="#222923",
                  command=self.home).pack(expand='YES')

    def home(self):
        """Home menu with 2 paths :
        FIND products : every method of this path will start with 'find'
        GET saved products : every method of this path will start with 'get'
        """
        self.destroy_frames()
        self.set_frames()
        self.set_title('Bonjour, bienvenue sur ChangeYourFood')
        find_path = tk.Button(self.content_frame, text="Trouver un produit de substitution",
                              font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                              command=self.find_select_category)
        get_path = tk.Button(self.content_frame, text="Voir vos produits de substitution",
                             font=("Open Sans", 20), bg=self.bg_color, fg="#222923",
                             command=self.get_select_category)
        find_path.grid(row=0, column=0, padx=15)
        get_path.grid(row=0, column=1, padx=15)
        self.window.mainloop()

    ######
    #FIND PATH METHODS
    ######

    def find_select_category(self):
        """Select category"""
        self.destroy_frames()
        self.set_frames()
        self.set_title("Selectionner une categorie")
        self.set_home_return()
        for row, category in enumerate(CATEGORIES):
            tk.Button(self.content_frame, text=category[0], font=("Open Sans", 20),
                      bg=self.bg_color, fg="#222923",
                      command=lambda category=category[0]: self.find_select_product(category, 1)
                      ).grid(row=math.floor(row/4), column=row%4,
                             padx=25, sticky='news')

    def find_select_product(self, category, page):
        """Select the product from the selected category"""
        self.destroy_frames()
        self.set_frames()
        self.set_title("Selectionner un produit")
        self.set_home_return()
        products = self.database.get_products_by_category(category, page)
        if products:
            for row, product in enumerate(products):
                tk.Button(self.content_frame, text=product[1], font=("Open Sans", 15),
                          bg=self.bg_color, fg="#222923", wraplength=400,
                          command=lambda product=product: self.find_save_product(product)
                          ).grid(row=math.floor(row/2), column=row%2,
                                 padx=25, pady=15, sticky='ew')
            self.set_pagination_product(category, page)
        else:
            tk.Label(self.content_frame,
                     text="Aucun produit trouvé",
                     font=('Courrier', 35), bg=self.bg_color, fg="#222923"
                    ).grid(row=0)
            tk.Button(self.content_frame, text="Retourner au menu principal",
                      font=("Courrier", 20), bg=self.bg_color, fg="#222923",
                      command=self.home
                      ).grid(row=1)

    def find_save_product(self, product):
        """Show the selected product, and a alternative product for it"""
        self.destroy_frames()
        self.set_frames()
        self.set_title('Voici le produit selectionné et son subsitut')
        self.set_home_return()
        alternative = self.database.get_best_alternative(product)
        if not alternative:
            tk.Label(self.content_frame, text='Ce produit est parfait, aucun subtitut trouvé',
                     bg=self.bg_color
                    ).pack(expand='YES')
        else:
            self.content_frame.destroy()
            self.set_product_frame(product)
            self.set_product_frame(alternative)
            self.save_button = tk.Button(self.footer_frame_center, text='Sauvegarder',
                                         bg=self.bg_color, font=('Open Sans', 18),
                                         command=lambda: self.save_product(alternative, product)
                                         )
            self.save_button.pack()

    def save_product(self, alternative, product):
        """When the user click to save the product, well, we do it
        return a positive message if it successed
        """
        self.save_button.destroy()
        data = (alternative[1], alternative[4], alternative[3],
                alternative[2], product[0])
        result = self.database.insert_alternative(data)
        if result:
            tk.Label(self.footer_frame_center, bg=self.bg_color, font=('Open Sans', 18),
                     text='Produit enregistré').pack()
        else:
            tk.Label(self.footer_frame_center, bg=self.bg_color, font=('Open Sans', 18),
                     text='Ce Produit est déjà enregistré').pack()



    def set_product_frame(self, product):
        """Display the product selected with his infos"""
        #Create the widget first
        product_frame = tk.LabelFrame(self.body_frame, text=product[1], bg=self.bg_color)
        product_name = tk.Label(product_frame,
                                text="Nom : " + str(product[1]),
                                bg=self.bg_color)
        product_nutriscore = tk.Label(product_frame,
                                      text='Nutriscore : ' + str(product[2]),
                                      bg=self.bg_color)
        product_url = tk.Label(product_frame, text='Lien vers la fiche OpenFoodFact',
                               cursor='hand2', bg=self.bg_color)
        product_image = tk.Canvas(product_frame, bg=self.bg_color,
                                  width=400, height=400)
        tkimage = self.get_image(product[3])
        product_image.create_image(200, 200, image=tkimage)
        product_image.image = tkimage
        #Display the widgets
        product_frame.pack(expand='YES', fill='both', side='left', padx=15)
        product_name.grid(row=0, column=0, sticky='W')
        product_nutriscore.grid(row=1, column=0, sticky='W')
        product_url.grid(row=2, column=0, sticky='W')
        product_image.grid(row=3, column=0, sticky='NESW')

        #Add a event to the Label to make it open the OFF url
        product_url.bind("<Button-1>", lambda e: self.open_url(product[4]))

    #######
    #GET PATH METHODS
    #######

    def get_select_category(self):
        """Display every categories containing saved product"""
        self.destroy_frames()
        self.set_frames()
        self.set_title("Selectionner une categorie")
        self.set_home_return()
        categories = self.database.get_saved_categories()
        if categories:
            for row, category in enumerate(categories):
                tk.Button(self.content_frame, text=category[1], font=("Open Sans", 20),
                          bg=self.bg_color, fg="#222923",
                          command=lambda category=category[1]: self.get_select_alternative(category, 1)
                          ).grid(row=math.floor(row/4), column=row%4,
                                 padx=25, sticky='news')
        else:
            tk.Label(self.content_frame, text='Aucun subsitut enregistré',
                     font=('Open Sans', 20), bg=self.bg_color).pack()

    def get_select_alternative(self, category, page):
        """Select the product from the selected category"""
        self.destroy_frames()
        self.set_frames()
        self.set_title("Selectionner un produit")
        self.set_home_return()
        products = self.database.get_alternatives_by_category(category, page)
        if products:
            for row, product in enumerate(products):
                tk.Button(self.content_frame, text=product[1], font=("Open Sans", 15),
                          bg=self.bg_color, fg="#222923", wraplength=400,
                          command=lambda product=product: self.get_saved_alternative(product)
                          ).grid(row=math.floor(row/2), column=row%2,
                                 padx=25, pady=15, sticky='ew')
            if products > 19:
                self.set_pagination_alternative(category, page)
        else:
            tk.Label(self.content_frame,
                     text="Aucun produit trouvé",
                     font=('Courrier', 35), bg=self.bg_color, fg="#222923"
                     ).grid(row=0)
            tk.Button(self.content_frame, text="Retourner au menu principal",
                      font=("Courrier", 20), bg=self.bg_color, fg="#222923",
                      command=self.home).grid(row=1)

    def get_saved_alternative(self, alternative):
        """Select the product from the selected category"""
        self.destroy_frames()
        self.set_frames()
        self.set_title("Voici votre produit de substitution")
        self.set_home_return()
        self.content_frame.destroy()
        self.set_product_frame(alternative)
