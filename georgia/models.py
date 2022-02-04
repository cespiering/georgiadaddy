
from georgia import db, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(25), default = "user")
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


    def get_reset_token(self, expires_sec=1800):
        """Gets an encrypted token that lasts for 30 mins"""
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token


    # note: static decorator makes self argument unnecessary
    @staticmethod
    def verify_reset_token(token):
        """Checks if reset token matches. Returns None if token doesn't match/is expired"""
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)




class Donation(db.Model):
    """Individual donation"""

    __tablename__ = "donations"

    donation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey("donors.donor_id"))
    official_id = db.Column(db.Integer, db.ForeignKey("officials.official_id"))
    amount = db.Column(db.Float)
    election_year = db.Column(db.Integer)
    record_count = db.Column(db.Integer)    

#     # ? When in donations table, door to donors table is "donor"
#     # ? When in donations table, door to officials table is "official"


    # official = db.relationship("Official", backref="donations")
    # donor = db.relationship("Donor", backref="donations")
    
    def __repr__(self):
        return f"<Donation donation_id={self.donation_id} amount={self.amount}>"

    def to_dict(self):
        return {
            'amount': self.amount,
            'election_year': self.election_year,
            'record_count': self.record_count
        }



class Donor(db.Model):
    """Donation Contributor"""

    __tablename__ = "donors"

    donor_id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(255))
    donor_type = db.Column(db.String(100))
    broad_sector = db.Column(db.String(100))
    general_industry = db.Column(db.String(100))
    specific_type = db.Column(db.String(100))

    donations = db.relationship('Donation', backref='donor')

    # ? When in donors table, door to donations is "donations"

    # donations = list of donation objects
    # Donor.donations will return all donations given by the Donor

    def __repr__(self):
        return f"<Donor donor_id={self.donor_id} name={self.donor_name}>"

    def get_donor_id(self):
        return self.donor_id

    def to_dict(self):
        return {
            'donor_name': self.donor_name,
            'donor_type': self.donor_type,
            'broad_sector': self.broad_sector
        }



class Official(db.Model):
    """A Current Office-holder in GA"""

    __tablename__ = "officials"

    official_id = db.Column(db.Integer, primary_key = True, unique=True)
    official_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    party = db.Column(db.String(50), nullable = True)
    position_name = db.Column(db.String(100), nullable = True)
    branch = db.Column(db.String(10), nullable = True)
    court = db.Column(db.String(10), nullable = True)
    district = db.Column(db.String, nullable = True)
    height = db.Column(db.String(15), nullable = True)

    donations = db.relationship('Donation', backref='official')

#     # ? When in officials table, door to donations is 'donations'

    
    # donations = list of donation objects
    #Official.donations will return all donations given to the official
    
    def __repr__(self):
        return f"<Official official_id={self.official_id} name={self.official_name}>"

    def get_official_id(self):
        return self.official_id

    def to_dict(self):
        return {
            'official_name': self.official_name,
            'party': self.party,
            'position_name': self.position_name,
            'branch': self.branch,
            'court': self.court,
            'district': self.district,
            'height': self.height
        }


#note: trying to connect to the database to populate tables

def connect_to_db(flask_app, db_uri="postgresql:///georgia", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":

    connect_to_db(app)