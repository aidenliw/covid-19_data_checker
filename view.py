
class View:

    # Page 1
    @staticmethod
    def main_page():
        print("+------------------------------------------------------+")
        print("| <<Welcome to Covid-19 Data Checker>>                  ")
        print("| (1) Search Global Data                                ")
        print("| (2) Search Canada Data                                ")
        print("| (0) Exit                                              ")
        print("+------------------------------------------------------+")
        option = input("Enter number to select an option: ")
        return int(option)

    # Page 2 from option 1
    @staticmethod
    def select_global_option():
        print("+------------------------------------------------------+")
        print("| (1) Search by Country Name                            ")
        print("| (2) Open Favourite List                               ")
        print("| (3) Return to Previous Page                           ")
        print("| (0) Exit                                              ")
        print("+------------------------------------------------------+")
        option = input("Enter number to select an option: ")
        return int(option)

    # Page 3 from option 1
    @staticmethod
    def set_global_location():
        print("+------------------------------------------------------+")
        print("| <<Search by Country Name>>                            ")
        print("| Enter the country full name below:                    ")
        print("| (Or Enter 0 to Exit)                                  ")
        print("+------------------------------------------------------+")
        country_name = input("Country Name: ")
        return country_name

    # Page 4 from option 1
    @staticmethod
    def set_global_date_range():
        print("+------------------------------------------------------+")
        print("| <<Set date range for the country to get a Plot view>> ")
        print("| Enter starting and ending date below:                 ")
        print("| (Format: YYYY-MM-DD E.g. 2022-07-01)                  ")
        print("| (Or Enter 1 to Display All Possible Data)             ")
        print("| (Or Enter 0 to Exit)                                  ")
        print("+------------------------------------------------------+")
        start_date = input("From (YYYY-MM-DD): ")
        end_date = input("To   (YYYY-MM-DD): ")
        return start_date, end_date

    # Page 2 from option 2
    @staticmethod
    def select_canada_option():
        print("+------------------------------------------------------+")
        print("| (1) Search by Province                                ")
        print("| (2) Open Favourite List                               ")
        print("| (3) Return to Previous Page                           ")
        print("| (0) Exit                                              ")
        print("+------------------------------------------------------+")
        option = input("Enter number to select an option: ")
        return int(option)

    # Page 3 from option 2
    @staticmethod
    def set_province_location():
        canada_provinces = {
            "AB": "Alberta",
            "BC": "British Columbia",
            "MB": "Manitoba",
            "NB": "New Brunswick",
            "NL": "Newfoundland and Labrador",
            "NT": "Northwest Territories",
            "NS": "Nova Scotia",
            "NU": "Nunavut",
            "ON": "Ontario",
            "PE": "Prince Edward Island",
            "QC": "Quebec",
            "SK": "Saskatchewan",
            "YT": "Yukon",
        }
        print("+------------------------------------------------------+")
        print("| <<Search by Province Abbreviation>>                   ")
        for abb in canada_provinces:
            print("| " + abb + ": " + canada_provinces[abb])
        print("| Enter the province's abbreviation below:              ")
        print("| (Or Enter 0 to Exit)                                  ")
        print("+------------------------------------------------------+")
        province_abb = input("Province Abbreviation (e.g. ON): ")
        return province_abb

    # Page 4 from option 2
    @staticmethod
    def set_province_date_range():
        print("+------------------------------------------------------+")
        print("| <<Set date range for the province to get a Plot view>>")
        print("| Enter starting and ending date below:                 ")
        print("| (Format: YYYY-MM-DD E.g. 2022-07-01)                  ")
        print("| (Or Enter 1 to Display All Possible Data)             ")
        print("| (Or Enter 0 to Exit)                                  ")
        print("+------------------------------------------------------+")
        start_date = input("From (YYYY-MM-DD): ")
        end_date = input("To   (YYYY-MM-DD): ")
        return start_date, end_date

    # Page 5
    @staticmethod
    def save_as_favourite():
        print("+------------------------------------------------------+")
        print("| Do you want to save this location?                    ")
        print("| (1) Yes                                               ")
        print("| (2) No                                                ")
        print("+------------------------------------------------------+")
        option = input("Enter number to select an option: ")
        return int(option)

    # Page 6
    @staticmethod
    def export_data():
        print("+------------------------------------------------------+")
        print("| Do you want to export the data into a text file?      ")
        print("| (1) Yes                                               ")
        print("| (2) No                                                ")
        print("+------------------------------------------------------+")
        option = input("Enter number to select an option: ")
        return int(option)
