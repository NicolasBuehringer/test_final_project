from tweets import main
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_wikipedia_table():

    # get wikipedia textfile of whole article
    website_url = requests.get(
        "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2021_German_federal_election"
    ).text

    # create parser
    soup = BeautifulSoup(website_url, "html.parser")
    type(soup)

    # find the table and return it
    my_table = soup.find(
        "table", {"class": "wikitable sortable tpl-blanktable mw-collapsible"})

    return str(my_table)



data= pd.read_html(get_wikipedia_table())
# convert list to dataframe
data= pd.DataFrame(data[0])

# Columns are somehow a tuple of duplicates -> reduce to one colum name
data.columns = [x[0] for x in data.columns]

# save series of the Fieldwork date
dates = list(data["Fieldwork date"])


# split current timeframe string at - or space with regex; before "26-28 Jan 2021"
splitted_timeframe = []
for c in dates:
    splitted_timeframe.append(re.split("–| ", c))

#create helper dict
months_dict = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Okt": "10",
    "Nov": "11",
    "Dec": "12"
}

#create helper dict
days_dict = {
    "Jan": "31",
    "Feb": "28",
    "Mar": "31",
    "Apr": "30",
    "May": "31",
    "Jun": "30",
    "Jul": "31",
    "Aug": "31",
    "Sep": "30",
    "Okt": "31",
    "Nov": "30",
    "Dec": "31"
}


def poll_to_year(year_dataframe):
    year = []
    #iterate over each poll timeframe
    for poll in year_dataframe:
        dates = []
        month = []

        # iterate over each element in a poll timeframe
        for element in poll:

            # check if element is a date
            if len(element) == 2 or len(element) == 1:
                dates.append(int(element))

            # check if element is a month
            if len(element) == 3:
                month.append(element)

        # if poll was conducted on one single day
        if len(dates) == 1:
            #append poll day to year list as a list through split()
            year.append(f"{dates[0]}/{months_dict[month[0]]}/2021".split())

        else:
            # try to get all dates on which the poll was conducted
            x = list(range(dates[0], (int(dates[1]) + 1)))

            sub_list = []

            # check if x is valid range
            if x:

                #iterate over alls days and append them as a list with theirs month as digits and the year to a normal dd/mm/yyyy syntax
                for date in x:
                    sub_list.append(f"{date}/{months_dict[month[0]]}/2021")

                #append list of lists for one poll to the year list
                year.append(sub_list)

            # if the poll was conducted in two month x is  an empty list and thus False ->this will be executed
            else:

                # get the dates of the polls in the first month
                dates_first_month = range(dates[0],
                                          (int(days_dict[month[0]]) + 1))

                #append each day in formant dd/mm/yyyy as a list to sub_list
                for date in dates_first_month:
                    sub_list.append(f"{date}/{months_dict[month[0]]}/2021")

                # get the dates of the polls in the second month
                dates_second_month = range(1, (dates[1] + 1))

                #append each day in formant dd/mm/yyyy as a list to sub_list
                for date in dates_second_month:
                    sub_list.append(f"{date}/{months_dict[month[1]]}/2021")

                #append list of lists to years
                year.append(sub_list)

    return year
