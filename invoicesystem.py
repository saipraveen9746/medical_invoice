from datetime import datetime
import mysql.connector


mydb = mysql.connector.connect(host="localhost", user="root", password="#######", port=3306)
my_cursor = mydb.cursor()
# my_cursor.execute("create database pharmacy")
my_cursor.execute("use pharmacy")
# my_cursor.execute("CREATE TABLE medicine (item_no INT, batch_number INT, brand_name VARCHAR(100), product_name VARCHAR(100) PRIMARY KEY, quantity INT, rate INT, gst INT, MRP INT, expiry_date DATE)")

class Purchase:
    def add_medicine(self):
        insert_query = "INSERT INTO medicine (item_no, batch_number, brand_name, product_name, quantity, rate, gst, MRP, expiry_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        batch_number = int(input("Enter the Batch code:"))
        brand_name = input("Enter the brand name:")
        product_name = input("Enter product name:").capitalize()
        quantity = int(input("Enter the quantity:"))
        rate = int(input("Enter the rate:"))
        gst = rate * 0.2
        MRP = gst + rate  # MRP is the sum of gst and rate
        expiry_date = input("Enter the Expiry date (yyyy-mm-dd):")

        max_item_no_query = "SELECT MAX(item_no) FROM medicine"
        my_cursor.execute(max_item_no_query)
        max_item_no = my_cursor.fetchone()[0]
        if max_item_no is None:
            max_item_no = 0
        item_no = max_item_no + 1

        data = (item_no, batch_number, brand_name, product_name, quantity, rate, gst, MRP, expiry_date)
        my_cursor.execute(insert_query, data)
        mydb.commit()
        print("Purchase added successfully")

    def show_medicine(self):
        select_query = "SELECT * FROM medicine ORDER BY item_no"  # Add ORDER BY clause
        my_cursor.execute(select_query)
        medicines = my_cursor.fetchall()

        if not medicines:
            print("No medicine records found.")
        else:
            print("Medicine records:")
            for medicine in medicines:
                print("Item No:", medicine[0])
                print("Batch Number:", medicine[1])
                print("Brand Name:", medicine[2])
                print("Product Name:", medicine[3])
                print("Quantity:", medicine[4])
                print("Rate:", medicine[5])
                print("GST:", medicine[6])
                print("MRP:", medicine[7])
                print("Expiry Date:", medicine[8])
                print("-----------------------")

    def edit_medicine(self):
            product_name = input("Enter the product name to edit: ").capitalize()
            select_query = "SELECT * FROM medicine WHERE product_name = %s"
            my_cursor.execute(select_query, (product_name,))
            medicine = my_cursor.fetchone()

            if medicine is None:
                print("Medicine not found.")
            else:
                print("Current Medicine Details:")
                print("Product Name:", medicine[3])
                print("Quantity:", medicine[4])
                print("Rate:", medicine[5])
                print("GST:", medicine[6])
                print("MRP:", medicine[7])
                print("Expiry Date:", medicine[8])
                print("-----------------------")

                quantity = int(input("Enter new quantity: "))
                rate = int(input("Enter new rate: "))
                gst = rate*0.2
                MRP = int(input("Enter new MRP: "))

                update_query = "UPDATE medicine SET quantity = %s, rate = %s, gst = %s, MRP = %s WHERE product_name = %s"
                new_data = (quantity, rate, gst, MRP, product_name)

                my_cursor.execute(update_query, new_data)
                mydb.commit()
                print("Medicine details updated successfully.")

    def find_expired_medicine(self):
        current_date = datetime.today().date()
        select_query = "SELECT * FROM medicine WHERE expiry_date < %s"
        my_cursor.execute(select_query, (current_date,))
        expired_medicines = my_cursor.fetchall()

        if not expired_medicines:
            print("No expired medicines found.")
        else:
            print("Expired Medicine records:")
            for medicine in expired_medicines:
                print("Product Name:", medicine[3])
                print("Expiry Date:", medicine[8])
                print("-----------------------")

    def show_stock(self):
            select_query = "SELECT product_name, quantity FROM medicine"
            my_cursor.execute(select_query)
            stock = my_cursor.fetchall()

            if not stock:
                print("No stock available.")
            else:
                print("Current Stock:")
                for item in stock:
                    print("Product Name:", item[0])
                    print("Quantity:", item[1])
                    print("-----------------------")

    def add_sales(self):
            product_name = input("Enter the product name sold: ").capitalize()
            quantity_sold = int(input("Enter the quantity sold: "))

            select_query = "SELECT quantity FROM medicine WHERE product_name = %s"
            my_cursor.execute(select_query, (product_name,))
            current_quantity = my_cursor.fetchone()

            if current_quantity is None:
                print("Product not found in stock.")
            elif quantity_sold > current_quantity[0]:
                print("Not enough stock available for the sale.")
            else:
                new_quantity = current_quantity[0] - quantity_sold
                update_query = "UPDATE medicine SET quantity = %s WHERE product_name = %s"
                new_data = (new_quantity, product_name)
                my_cursor.execute(update_query, new_data)
                mydb.commit()
                print("Sale recorded successfully.")

    def low_stock_reminder(self):
        select_query = "SELECT product_name, quantity FROM medicine WHERE quantity < 10"
        my_cursor.execute(select_query)
        low_stock_medicines = my_cursor.fetchall()

        if not low_stock_medicines:
            print("No medicines with low stock.")
        else:
            print("Low Stock Reminder:")
            for medicine in low_stock_medicines:
                print("Product Name:", medicine[0])
                print("Quantity:", medicine[1])
                print("-----------------------")

    def total_products(self):
            select_query = "SELECT SUM(quantity) FROM medicine"
            my_cursor.execute(select_query)
            total = my_cursor.fetchone()[0]

            print("Total number of products:", total)

        # ... (other methods)

    def delete_medicine(self):
        product_name = input("Enter the product name to delete: ").capitalize()
        select_query = "SELECT * FROM medicine WHERE product_name = %s"
        my_cursor.execute(select_query, (product_name,))
        medicine = my_cursor.fetchone()

        if medicine is None:
            print("Medicine not found.")
        else:
            print("Medicine Details:")
            print("Product Name:", medicine[3])
            print("Quantity:", medicine[4])
            print("Rate:", medicine[5])
            print("GST:", medicine[6])
            print("MRP:", medicine[7])
            print("Expiry Date:", medicine[8])
            print("-----------------------")

            confirm_delete = input("Are you sure you want to delete this medicine? (yes/no): ")
            if confirm_delete.lower() == 'yes':
                delete_query = "DELETE FROM medicine WHERE product_name = %s"
                my_cursor.execute(delete_query, (product_name,))
                mydb.commit()
                print("Medicine deleted successfully.")
            else:
                print("Medicine not deleted.")

    def main_menu(self):
        while True:
            print("1. Add Medicine")
            print("2. Show Medicine Records")
            print("3. Edit Medicine")
            print("4. Find Expired Medicine")
            print("5. Show Stock")
            print("6. Add Sales")
            print("7. Low Stock Reminder")
            print("8. Total Products")
            print("9. Delete Medicine")
            print("10. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_medicine()
            elif choice == '2':
                self.show_medicine()
            elif choice == '3':
                self.edit_medicine()
            elif choice == '4':
                self.find_expired_medicine()
            elif choice == '5':
                self.show_stock()
            elif choice == '6':
                self.add_sales()
            elif choice == '7':
                self.low_stock_reminder()
            elif choice == '8':
                self.total_products()
            elif choice == '9':
                self.delete_medicine()
            elif choice == '10':
                break
            else:
                print("Invalid choice. Please choose again.")

purchase_instance = Purchase()
purchase_instance.main_menu()


