import datetime
import re

class ConsumerManager:
    def __init__(self):
        self.consumers = self.load_consumers()
        self.bills = self.load_bills()

    def login(self):
        print("---- Login ----")
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        if username == "admin" and password == "admin123":
            self.admin_menu()
        elif username in self.consumers and password == self.consumers[username][1]:
            self.consumer_menu(username)
        else:
            print("Invalid username or password. Please try again.")
            self.login()

    def admin_menu(self):
        while True:
            print("\n---- Admin Menu ----")
            print("1. View Consumers")
            print("2. Update Consumer Details")
            print("3. Delete Consumer")
            print("4. Add Consumer")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_consumers()
            elif choice == "2":
                self.update_consumer()
            elif choice == "3":
                self.delete_consumer()
            elif choice == "4":
                self.add_consumer()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_consumer(self):
        print("\n---- Add Consumer ----")
        username = input("Enter username: ")
        if username in self.consumers:
            print("Username already exists. Please choose a different one.")
            return
        if not re.match("^[a-zA-Z0-9_]+$", username):
            print("Invalid username. Only alphanumeric characters and underscores are allowed.")
            return
        password = input("Enter password: ")
        name = input("Enter name: ")
        address = input("Enter address: ")
        self.consumers[username] = (username, password, name, address)
        self.save_consumers()
        print("Consumer added successfully.")

    def view_consumers(self):
        print("\n---- List of Consumers ----")
        for consumer in self.consumers.values():
            print("Username:", consumer[0])
            print("Name:", consumer[2])
            print("Address:", consumer[3])
            print("-------------------------")

    def update_consumer(self):
        print("\n---- Update Consumer ----")
        username = input("Enter username to update: ")
        if username in self.consumers:
            name = input("Enter updated name: ")
            address = input("Enter updated address: ")
            self.consumers[username] = (username, self.consumers[username][1], name, address)
            self.save_consumers()
            print("Consumer details updated successfully.")
        else:
            print("Consumer not found.")

    def delete_consumer(self):
        print("\n---- Delete Consumer ----")
        username = input("Enter username to delete: ")
        if username in self.consumers:
            del self.consumers[username]
            self.save_consumers()
            print("Consumer deleted successfully.")
        else:
            print("Consumer not found.")

    def consumer_menu(self, username):
        while True:
            print("\n---- Consumer Menu ----")
            print("1. View Price")
            print("2. Generate Bill")
            print("3. Check Usage")
            print("4. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_price()
            elif choice == "2":
                self.generate_bill(username)
            elif choice == "3":
                self.check_usage(username)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def view_price(self):
        print("\n---- Electricity Price ----")
        print("Price per unit: rs 7.00")

    def generate_bill(self, username):
        if username in self.consumers:
            try:
                usage = float(input("Enter usage in units: "))
                total = usage * 7.00
                print("Total Bill:", total)
                self.save_bill(username, total)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        else:
            print("Consumer not found.")

    def check_usage(self, username):
        if username in self.bills:
            print("\n---- Usage History ----")
            for bill in self.bills[username]:
                print("Date:", bill[0])
                print("Total Bill:", bill[1])
                print("-----------------------")
        else:
            print("No usage history found.")

    def save_bill(self, username, total):
        if username in self.bills:
            self.bills[username].append((self.get_current_date(), total))
        else:
            self.bills[username] = [(self.get_current_date(), total)]
        self.save_bills()

    def load_consumers(self):
        consumers = {}
        try:
            with open("consumers.txt", "r") as file:
                for line in file:
                    username, password, name, address = line.strip().split(",")
                    consumers[username] = (username, password, name, address)
        except FileNotFoundError:
            print("Consumers file not found. Starting with an empty list.")
        return consumers

    def save_consumers(self):
        with open("consumers.txt", "w") as file:
            for consumer in self.consumers.values():
                file.write(",".join(consumer) + "\n")

    def load_bills(self):
        bills = {}
        try:
            with open("bills.txt", "r") as file:
                for line in file:
                    username, date, total = line.strip().split(",")
                    if username in bills:
                        bills[username].append((date, float(total)))
                    else:
                        bills[username] = [(date, float(total))]
        except FileNotFoundError:
            print("Bills file not found. Starting with an empty list.")
        return bills

    def save_bills(self):
        with open("bills.txt", "w") as file:
            for username, bill_list in self.bills.items():
                for bill in bill_list:
                    file.write(username + "," + str(bill[0]) + "," + str(bill[1]) + "\n")

    @staticmethod
    def get_current_date():
        return datetime.datetime.now().strftime("%Y-%m-%d")

manager = ConsumerManager()
manager.login()
