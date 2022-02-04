import os
import sys

#changing path allows for db connection in nested structure
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import csv
from georgia import app, db
import georgia.create as c
import georgia.models as models
import georgia.user_funcs as u

#dropdb/createdb is utlized when changing database contents, otherwise can be excluded
os.system("dropdb georgia")
os.system("createdb georgia")

models.connect_to_db(app)
db.create_all()

# creates a list of dictionaries from the alldata.tsv file
data_list = []
with open("data/alldata.tsv", newline= "") as data:
    data_reader = csv.DictReader(data, delimiter = '\t')
    for line in data_reader:
        data_list.append(line)



# functions for parsing information for the Officials table
def get_last_name(full_name):
    """gets only the last name from official name"""
    name_list = full_name.split(" ")
    comma_name = name_list[0]
    last_name = comma_name[:-1]
    return last_name

def parse_branch(position_name, party):
    """returns branch of government"""
    if any(char.isdigit() for char in position_name):
        pos_list = position_name.split(" ")
        if "COMMISSIONER" in pos_list:
            return "E"
        else:
            return "L"
    if party == "Nonpartisan":
        return "J"
    return "E"

def parse_court(position_name):
    """for judicial officials, returns court"""
    if "APPELLATE" in position_name:
        return "APPELLATE"
    else:
        return "SUPREME"


def create_official_entry(dict, official_id):
    official_name = dict["Officeholder"]
    last_name = get_last_name(official_name)
    party = dict["General_Party"]
    position_name = (dict["Office_Held"])
    branch = parse_branch(position_name, party)
    court = None
    if branch == "J":
        court = parse_court(position_name)
    district = None
    height = None
    if any(char.isdigit() for char in position_name):
        pos_list = position_name.split(" ")
        district = pos_list[-1]
        height = pos_list[0]
    c.create_official(official_id=official_id, official_name=official_name, last_name=last_name, party=party, position_name=position_name, branch=branch, court=court, district=district, height=height)


def create_donor_entry(dict, donor_id):
        donor_name = dict["Contributor"]
        donor_type = dict["Type_of_Contributor"]
        broad_sector = dict["Broad_Sector"]
        general_industry = dict["General_Industry"]
        specific_type = dict["Specific_Business"]

        c.create_donor(donor_id = donor_id, donor_name=donor_name, donor_type=donor_type, broad_sector=broad_sector, general_industry=general_industry, specific_type=specific_type)


def create_donation_entry(dict):
    official_id = dict["ga_id"]
    donor_id = dict["donor_id"]
    amount = dict['Total_$']
    election_year = dict["Election_Year"]
    record_count = dict["#_of_Records"]

    c.create_donation(amount=amount, election_year=election_year, record_count=record_count, donor_id=donor_id, official_id=official_id)


#Parse each data line and populate tables
processed_officials = []
processed_donors = []

for dict in data_list:
    official_id = dict["ga_id"]
    donor_id = dict["donor_id"]


    if official_id not in processed_officials:
        processed_officials.append(official_id)
        create_official_entry(dict)

    if donor_id not in processed_donors:
        processed_donors.append(donor_id)
        create_donor_entry(dict, donor_id)
    
    create_donor_entry()




#fake user info for demo purposes
user_names = ["cspiering", "cesimms", "bsonderman", 'dkanaga', 'ndamluji', 'ialden', 'cduncan', 'jpineda']
passwords = ['account', 'theme', 'choice', 'potato', 'fascinate', 'cast', 'pastel', 'lamp']
emails = ['cespiering@gmail.com', 'carly.trial@gmail.com', 'bsonderman@pitzer.gov', 'dkanaga@nelnet.edu', 'ndamluji@whitman.edu', 'ialden@whitman.edu', 'cduncan@whitman.edu', 'jpineda@whitman.edu']

for i in range(len(user_names)):
    user_name = user_names[i]
    password = passwords[i]
    email = emails[i]

    u.create_user(email = email, user_name=user_name, password=password)

