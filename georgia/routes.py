from flask import Blueprint, jsonify, request, render_template, flash, redirect, session, url_for
from georgia import app, db, mail
from georgia.forms import TestForm, LoginForm, ChangePasswordForm, EmailResetForm, SpecificNameForm, SearchType, GeneralNameForm
from georgia.models import User, Official, Donation, Donor
from flask_login import login_user, current_user, logout_user, login_required
import georgia.user_funcs as u
import georgia.filter as filter
from flask_mail import Message
# views = Blueprint("views", __name__)

# ^ HOMEPAGE:


@app.route("/")
@app.route('/home')
def show_homepage():
    return render_template("homepage.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# ^ LOGIN AND PASSWORD CHANGING:

@app.route("/login", methods=['GET', 'POST'])
def login():
    """logs in user, checks for already authenticated user"""
    if current_user.is_authenticated:
        return redirect(url_for("search_home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = u.get_user(form.email.data)
        if user and u.check_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You have logged in!', 'success')
            return redirect(url_for('search_home'))
        else:
            flash(f'user not found', 'danger')
    return render_template("login.html", form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('CorruptApp Password Reset',
                  sender='carly.trial@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Click the link below to change your password:
{url_for('reset_password', token=token, _external=True)}
If you did not make this request then simply ignore this email.
'''
    mail.send(msg)


@app.route("/reset_password_email", methods=['GET', 'POST'])
def reset_password_email():
    """Sends password-reset email to user"""
    if current_user.is_authenticated:
        return redirect(url_for("search_home"))
    form = EmailResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f"An email has been sent to {form.email.data}", 'success')
        return redirect(url_for("login"))
    return render_template("reset_password_email.html", form=form)


@app.route("/change_pass/<token>", methods=['GET', 'POST'])
def reset_password(token):
    """validates token, sends form to change password, POST requests reset password"""
    if current_user.is_authenticated:
        return redirect(url_for("search_home"))

    user = User.verify_reset_token(token)
    if user is None:
        flash("The session has expired. Please try again", 'warning')
        return redirect(url_for("reset_email"))

    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_password = form.password.data
        hashed_password = u.hash_password(new_password)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been changed. Please log in", 'success')
        return redirect(url_for("login"))
    return render_template("change_password.html", form=form)


@app.route('/logout')
def logout():
    """Logs out the user"""
    logout_user()
    return redirect(url_for("show_homepage"))

# ^ SEARCHING THE DATABASE:


@app.route("/search_home", methods=['GET', 'POST'])
@login_required
def search_home():
    form = SearchType()
    if form.is_submitted():
        type = form.search_type.data
        if type == "specific":
            return redirect(url_for("search_specific_official"))
        if type == "officials":
            return redirect(url_for("search_general_officials"))
        if type == "v2":
            return redirect(url_for("search_V2"))
    return render_template("search_home.html", form=form)


@app.route("/search_specific_official", methods=['GET', 'POST'])
@login_required
def search_specific_official():
    form = SpecificNameForm()
    if form.is_submitted():
        session["payload"] = form.data
        name = form.last_name.data
        print(f"******{session['payload']}")
        if name == '':
            flash('Enter A Name', 'danger')
            return redirect(url_for('search_home'))
        # session['payload']= form.data
        
        if filter.check_for_duplicate_names(name):
            return redirect(url_for('multiple_names', last=name))
        else:
            full_name = filter.get_official_by_last_name(name)
            return redirect(url_for("link_name_search", name=full_name))
    return render_template("search_specific_official.html", form=form)


@app.route("/multiple_names/<last>")
def multiple_names(last):
    matches = filter.get_identical_names(last)
    print(f"**********{matches}")
    return render_template('multiple_names.html', matches=matches)


@app.route("/search_general_officials", methods=['GET', 'POST'])
def search_general_officials():
    form = GeneralNameForm()
    exec_jobs = filter.find_all_exec()
    form.exec_jobs.choices = [(item, item) for item in exec_jobs]
    if form.is_submitted():
        session["payload"] = form.data
        payload = session["payload"]
        print(f"**********{payload}")
        results = filter.narrow_by_official_general(payload)
        return render_template("general_official_results.html", results = results)
    return render_template("search_general_official.html", form=form)

@app.route("/branch.json")
def dropdown():
    branch = request.args.get('branch')
    if branch == "E":
        
        hide = {"#show_height": "height", "#show_district": "district", "#show_court": "court"}
        values = {"#height": "height", "#district": "district", "#court": "court"}
        show = {"#show_exec_jobs": "show_exec_jobs"}

        
    if branch == 'J':
        hide = {"#show_height": "height", "#show_district": "district", "#show_exec_jobs": "exec"}
        values = {"#height": "height", "#district": "district", "#exec_jobs": "exec_jobs"}
        show = {"#show_court": "court"}
    
    if branch == "L":
        hide = {"#show_exec_jobs": "exec", "#show_court": "court"}
        values = {"#exec_jobs": "exec_jobs", "#court": "court"}
        show = {"#show_height": "height", "#show_district": "district"}
    return jsonify({"hide": hide, "n_values": values, "show": show})


@app.route("/search_general_donors", methods = ['GET', 'POST'])
def search_general_donors():
    pass


# SEARCH RESULTS BY NAME
@app.route("/name_search")
@login_required
def name_search():
    name = request.args.get("name")
    position = filter.get_position_name(name)
    donations = filter.get_all_by_official_name(name)
    return render_template("name_results.html", donations=donations, name=name, position=position)

@app.route("/name_search/<name>")
@login_required
def link_name_search(name):
    payload = session["payload"]
    payload["official_name"] = name
    print(f"*******This is the payload: {payload}")
    donations = filter.narrow_by_official_specific(payload)
    print(f"*****{len(donations)}")
    position = filter.get_position_name(name)
    return render_template("name_results.html", donations=donations, name=name, position=position)


# ^ V2 SEARCH FUNCTIONS

@app.route('/search_V2', methods=['GET', 'POST'])
def test_table():
    form = TestForm()
    if form.is_submitted():
        session['params'] = form.data
        return redirect(url_for('show_V2_table'))
    return render_template("general_official_search_v2.html", form=form)
    

@app.route('/v2_table')
def show_V2_table():
    return render_template('v2_table.html')

@app.route('/api/data1')
def data():
    payload = session['params']
    query = filter.test_filter(payload)
    

    # search filter
    search = request.args.get('search[value]')
    search = search.upper()
    if search:
        query = query.filter(db.or_(
            Official.official_name.like(f'%{search}%'),
            Donor.donor_name.like(f'%{search}%')
        ))
    total_filtered = query.count()


    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    results = filter.response_to_dict(query)


    # response
    return {
        'data': results,
        'recordsFiltered': total_filtered,
        'recordsTotal': Donation.query.count(),
        'draw': request.args.get('draw', type=int),
    }



# SEARCH RESULTS BY DISTRICT
@app.route("/district_search")
@login_required
def district_search():
    district = request.args.get("district")
    official_objs = filter.get_by_district(district)
    return render_template("district_results.html", official_objs=official_objs, district=district)

# SEARCH RESULTS BY POSITION
@app.route("/position_search")
@login_required
def position_search():
    position = request.args.get("position")
    pols = filter.get_by_job(position)
    return render_template("position_results.html", position=position, pols=pols)

@app.route("/position_search/<position>")
@login_required
def link_position_search(position):
    pols = filter.get_by_job(position)
    return render_template("position_results.html", position=position, pols=pols)

# SEARCH RESULTS BY DONOR
@app.route("/donor_search")
@login_required
def donor_name_search():
    donor_name = request.args.get("donor_name")
    donations = filter.get_by_donor_name(donor_name)
    return render_template("donor_results.html", donor_name=donor_name, donations=donations)

@app.route("/donor_search/<donor_name>")
@login_required
def link_donor_name_search(donor_name):
    donations = filter.get_by_donor_name(donor_name)
    return render_template("donor_results.html", donor_name=donor_name, donations=donations)
    

# SEARCH RESULT BY BUSINESS SECTOR
@app.route("/sector_search")
@login_required
def sector_search():
    sector = request.args.get("sector")
    donor_objs = filter.get_by_sector(sector)
    return render_template("sector_results.html", sector=sector, donor_objs=donor_objs)


# #Login stuff needs to be at bottom for reasons unexplainable

