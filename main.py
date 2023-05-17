from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waitlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class WaitlistEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    firm_website = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        firm_website = request.form['firm-website']
        title = request.form['title']
        country = request.form['country']

        entry = WaitlistEntry(firstname=firstname, lastname=lastname, email=email,
                              firm_website=firm_website, title=title, country=country)

        try:
            db.session.add(entry)
            db.session.commit()
            return render_template('popup.html')  # Render the popup.html template
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error"  # Return an error response if there was an exception

    else:
        return render_template('waitlist.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
