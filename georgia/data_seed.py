import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import csv
from georgia import db, app
import georgia.create as c
import georgia.models as models
import georgia.user_funcs as u

os.system("dropdb georgia")
os.system("createdb georgia")

models.connect_to_db(app)
db.create_all()

# pull a list of dictionaries from tsv file
data_list = []
with open("data/alldata.tsv", newline= "") as data:
    data_reader = csv.DictReader(data, delimiter = '\t')
    for line in data_reader:
        data_list.append(line)

def get_last_name(full_name):
    name_list = full_name.split(" ")
    comma_name = name_list[0]
    last_name = comma_name[:-1]
    return last_name

def parse_branch(position_name, party):
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
    if "APPELLATE" in position_name:
        return "APPELLATE"
    else:
        return "SUPREME"
    

#Seed database with official info  
official_list = [] 
for dict in data_list:
    official_id = dict["ga_id"]
    if official_id not in official_list:
        official_list.append(official_id)
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
        db_official = c.create_official(official_id=official_id, official_name=official_name, last_name=last_name, party=party, position_name=position_name, branch=branch, court=court, district=district, height=height)
        dict["official_id"] = models.Official.get_official_id(db_official)
    








# Seed database with donor info
donor_list = []
for dict in data_list:
    donor_id = dict["donor_id"]
    if donor_id not in donor_list:
        donor_list.append(donor_id)
        donor_name = dict["Contributor"]
        donor_type = dict["Type_of_Contributor"]
        broad_sector = dict["Broad_Sector"]
        general_industry = dict["General_Industry"]
        specific_type = dict["Specific_Business"]

        db_donor =c.create_donor(donor_id = donor_id, donor_name=donor_name, donor_type=donor_type, broad_sector=broad_sector, general_industry=general_industry, specific_type=specific_type)
        dict["donor_id"]=models.Donor.get_donor_id(db_donor)


# Seed database with donation info
for dict in data_list:
    official_id = dict["ga_id"]
    donor_id = dict["donor_id"]
    amount = dict['Total_$']
    election_year = dict["Election_Year"]
    record_count = dict["#_of_Records"]

    db_donation = c.create_donation(amount=amount, election_year=election_year, record_count=record_count, donor_id=donor_id, official_id=official_id)

user_names = ["cspiering", "cesimms", "bsonderman", 'dkanaga', 'ndamluji', 'ialden', 'cduncan', 'jpineda']
passwords = ['account', 'theme', 'choice', 'potato', 'fascinate', 'cast', 'pastel', 'lamp']
emails = ['cespiering@gmail.com', 'carly.trial@gmail.com', 'bsonderman@pitzer.gov', 'dkanaga@nelnet.edu', 'ndamluji@whitman.edu', 'ialden@whitman.edu', 'cduncan@whitman.edu', 'jpineda@whitman.edu']

for i in range(len(user_names)):
    user_name = user_names[i]
    password = passwords[i]
    email = emails[i]

    db_user = u.create_user(email = email, user_name=user_name, password=password)

