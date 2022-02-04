from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from georgia.Database.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class ChangePasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Contact your administrator.')

class EmailResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Contact your administrator.')

class SearchType(FlaskForm):
    search_type = SelectField("Search Type", choices=[('specific','By Specific Name'), ('officials', 'By Officeholder'), ('v2', 'By Officeholder V2')])
    submit = SubmitField('Go')

class SpecificNameForm(FlaskForm):
    last_name = StringField("Last Name")
    max_amount = IntegerField("Max Donation")
    min_amount = IntegerField("Min Donation")
    donation_type = SelectField("Donor Type", choices=[("All", "All"), ("Individual", "Individual"), ("Non-Individual", "Business"), ("Other", "Other")])
    donor_sector = SelectField("Industry", choices= [("All", "All"), ('Agriculture', 'Agriculture'), ('Candidate Contributions', 'Candidate Contributions'), ('Communications & Electronics', 'Communications & Electronics'), ('Construction', 'Construction'), ('Defense', 'Defense'), ('Energy & Natural Resources', 'Energy & Natural Resources'), ('Finance, Insurance & Real Estate', 'Finance, Insurance & Real Estate'), ('General Business', 'General Business'), ('Government Agencies/Education/Other', 'Government Agencies/Education/Other'), ('Health', 'Health'), ('Ideology/Single Issue', 'Ideology/Single Issue'), ('Labor', 'Labor'), ('Lawyers & Lobbyists', 'Lawyers & Lobbyists'), ('Party', 'Party'), ('Transportation', 'Transportation'), ('Uncoded', 'Uncoded'), ('Unitemized Contributions', 'Unitemized Contributions')])
    submit = SubmitField('Go')



class GeneralNameForm(FlaskForm):
    party = SelectField("Party", choices=[("None", "All"), ("Democratic", "Democrat"), ("Republican", "Republican"), ("Nonpartisan", "Other")])
    branch = SelectField("Branch", choices=[("None", "All"), ("E", "Executive"), ("J", "Judicial"), ("L", "Legislative")])
    exec_jobs = SelectField("Executive Positions", choices=[])
    district = StringField("District")
    height = SelectField("Congressional House", choices = [("None", "All"), ("HOUSE", "House"), ("SENATE", "Senate")])
    court = SelectField("Court", choices=[("None", "All"), ("APPELLATE", "Appellate"), ("SUPREME", "Supreme")])
    max_amount = IntegerField("Max Donation")
    min_amount = IntegerField("Min Donation")
    donation_type = SelectField("Donor Type", choices=[("All", "All"), ("Individual", "Individual"), ("Business", "Non-Individual"), ("Other", "Other")])
    donor_sector = SelectField("Industry", choices= [("All", "All"), ('Agriculture', 'Agriculture'), ('Candidate Contributions', 'Candidate Contributions'), ('Communications & Electronics', 'Communications & Electronics'), ('Construction', 'Construction'), ('Defense', 'Defense'), ('Energy & Natural Resources', 'Energy & Natural Resources'), ('Finance, Insurance & Real Estate', 'Finance, Insurance & Real Estate'), ('General Business', 'General Business'), ('Government Agencies/Education/Other', 'Government Agencies/Education/Other'), ('Health', 'Health'), ('Ideology/Single Issue', 'Ideology/Single Issue'), ('Labor', 'Labor'), ('Lawyers & Lobbyists', 'Lawyers & Lobbyists'), ('Party', 'Party'), ('Transportation', 'Transportation'), ('Uncoded', 'Uncoded'), ('Unitemized Contributions', 'Unitemized Contributions')])
    submit = SubmitField('Go')

class TestForm(FlaskForm):
    party = SelectField("Party", choices=[("None", "All"), ("Democratic", "Democrat"), ("Republican", "Republican"), ("Nonpartisan", "Other")])
    branch = SelectField("Branch", choices=[("None", "All"), ("E", "Executive"), ("J", "Judicial"), ("L", "Legislative")])
    exec_jobs = SelectField("Executive Positions", choices=[])
    district = StringField("District")
    height = SelectField("Congressional House", choices = [("None", "All"), ("HOUSE", "House"), ("SENATE", "Senate")])
    court = SelectField("Court", choices=[("None", "All"), ("APPELLATE", "Appellate"), ("SUPREME", "Supreme")])
    max_amount = IntegerField("Max Donation")
    min_amount = IntegerField("Min Donation")
    donation_type = SelectField("Donor Type", choices=[("All", "All"), ("Individual", "Individual"), ("Business", "Non-Individual"), ("Other", "Other")])
    donor_sector = SelectField("Industry", choices= [("All", "All"), ('Agriculture', 'Agriculture'), ('Candidate Contributions', 'Candidate Contributions'), ('Communications & Electronics', 'Communications & Electronics'), ('Construction', 'Construction'), ('Defense', 'Defense'), ('Energy & Natural Resources', 'Energy & Natural Resources'), ('Finance, Insurance & Real Estate', 'Finance, Insurance & Real Estate'), ('General Business', 'General Business'), ('Government Agencies/Education/Other', 'Government Agencies/Education/Other'), ('Health', 'Health'), ('Ideology/Single Issue', 'Ideology/Single Issue'), ('Labor', 'Labor'), ('Lawyers & Lobbyists', 'Lawyers & Lobbyists'), ('Party', 'Party'), ('Transportation', 'Transportation'), ('Uncoded', 'Uncoded'), ('Unitemized Contributions', 'Unitemized Contributions')])
    submit = SubmitField('Go')

class TestForm2(FlaskForm):
    username = StringField("username")
    submit = SubmitField('Go')