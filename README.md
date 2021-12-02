# georgiadaddy
Flask Rest API to search campaign finance data in the state of Georgia.
The data used is not allowed to be shared by request of FollowTheMoney.org. However, the data consists of just over 137,000 records parsed into a PostgreSQL database. Users can search the database by various parameters to browse the data or return specific records.

## Features and Tech Stack
- Python/Flask/PostgreSQL backend (Flask-SQLAlchemy as the ORM)
- JS/Jinja/Ajax frontend
- Salted and hashed passwords (Werkzeug)
- Password reset sent via email with timed token (itsdangerous and Flask-Mail)
- Datatables with server-side processing (Datatables.js)

- HTML forms handled with Flask-WTForms
- Login handled with Flask-Login


## Demo Link
https://youtu.be/TTflUgY-iLg
