from view import *
from model import *
from covid_global import *
from covid_canada import *
from pyplot import *
from logger import *
import datetime


class Controller():

    # Controller initialized with a view and model object
    def __init__(self):
        self.__view = View()
        self.__model = Model()

    # Execute the app
    def run(self):
        # initialize the database table
        self.__model.initialize(my_sql_pool)
        while True:
            option = self.__view.main_page()
            chain.log("Selected main page option: " + str(option) + "\n")
            if option == 1:
                self.search_global_data()
            elif option == 2:
                self.search_canada_data()
            else:
                print("Goodbye!")
                exit()

    # Search data globally
    def search_global_data(self):
        print("+------------------------------------------------------+")
        print("| Global Covid-19 Data Summary:                         ")
        CovidGlobal().print_global_summary()

        option = self.__view.select_global_option()
        chain.log("Selected global data option: " + str(option) + "\n")
        if option == 1:
            self.search_by_country_name()
        elif option == 2:
            self.select_favourite_country()
        elif option == 3:
            return
        else:
            print("Goodbye!")
            exit()

    # Search the inputted country
    def search_by_country_name(self):
        user_input = self.__view.set_global_location()
        chain.log("Inputted country name: " + str(user_input) + "\n")
        if user_input == "0":
            print("Goodbye!")
            exit()
        else:
            self.validate_country_input(user_input.capitalize())

    # Access the favourite country list
    def select_favourite_country(self):
        favourite_list = self.__model.get_all_countries(my_sql_pool)
        chain.log("Selected favourite country list option: " + str(favourite_list) + "\n")
        if len(favourite_list) == 0:
            print("+------------------------------------------------------+")
            print("| Favourite Country List is Empty")
            return
        else:
            print("+------------------------------------------------------+")
            print("| Favourite Country List:")

            for idx, country in enumerate(favourite_list):
                print("| (" + str(idx + 1) + ") " + country)
            print("| (0) Cancel ")
            index = input("Enter a number to select an option: ")
            if index == "0":
                return
            else:
                country_name = favourite_list[int(index) - 1]
                self.validate_country_input(country_name)

    # Validate if the inputted data can be retrieved from the API
    def validate_country_input(self, user_input):
        country_data = CovidGlobal().get_country_summary(user_input)
        if country_data is not None:
            print("+------------------------------------------------------+")
            print("| " + user_input.capitalize() + "'s Covid-19 Data Summary: ")
            CovidGlobal().print_country_summary(user_input)
            self.search_by_country_date_range(user_input)
        else:
            print("+------------------------------------------------------+")
            print("| ERROR! Country Name Not Found. Please Try Again!      ")
            self.search_by_country_name()

    # Validate if the inputted date range's format is correct
    def search_by_country_date_range(self, country_name):
        start_date, end_date = self.__view.set_global_date_range()
        chain.log("Inputted date range data: " + str(start_date) + " & " + str(end_date) + "\n")
        if start_date == "0" or end_date == "0":
            print("Goodbye!")
            exit()
        elif start_date == "1" or end_date == "1":
            result = CovidGlobal().get_country_all_data(country_name)
            title = 'All Covid-19 Data of ' + country_name.capitalize()
            print("+------------------------------------------------------+")
            print("| Please close the plot to continue                     ")
            self.plot_covid19_data(result, title, "country")
            result = self.__model.get_country(country_name, my_sql_pool)
            # Skip save as favourite page if the data already exits in the DB
            if len(result) >= 1:
                self.export_country_data(country_name)
            else:
                self.save_as_favourite(country_name, "country")
        elif self.convert_datetime(start_date) > self.convert_datetime(end_date):
            print("+------------------------------------------------------+")
            print("| ERROR! Invalid Date range. Please Try Again!          ")
            self.search_by_country_date_range(country_name)
        elif self.validate_datetime(start_date) and self.validate_datetime(end_date):
            result = CovidGlobal().get_country_daterange_data(country_name, start_date, end_date)
            title = 'Covid-19 Data of ' + country_name.capitalize() + " From " + start_date + " To " + end_date
            print("+------------------------------------------------------+")
            print("| Please close the plot to continue                     ")
            self.plot_covid19_data(result, title, "country")
            result = self.__model.get_country(country_name, my_sql_pool)
            # Skip save as favourite page if the data already exits in the DB
            if len(result) >= 1:
                self.export_country_data(country_name)
            else:
                self.save_as_favourite(country_name, "country")
        else:
            print("+------------------------------------------------------+")
            print("| ERROR! Invalid Date Format. Please Try Again!         ")
            self.search_by_country_date_range(country_name)

    # Search data from Canada's provinces
    def search_canada_data(self):
        print("+------------------------------------------------------+")
        print("| Canada's Covid-19 Data Summary:                       ")
        CovidCanada().print_canada_summary()

        option = self.__view.select_canada_option()
        chain.log("Selected provincial data option: " + str(option) + "\n")
        if option == 1:
            self.search_by_province_abbreviation()
        elif option == 2:
            self.select_favourite_province()
        elif option == 3:
            return
        else:
            print("Goodbye!")
            exit()

    # Search the province in Canada by inputted abbreviation
    def search_by_province_abbreviation(self):
        user_input = self.__view.set_province_location().upper()
        chain.log("Inputted province abbreviation: " + str(user_input) + "\n")
        if user_input == "0":
            print("Goodbye!")
            exit()
        else:
            self.validate_province_input(user_input)

    # Access the favourite province list
    def select_favourite_province(self):
        favourite_list = self.__model.get_all_provinces(my_sql_pool)
        chain.log("Selected favourite province list option: " + str(favourite_list) + "\n")
        if len(favourite_list) == 0:
            print("+------------------------------------------------------+")
            print("| Favourite Province List is Empty")
            return
        else:
            print("+------------------------------------------------------+")
            print("| Favourite Province List: ")

            for idx, province in enumerate(favourite_list):
                print("| (" + str(idx + 1) + ") " + province)
            print("| (0) Cancel ")
            index = input("Enter a number to select an option: ")
            if index == "0":
                return
            else:
                province_name = favourite_list[int(index) - 1]
                provinces = CovidCanada().canada_provinces

                for abb, name in provinces.items():
                    if name == province_name:
                        self.validate_province_input(abb)

    # Validate if the inputted data can be retrieved from the API
    def validate_province_input(self, user_input):
        province_data = CovidCanada().get_province_summary(user_input)
        if province_data is not None:
            provinces = CovidCanada().canada_provinces
            full_name = provinces[user_input]
            print("+------------------------------------------------------+")
            print("| " + full_name + "'s Covid-19 Data Summary: ")
            CovidCanada().print_province_summary(user_input)
            self.search_by_province_date_range(user_input)
        else:
            print("+------------------------------------------------------+")
            print("| ERROR! Province Abbreviation Not Found. Please Try Again!")
            self.search_by_province_abbreviation()

    # Validate if the inputted date range's format is correct
    def search_by_province_date_range(self, province_abb):
        start_date, end_date = self.__view.set_province_date_range()
        chain.log("Inputted date range data: " + str(start_date) + " & " + str(end_date) + "\n")
        provinces = CovidCanada().canada_provinces
        full_name = provinces[province_abb]
        if start_date == "0" or end_date == "0":
            print("Goodbye!")
            exit()
        elif start_date == "1" or end_date == "1":
            result = CovidCanada().get_province_all_data(province_abb)
            title = 'All Covid-19 Data of ' + full_name
            print("+------------------------------------------------------+")
            print("| Please close the plot to continue                     ")
            self.plot_covid19_data(result, title, "province")
            result = self.__model.get_province(full_name, my_sql_pool)
            # Skip save as favourite page if the data already exits in the DB
            if len(result) >= 1:
                self.export_province_data(province_abb)
            else:
                self.save_as_favourite(province_abb, "province")
        elif self.convert_datetime(start_date) > self.convert_datetime(end_date):
            print("+------------------------------------------------------+")
            print("| ERROR! Invalid Date range. Please Try Again!          ")
            self.search_by_province_date_range(full_name)
        elif self.validate_datetime(start_date) and self.validate_datetime(end_date):
            result = CovidCanada().get_province_daterange_data(province_abb, start_date, end_date)
            title = 'All Covid-19 Data of ' + full_name + " From " + start_date + " To " + end_date
            print("+------------------------------------------------------+")
            print("| Please close the plot to continue                     ")
            self.plot_covid19_data(result, title, "province")
            result = self.__model.get_province(full_name, my_sql_pool)
            # Skip save as favourite page if the data already exits in the DB
            if result is not None:
                self.export_province_data(province_abb)
            else:
                self.save_as_favourite(province_abb, "province")
        else:
            print("+------------------------------------------------------+")
            print("| ERROR! Invalid Date Format. Please Try Again!         ")
            self.search_by_province_date_range(province_abb)

    # Save the country or province name into the SQLite3 database
    def save_as_favourite(self, name, data_type):
        option = self.__view.save_as_favourite()
        chain.log("Saved " + name + " into favourite " + data_type + " list. \n")
        if option == 1:
            if data_type == "country":
                self.__model.insert_country(name, my_sql_pool)
            elif data_type == "province":
                provinces = CovidCanada().canada_provinces
                full_name = provinces[name]
                self.__model.insert_province(full_name, name, my_sql_pool)
        else:
            pass
        if data_type == "country":
            self.export_country_data(name)
        elif data_type == "province":
            self.export_province_data(name)

    # Export the Covid-19 summary data of the country into a text file
    def export_country_data(self, name):
        option = self.__view.export_data()
        chain.log("Exported " + name + "'s Covid-19 summary data into text file. \n")
        if option == 1:
            data = CovidGlobal().get_country_summary(name)
            location = name + "'s Covid-19 Summary.txt"
            output_file = open(location, "a")
            output_file.write(name + "'s Covid-19 Summary" + "\n")
            output_file.write("Total Confirmed: \t" + str(data["TotalConfirmed"]) + "\n"
                              + "Total Deaths: \t\t" + str(data["TotalDeaths"]) + "\n"
                              + "Total Recovered: \t" + str(data["TotalRecovered"]) + "\n"
                              + "New Confirmed: \t\t" + str(data["NewConfirmed"]) + "\n"
                              + "New Deaths: \t\t" + str(data["NewDeaths"]) + "\n"
                              + "New Recovered: \t\t" + str(data["NewRecovered"]) + "\n")
            output_file.close()
            print("File Exported!")

    # Export the Covid-19 summary data of the province into a text file
    def export_province_data(self, name):
        option = self.__view.export_data()
        if option == 1:
            data = CovidCanada().get_province_summary(name)
            provinces = CovidCanada().canada_provinces
            full_name = provinces[name]
            location = full_name + "'s Covid-19 Summary.txt"
            output_file = open(location, "a")
            output_file.write(full_name + "'s Covid-19 Summary"+ "\n")
            output_file.write("Total Cases: \t\t" + str(data["total_cases"]) + "\n"
                              + "Total Deaths: \t\t" + str(data["total_fatalities"]) + "\n"
                              + "Hospitalizations: \t" + str(data["total_hospitalizations"]) + "\n"
                              + "Criticals: \t\t" + str(data["total_criticals"]) + "\n"
                              + "Recoveries: \t\t" + str(data["total_recoveries"]) + "\n"
                              + "Vaccinated: \t\t" + str(data["total_vaccinated"]) + "\n")
            output_file.close()
            print("File Exported!")

    # Draw the plot by using the matplotlib with the given data
    def plot_covid19_data(self, result, title, data_type):
        if data_type == "country":
            context = Context(GlobalPlotStrategy())
            context.display_plot(result, title)
        elif data_type == "province":
            context = Context(CanadaPlotStrategy())
            context.display_plot(result, title)

    # Validate the date format YYYY-MM-DD
    def validate_datetime(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            return False
        return True

    # Convert the string datetime to datetime format
    def convert_datetime(self, date_text):
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')