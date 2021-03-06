import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('cred.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love-sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.

    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
  
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data
          


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)

def update_worksheet(data, worksheet):

    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    works_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def update_surplus_worksheet(new_surplus_data):

    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(new_surplus_data)
    
def calculate_surplus_data(sales_row):
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data



def get_last_5_entries_sales():
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    # print(column)
    columns = []
    for ind in range(1, 7):
        column  = sales.col_values(ind)
        columns.append(column[-5:])
    pprint(columns)

def main():

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus")

#main()
get_last_5_entries_sales()
