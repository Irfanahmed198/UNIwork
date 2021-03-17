from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3 as sql

# Gui class that contain window properties like title,size etc.
class GUI:  
    def __init__(self, arg):
        # Main Window Title, size
        self.center_window()
        root.title("Product list ")
        root.configure(bg='lightblue')
        root.resizable(0, 0)  # Stops window from being resizable
        # calling main window function
        main_design.Main_interface(self)

    def center_window(Self):
        width, height = 800, 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cord = int((screen_width / 2) - (width / 2))
        y_cord = int((screen_height / 2) - (height / 2))
        root.geometry("{}x{}+{}+{}".format(width,
                                           height,
                                           x_cord,
                                           y_cord))

# database function to execute queries
def DB_Con(query):
    con = sql.connect('reviews.db')
    cur = con.cursor()
    cur.execute(query)
    res=cur.fetchall()
    con.commit()
    con.close()
    return res
######################
# Review window GUI #
#####################
def open():
    root.withdraw()
    top = Toplevel()
    top.title("Customer Reviews")
    top.geometry("800x500")
    top.configure(bg='lightblue')
    lbl_font1 = font.Font(family='Verdana',
                          size='20',
                          weight='bold')

    global list_box   # global variable
    text_label1 = Label(top, text="Enter your review", font=("Arial", 14, "bold"), bg='lightblue', fg='White')
    text_label1.pack(side=TOP, anchor=CENTER, pady=3)
    revbox = Text(top, height=8, width=30)
    revbox.pack(side=TOP, anchor=CENTER, pady=3)

    revbutton = Button(top, text="Submit", font=("Arial", 11, "bold"),
                       command=lambda: reviews.add_reviews(None, revbox.get("1.0", END)))
    revbutton.pack(side=TOP, anchor=CENTER, pady=3)

    revlabel = Label(top, text="Reviews", font=("Arial", 14, "bold", 'italic'), bg='lightblue', fg='red')
    revlabel.pack()

    # listbox view with scroll bar
    my_frame = Frame(top)
    scrollbar = Scrollbar(my_frame, orient=VERTICAL)
    list_box = Listbox(my_frame, selectmode="multiple", height=12, width=60, yscrollcommand=scrollbar.set)
    scrollbar.config(command=list_box.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    list_box.pack()
    my_frame.pack(side=TOP, pady=10)

   # listbox view with scroll bar code end here
    ExitButton = Button(top, text="exit",
                      fg='darkred', bg='darkgrey',
                      cursor='arrow', font=('Arial', 11, 'bold'),
                      command=top.destroy)
    ExitButton.pack(side=BOTTOM, pady=5)
    # storing query of select reviews and show it in listbox
    review_query = 'Select * from Reviews'
    res = DB_Con(review_query)  # calling function to execute or get data from database
    for i in range(len(res)):
        # show in listbox
        list_box.insert(END, res[i][1])  #res[i][1] means get the review column data

    # minimize the main window 
    top.wait_window()
    root.deiconify()

#review class to insert reviews in database
class reviews():
    def add_reviews(self, data):
        # inserting review in listbox
        list_box.insert(END, data)
        # database connection and inserting data in database
        con = sql.connect('Reviews.db')
        cur = con.cursor()
        cur.execute("Insert into Reviews (r_no,review) Values (?,?);", (1, data))
        con.commit()
        con.close()
        messagebox.showinfo("Review", "Review Saved")





class product_details():
    def item_pics(self, ind):
        # opening the pics and saveing them in a list
        photo1 = Image.open('Toytruck.PNG')
        photo2 = Image.open('barbie.PNG')
        photo3 = Image.open('actionfigure.PNG')
        photo4 = Image.open('legoset.PNG')
        photo5 = Image.open('barbiedollhouse.PNG')
        photo6 = Image.open('batmancar.PNG')
        photo1 = photo1.resize((400, 250), Image.ANTIALIAS)
        product_images = [photo1, photo2, photo3, photo4, photo5, photo6]
        # for resizing all images into 400 W, 250 H
        global resized_images
        resized_images = []
        for i in range(0, len(product_images)):
            res = product_images[i].resize((400, 250), Image.ANTIALIAS)
            new_pic = ImageTk.PhotoImage(res)
            resized_images.insert(i, new_pic)
        return resized_images[ind]

    def item_name_price(self, name_indx, price_index):
        global items, desc1 # declare a global variable to access it in whole program
        #description of product store in a variable
        desc1 = '''
        This 15-inch large-scale truck 
        is hand-activated with realistic 
        sounds for loading, dumping and rolling.
        ​Push vehicle forward or pull 
        backward for realistic sounds.
        Push down the garbage lever to
        raise the trash bin and dump
        recycling in the truck—this 
        action activates sounds, too.
​        Press down on the horn above 
        the cab for even more sounds.
​        '''
        # second description
        desc2 = '''The latest line of Barbie 
        Fashionistas dolls includes different
        body types and a mix of skin tones, 
        eye colors, hair colors, hairstyles 
        and so many fashions inspired by 
        the latest trends!​
        Each Barbie doll wears a unique outfit
        that pops with her personality and style!
        Fun fashion accessories, like a cool 
        pair of shoes or a bracelet, complete 
        each look.
        '''
        # this list contain all the infomation about the products
        # (name, price, stock, description, category, index_position)
        items = [('Toy Truck', 'Price = £13', 10, desc1, 'Boys', 0), ('Barbie Doll', 'Price = £11', 5, desc2, 'Girls', 1),
            ('Action Figure', 'Price = £25', 2, desc1, 'Boys', 2), ('Lego Set', 'Price = £45', 3, desc1, 'Boys', 3),
               ("barbie house", 'Price = £69', 0, desc2, 'Girls', 4), ("action figure's car", 'Price = £35', 20, desc1, 'Boys', 5)]
        return items[name_indx][price_index]

    # function to view next product
    def forword(self, image_index):
        global Productphoto, Product_label, Product_price, index_item
        if image_index!=5 and Selected_cat.get() == 'Both': # checking index not the last position
            #updating the product info
            Productphoto.configure(image=resized_images[image_index+1])
            Product_label.config(text=product_details.item_name_price(self, index_item+1, 0))
            Product_price.config(text=product_details.item_name_price(self, index_item+1, 1))
            desc_label.config(text=product_details.item_name_price(self, index_item + 1, 3))
            # increasing the index
            index_item += 1
        elif image_index != 3 and Selected_cat.get() == 'Boys':
            # updating the product info
            Productphoto.configure(image=resized_images[items_boys[index_item+1][5]])
            Product_label.config(text=items_boys[index_item+1][0])
            Product_price.config(text=items_boys[index_item+1][1])
            desc_label.config(text=items_boys[index_item+1][3])
            # increasing the index
            index_item += 1
        elif image_index != 1 and Selected_cat.get() == 'Girls':
            # updating the product info
            Productphoto.configure(image=resized_images[items_girls[index_item+1][5]])
            Product_label.config(text=items_girls[index_item+1][0])
            Product_price.config(text=items_girls[index_item+1][1])
            desc_label.config(text=items_girls[index_item+1][3])
            # increasing the index
            index_item += 1
        else:
            messagebox.showwarning("Info", "This is the Last product")

    # previous btn function to move back in the product list
    def back(self, image_index):
        global Productphoto, Product_label, Product_price, index_item
        if image_index > 0 and Selected_cat.get() == 'Both':  # checking the index isn't in the first product
            # updating the product info
            Productphoto.configure(image=resized_images[image_index-1])
            Product_label.config(text=product_details.item_name_price(self, index_item - 1, 0))
            Product_price.config(text=product_details.item_name_price(self, index_item - 1, 1))
            desc_label.config(text=product_details.item_name_price(self, index_item - 1, 3))
            # descreasing the index of list items
            index_item -= 1
        elif image_index > 0 and Selected_cat.get() == 'Boys':
            # updating the product info
            Productphoto.configure(image=resized_images[items_boys[index_item-1][5]])
            Product_label.config(text=items_boys[index_item-1][0])
            Product_price.config(text=items_boys[index_item-1][1])
            desc_label.config(text=items_boys[index_item-1][3])
            # increasing the index
            index_item -= 1
        elif image_index > 0 and Selected_cat.get() == 'Girls':
            # updating the product info
            Productphoto.configure(image=resized_images[items_girls[index_item-1][5]])
            Product_label.config(text=items_girls[index_item-1][0])
            Product_price.config(text=items_girls[index_item-1][1])
            desc_label.config(text=items_girls[index_item-1][3])
            # increasing the index
            index_item -= 1
        else:
            messagebox.showwarning("Info", "Already in the first Product")

    # stock function to display stock
    def Stcok(self, index_stock):
        # getting stock qty from items list
        stock_qty = product_details.item_name_price(self, index_stock, 2)
        # if conditions
        if stock_qty < 20 and stock_qty > 0:
            msg = "Stock is Low remaining qty is " + str(stock_qty)
        elif stock_qty >= 20:
            msg = "Stock is Normal remaining qty is " + str(stock_qty)
        elif stock_qty <= 0:
            msg = "Out of Stock"
        # showing msg
        messagebox.showinfo("Stock Info", msg)

    # search function
    def search_item(self):
        # getting search field data
        search_value = Search_entry.get()
        cnt = 0  # cnt used to know search data founded or not
        # loop for compare all the list name with search name
        for i in range(0, len(items)):
            # if condition to check the search name match or not
            if search_value.upper() == items[i][0].upper() or search_value.upper() == items[i][0][0:len(search_value)].upper():
                cnt = 1
                # updating the pic and the labels of the product
                Productphoto.configure(image=resized_images[i])
                Product_label.config(text=product_details.item_name_price(self, i, 0))
                Product_price.config(text=product_details.item_name_price(self, i, 1))
                desc_label.config(text=product_details.item_name_price(self, i, 3))
                Selected_cat.current(0)
                break  # break the loop the search found
        if cnt == 0:
            # show message if search not found
            messagebox.showinfo("Information", "No item Found")

    # purchase function just to show the message
    def purchase_item(self):
        messagebox.showinfo("Purchase", "Item purchased")

    def select_list(self):
        global index_item
        var = Selected_cat.get()
        global items_boys, items_girls
        items_boys = []
        items_girls = []
        if var == 'Boys' or var == 'Girls':
            for i in range(len(items)):
                if items[i][4] == 'Boys':
                    items_boys.append(items[i])
                elif items[i][4] == 'Girls':
                    items_girls.append(items[i])
        print(items_boys)
        if var == 'Boys':
            index_item = 0
            Productphoto.configure(image=resized_images[items_boys[0][5]])
            Product_label.config(text=items_boys[0][0])
            Product_price.config(text=items_boys[0][1])
            desc_label.config(text=items_boys[0][3])
        if var == 'Girls':
            index_item = 0
            Productphoto.configure(image=resized_images[items_girls[0][5]])
            Product_label.config(text=items_girls[0][0])
            Product_price.config(text=items_girls[0][1])
            desc_label.config(text=items_girls[0][3])





################################
#Gui form or Main window desin #
################################

class main_design(product_details):
    def Main_interface(self):
        lbl_font = font.Font(family='Verdana',
                             size='20',
                             weight='bold')

        Title_label = Label(root, text='All About Toys Catalogue', font=lbl_font,
                        bg='lightblue', fg='White')
        Title_label.pack(side=LEFT, anchor=NW, padx=5)
        # global variables to access and update the values of product
        global Productphoto, Product_label, Product_price, index_item, Search_entry, desc_label, Selected_cat

        Search_button = Button(root, text='search', font=("Arial", 8, "bold"),
                               command=lambda: product_details.search_item(self)
                               )
        Search_button.pack(side=RIGHT, anchor=NE, padx=5, pady=10)

        Search_entry = Entry(root, width=20, font=("Arial", 13))
        Search_entry.pack(side=RIGHT, anchor=NE, padx=2, pady=10)

        Search_label = Label(root, text="Search", font=("Arial", 11, "bold"), bg='lightblue')
        Search_label.pack(side=RIGHT, anchor=NE, padx=2, pady=10)

        # frame for showing the product details
        Product_frame = LabelFrame(root, text="Product Detail", width=550, height=380, pady=10, padx=10,
                                 bg='lightblue', fg='White', font=('Arial', 16, "bold"))
        Product_frame.place(x=25, y=60)

        # category combobox and label
        Label(root, text='Categore', font=('Arial', 11, 'bold'), bg='lightblue').place(x=485, y=60)
        Selected_cat = ttk.Combobox(root, width=18, font=('Arial', '12'), justify='center', state="readonly")
        Selected_cat['values'] = ('Both', 'Boys', 'Girls')
        Selected_cat.current(0)
        Selected_cat.bind("<<ComboboxSelected>>", product_details.select_list)
        Selected_cat.place(x=555, y=60)

        # frame for showing the product description
        Product_description = LabelFrame(root, text="Description", width=270, height=373, pady=10, padx=10,
                                   bg='lightblue', fg='White', font=('Arial', 16, "bold"))
        Product_description.place(x=465, y=120)
        # description label
        desc_label = Label(Product_description, text=
                         """This 15-inch large-scale truck 
        is hand-activated with realistic 
        sounds for loading, dumping and rolling.
        ​Push vehicle forward or pull 
        backward for realistic sounds.
        Push down the garbage lever to
        raise the trash bin and dump
        recycling in the truck—this 
        action activates sounds, too.
​        Press down on the horn above 
        the cab for even more sounds.""", font=('Arial', 9, "bold"), bg='lightblue')
        desc_label.pack(side=LEFT, anchor=NW, padx=20)


        # create object of the class product_details
        details = product_details()

        Productphoto = Label(Product_frame, image=product_details.item_pics(None, 0), width=400, height=250)
        Productphoto.pack(side=TOP, anchor=CENTER)

        Product_label = Label(Product_frame, text=product_details.item_name_price(self, 0, 0), font=("Arial", 14, "bold", "italic"))
        Product_label.pack(side=LEFT, anchor=NW, pady=5)

        Product_price = Label(Product_frame, text=product_details.item_name_price(self, 0, 1), font=("arial", 14, "bold"))
        Product_price.pack(side=RIGHT, anchor=NE, pady=5)

        Label(Product_frame, text='', bg='lightblue').pack(side=TOP, pady=25)
        #inilize the items list to 0 index
        index_item = 0

        Previous_btn = Button(Product_frame, text="<< Previous", font=("arial", 12, "bold"),
                             command=lambda: product_details.back(self, index_item))
        Previous_btn.place(x=2, y=295)


        Next_btn = Button(Product_frame, text="Next >>", font=("arial", 12, "bold"),
                         command=lambda: product_details.forword(self, index_item))
        Next_btn.place(x=330, y=295)

        Stock_btn=Button(Product_frame, text="stock", font=("arial", 12, "bold"),
                         command=lambda: product_details.Stcok(self,index_item))
        Stock_btn.place(x=175, y=295)

        btnpurchase = Button(root, text="Purchase", font=("arial", 12, "bold"),
                             command=lambda: product_details.purchase_item(self))
        btnpurchase.place(x=42, y=450)
        btnreview = Button(root, text="Review Page", command=open, font=("arial", 12, "bold"))
        btnreview.place(x=328, y=450)


if __name__ == '__main__':
    review_table = "CREATE TABLE IF NOT EXISTS Reviews ( R_no number,Review VARCHAR2(200));"
    DB_Con(review_table)
    root = Tk()
    run = GUI(root)
    root.mainloop()
