
from georgia import db
from georgia.Database.models import  Donor, Donation, Official

#^DB CREATION FUNCTIONS:

def create_donor(donor_id, donor_name, donor_type, broad_sector, general_industry, specific_type):
    """Creates a donor objects and stores it in the donors table"""
    donor = Donor(
        donor_id = donor_id,
        donor_name = donor_name,
        donor_type = donor_type,
        broad_sector = broad_sector,
        general_industry = general_industry,
        specific_type = specific_type,
    )

    db.session.add(donor)
    db.session.commit()

    return donor 


def create_official(official_id, official_name, last_name, party, position_name, branch, court, district, height):
    """Creates an official object and stores it in the officials table"""

    official = Official(
        official_id = official_id,
        official_name = official_name,
        last_name=last_name,
        party = party,
        position_name = position_name,
        branch = branch,
        court = court,
        district=district,
        height = height    
    )

    db.session.add(official)
    db.session.commit()

    return official


def create_donation(amount, election_year, record_count, donor_id, official_id):
    """Creates a donation object and stores it in the donations table"""

    donation = Donation(
        amount = amount,
        election_year=election_year,
        record_count = record_count,
        donor_id=donor_id,
        official_id = official_id,   
    )

    db.session.add(donation)
    db.session.commit()

    return donation 


