# Banking app v3
import json

class Datamanager():
    FILE_PATH = 'accounts.json'
    
    def __init__(self):
        self.accounts = self.load()
        
    def load(self):
        
        try:
          with open(self.FILE_PATH, 'r') as file:
            return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
           return {}
        
    def save(self):
        with open(self.FILE_PATH, 'w') as file:
            json.dump(self.accounts, file, indent=4)
        

class Bank_Actions:
    def __init__(self, data_manager, customer):
        self.data_manager = data_manager
        self.customer = customer
        

    def _get_current_account(self):
        name = self.customer.current_account
        if name is None:
            print("No account selected. Please choose an account first.")
            return None
        if name not in self.data_manager.accounts:
            print("Selected account no longer exists.")
            return None
        return self.data_manager.accounts[name]

    def deposit(self):
        acc = self._get_current_account()
        if acc is None:
            return
        try:
            amount = float(input('Enter deposit amount: '))
            if amount <= 0:
                print('Amount must be positive.')
                return
            acc['Balance'] += amount
            print(f'Deposited ${amount}. New balance: ${acc["Balance"]}')
            self.data_manager.save()
        except ValueError:
            print('Invalid input.')

    def withdraw(self):
        acc = self._get_current_account()
        if acc is None:
            return
        try:
            amount = float(input('Enter withdrawal amount: '))
            if amount <= 0:
                print('Amount must be positive.')
                return
            if amount > acc['Balance']:
                print('Insufficient funds.')
                return
            acc['Balance'] -= amount
            print(f'Withdrew ${amount}. New balance: ${acc["Balance"]}')
            self.data_manager.save()
        except ValueError:
            print('Invalid input.')

    def show_balance(self):
        acc = self._get_current_account()
        if acc is None:
            return
        print(f'Current balance: ${acc["Balance"]}')
    
class Customer():
    def __init__(self,data_manager,name = ''):
        self.name = name
        self.data_manager = data_manager
        self.current_account = None

    def add_account(self):
        name = input('Enter your new account name: ').strip()
        if not name:
            print("Name cannot be empty.")
            return

        if name in self.data_manager.accounts:
            print(f"Account named '{name}' already exists.")
            return

        try: 
            money = float(input('Please enter your balance: '))
            if money < 0:
                print("Balance cannot be negative.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return

    
        self.data_manager.accounts[name] = {
        'Balance': money,
        
    }

        self.data_manager.save()
        print(f"Account '{name}' was created")
        
        self.current_account = name
        print(f"Account selected: {name}")
        
    def choose_account(self):
        
        if self.data_manager.accounts:
            for name in self.data_manager.accounts:
                print(f'Accounts: {name}')
        else:
            print('There are no accounts to choose from')
             
        selection = input('Please select the account you would like to access, make sure to type account name as shown: ').strip()

        
        found = None
        selection_lower = selection.lower()
        for name in self.data_manager.accounts:
            if name.lower() == selection_lower:
                found = name
                break

        if found:
            self.current_account = found
            print(f"Account selected: {found}")
        else:
            print("Account not found.")
            self.current_account = None
        
    

        
def main():
    data_manager = Datamanager()
    customer = Customer(data_manager)
    account = Bank_Actions(data_manager, customer)

    while True:
        print('\nWelcome to the bank!')
        account_verification = input('Do you have an account ?(y/n): ').strip().lower()

        if account_verification == 'y':
            customer.choose_account()

        elif account_verification == 'n':
            create_account = input('Would you like to create an account ?(y/n): ').strip().lower()
            if create_account == 'y':
                customer.add_account()
            else:
                print('Thanks for banking!')
                break

        else:
            print('Please enter y or n')
            continue

        choice = input('1.deposit, 2.withdraw, 3.show_balance, 4.exit: ').strip()

        if choice == '1':
            account.deposit()
        elif choice == '2':
            account.withdraw()
        elif choice == '3':
            account.show_balance()
        elif choice == '4':
            print('Thanks for banking!')
            break
        else:
            print('Enter a valid option 1-4')
        

if __name__ == '__main__':
    main()