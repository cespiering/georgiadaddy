from georgia import db
from georgia.Database.models import Donor, Donation, Official

def get_all_officials():
    test = Official.query.all()
    all_officials = []
    for name in test:
        all_officials.append(name.official_name)
    officials = sorted(all_officials)
    return officials

def get_all_districts():
    all = Official.query.filter(Official.district.isnot(None)).all()
    district_list = []
    for official in all:
        d = official.district
        if d not in district_list:
            district_list.append(d)
    all_districts = sorted(district_list)
    return all_districts

def get_all_jobs():
    officials = Official.query.all()
    job_list = []
    for official in officials:
        job = official.position_name
        if job not in job_list:
            job_list.append(job)
    all_jobs = sorted(job_list)
    return all_jobs

def get_all_sectors():
    donors = Donor.query.all()
    sector_list = []
    for donor in donors:
        sector = donor.broad_sector
        if sector not in sector_list:
            sector_list.append(sector)
    all_sectors = sorted(sector_list)
    return all_sectors

def find_all_exec():
    results = Official.query.filter(Official.branch=='E').all()
    jobArray = []
    for result in results:
        if result.position_name not in jobArray:
            jobArray.append(result.position_name)
    return jobArray

def sec_tup():
    donors = Donor.query.all()
    sector_list = []
    for donor in donors:
        sector = donor.broad_sector
        if sector not in sector_list:
            sector_list.append(sector)
    all_sectors = sorted(sector_list)
    tup_list = [(i, i) for i in all_sectors]
    return tup_list


#^ ******* SEARCH FUNCTIONS FOR QUERYING DB:

#******HANDLING DUPLICATE NAMES
def get_donations_by_last_name(last_name):
    last_name = last_name.upper()
    official = Official.query.filter_by(last_name=last_name).first()
    donations = official.donations
    return donations

def get_official_by_last_name(last_name):
    """returns the full name of officeholder if no name duplicates"""
    last_name = last_name.upper()
    official = Official.query.filter_by(last_name=last_name).first()
    if official == None:
        return None
    return official.official_name

def check_for_duplicate_names(last_name):
    """checks if there are more than one official with last_name, returns bool"""
    last_name = last_name.upper()
    matches = Official.query.filter_by(last_name=last_name).all()
    if len(matches) > 1:
        return True

def get_identical_names(last_name):
    """returns list of duplicate official objs"""
    last_name = last_name.upper()
    matches = Official.query.filter_by(last_name=last_name).all()
    return matches




def get_all_by_official_name(official_name):
    """returns all donation objects associated with official's full name"""
    official = Official.query.filter_by(official_name=official_name).first()
    donations = official.donations
    return donations

def get_position_name(official_name):
    official = Official.query.filter_by(official_name=official_name).first()
    position = official.position_name
    return position


def get_by_job(job):
    """Takes a position name and returns officials related"""
    job_holders = Official.query.filter_by(position_name=job).all()
    return job_holders

def get_by_sector(broad_sector):
    donors = Donor.query.filter_by(broad_sector=broad_sector).all()
    return donors  

def get_by_donor_name(donor_name):
    """takes a donor's name, returns all donations and officials related""" 
    donor = Donor.query.filter_by(donor_name=donor_name).first()
    donations = donor.donations
    return donations


def get_by_district(district):
    """Takes in a district number, returns all officials, donations, donors related"""
    official_objs = Official.query.filter_by(district=district).all()
    return official_objs


def get_by_amount(limit):
    """Takes in a limiting argument(20, 50, 100) and returns reciepient, donor from most given descending"""
    pass


# ^ MEGA SEARCH FUNCTION TRIAL
#pseudo
#Take in a dict of parameter. The key should be the same name as the column
#create a base query
# find out which key in value applies to which table

#base = db.session.query(Official, Donation, Donor).select_from(Official).join(Donation).join(Donor)


def donation_filter(params, results):
    results = results
    for key in params:
        if key == "donation_type":
            results=results.filter(Donor.donor_type==params[key])
        if key == "donor_sector":
            results = results.filter(Donor.broad_sector==params[key])
        if key == "max_amount":
            num = params[key]
            num = float(num)
            results = results.filter(Donation.amount<=num)
        if key == "min_amount":
            num = params[key]
            num = float(num)
            results = results.filter(Donation.amount>=num)
    return results



def narrow_by_official_specific(params):
    results = db.session.query(Official, Donation, Donor).select_from(Official).join(Donation).join(Donor)
    params = {key:value for (key, value) in params.items() if value != None}
    params = {key:value for (key, value) in params.items() if value != "All"}
    results = results.filter(Official.official_name==params["official_name"])
    results = donation_filter(params, results)
    return results.all()

def test_filter_1(params):
    results = db.session.query(Official, Donation, Donor).select_from(Official).join(Donation).join(Donor)
    params = {key:value for (key, value) in params.items() if value != None}
    params = {key:value for (key, value) in params.items() if value != "All"}
    results = results.filter(Official.official_name==params["official_name"])
    results = donation_filter(params, results)
    return results

#note: creates a list of results that can be accessed as such:
# data = narrow_by_official_specific(test)
#for line in data:
    #print(line.Official.official_name)
    #print(line.Donor.donor_type)
    #print(line.Donation.amount
def narrow_by_official_general(params):
    results = db.session.query(Official, Donation, Donor).select_from(Official).join(Donation).join(Donor)
    params = {key:value for (key, value) in params.items() if value != None}
    params = {key:value for (key, value) in params.items() if value != "All"}
    params = {key:value for (key, value) in params.items() if value != "None"}
    results = donation_filter(params, results)
    for key in params:
        if key == "branch":
            results = results.filter(Official.branch==params[key])
        if key == "exec_jobs":
            results = results.filter(Official.position_name==params[key])
        if key == "height":
            results = results.filter(Official.height==params[key])
        if key == "court":
            results = results.filter(Official.court==params[key])
        if key == "district":
            str_num = params[key]
            if len(str_num) == 1:
                str_num = "00" + str_num
            elif len(str_num) == 2:
                str_num = "0" + str_num
            results = results.filter(Official.district==str_num)
        if key == 'party':
            results = results.filter(Official.party==params[key])
    return results.all()

def test_filter(params):
    results = db.session.query(Official, Donation, Donor).select_from(Official).join(Donation).join(Donor)
    params = {key:value for (key, value) in params.items() if value != None}
    params = {key:value for (key, value) in params.items() if value != 'All'}
    params = {key:value for (key, value) in params.items() if value != 'None'}
    params = {key:value for (key, value) in params.items() if value != ''}
    results = donation_filter(params, results)
    for key in params:
        if key == "branch":
            results = results.filter(Official.branch==params[key])
        if key == "exec_jobs":
            results = results.filter(Official.position_name==params[key])
        if key == "height":
            results = results.filter(Official.height==params[key])
        if key == "court":
            results = results.filter(Official.court==params[key])
        if key == "district":
            str_num = params[key]
            if len(str_num) == 2:
                str_num = "0" + str_num
            elif len(str_num) == 1:
                str_num = "00" + str_num
            results = results.filter(Official.court==str_num)
        if key == "party":
            results = results.filter(Official.party==params[key])
    return results

def response_to_dict(response):
    results = []
    for line in response:
        a = line.Official.to_dict()
        b = line.Donor.to_dict()
        c = line.Donation.to_dict()
        d = a.update(b)
        e = a.update(c)
        results.append(a)
    return results