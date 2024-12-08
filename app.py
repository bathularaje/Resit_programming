from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Initialize the Flask application and set up the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Company data model
class CompanyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    details = db.Column(db.Text, nullable=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_data.id'), nullable=False)

class SalesPipeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deal_name = db.Column(db.String(120), nullable=False)
    stage = db.Column(db.String(120), nullable=False)
    value = db.Column(db.Float, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_data.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    due_date = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_data.id'), nullable=False)

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_by = db.Column(db.String(120), nullable=False)
    date_sent = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_data.id'), nullable=False)

# Define Forms for each page
class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    type = StringField('Company Type', validators=[DataRequired()])
    details = TextAreaField('Details')
    submit = SubmitField('Save')

class ContactForm(FlaskForm):
    name = StringField('Contact Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone')
    address = StringField('Address')
    submit = SubmitField('Save')

class SalesPipelineForm(FlaskForm):
    deal_name = StringField('Deal Name', validators=[DataRequired()])
    stage = StringField('Stage', validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Save')

class TaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    due_date = StringField('Due Date', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Save')

class EmailLogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    sent_by = StringField('Sent By', validators=[DataRequired()])
    date_sent = StringField('Date Sent', validators=[DataRequired()])
    submit = SubmitField('Save')

# Route for Home page
@app.route('/')
def home():
    return render_template('login.html')

# Route for Company Data
@app.route('/company', methods=['GET', 'POST'])
def company_data():
    form = CompanyForm()
    if form.validate_on_submit():
        company = CompanyData(name=form.name.data, type=form.type.data, details=form.details.data)
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('company_data'))
    return render_template('company_data.html', form=form)

# Route for Contacts
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print("Request method:", request.method)
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            company_id=1
        )
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('contact'))

    contacts = Contact.query.all()
    return render_template('contact.html', form=form, contacts=contacts)


# Route for Sales Pipeline
@app.route('/sales-pipeline', methods=['GET', 'POST'])
def sales_pipeline():
    form = SalesPipelineForm()
    if form.validate_on_submit():
        pipeline = SalesPipeline(deal_name=form.deal_name.data, stage=form.stage.data, value=form.value.data, company_id=1)
        db.session.add(pipeline)
        db.session.commit()
        return redirect(url_for('sales_pipeline'))
    
    pipelines = SalesPipeline.query.all()  # Fetch all sales pipeline records
    return render_template('sales_pipeline.html', form=form, pipelines=pipelines)

# Route for Tasks
@app.route('/task', methods=['GET', 'POST'])
def task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(description=form.description.data, due_date=form.due_date.data, status=form.status.data, company_id=1)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('task'))
    
    tasks = Task.query.all()  # Fetch all tasks
    return render_template('task.html', form=form, tasks=tasks)

# Route for Email Logs
@app.route('/email-log', methods=['GET', 'POST'])
def email_log():
    form = EmailLogForm()
    if form.validate_on_submit():
        email_log = EmailLog(subject=form.subject.data, body=form.body.data, sent_by=form.sent_by.data, date_sent=form.date_sent.data, company_id=1)
        db.session.add(email_log)
        db.session.commit()
        return redirect(url_for('email_log'))
    
    email_logs = EmailLog.query.all()  # Fetch all email logs
    return render_template('email_log.html', form=form, email_logs=email_logs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("All fields are required!", "warning")
            return redirect(url_for('register'))
        
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash("Username already exists!", "danger")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('welcome'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    
    return render_template('login.html')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if 'username' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        details = request.form['details']

        if not name or not type_:
            flash("Name and Type are required fields!", "warning")
        else:
            new_data = CompanyData(name=name, type=type_, details=details)
            db.session.add(new_data)
            db.session.commit()
            flash("Data added successfully!", "success")

    company_data = CompanyData.query.all()
    return render_template('welcome.html', username=session['username'], company_data=company_data)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_data(id):
    data = CompanyData.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    flash("Data deleted successfully!", "success")
    return redirect(url_for('welcome'))

@app.route('/update', methods=['POST'])
def update_data():
    data_id = request.form['id']
    name = request.form['name']
    type_ = request.form['type']
    details = request.form['details']
    
    data = CompanyData.query.get_or_404(data_id)
    data.name = name
    data.type = type_
    data.details = details
    
    db.session.commit()
    flash("Data updated successfully!", "success")
    return redirect(url_for('welcome'))

# JSON API Endpoints
@app.route('/api/company-data', methods=['GET'])
def get_company_data():
    company_data = CompanyData.query.all()
    return jsonify([{
        'id': data.id,
        'name': data.name,
        'type': data.type,
        'details': data.details
    } for data in company_data])

@app.route('/api/company-data/<int:id>', methods=['GET'])
def get_single_company_data(id):
    data = CompanyData.query.get_or_404(id)
    return jsonify({
        'id': data.id,
        'name': data.name,
        'type': data.type,
        'details': data.details
    })

@app.route('/api/company-data', methods=['POST'])
def create_company_data():
    data = request.get_json()
    new_data = CompanyData(name=data['name'], type=data['type'], details=data.get('details'))
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Company data added successfully!'}), 201

@app.route('/api/company-data/<int:id>', methods=['PUT'])
def update_company_data(id):
    data = request.get_json()
    existing_data = CompanyData.query.get_or_404(id)
    
    existing_data.name = data['name']
    existing_data.type = data['type']
    existing_data.details = data.get('details')
    
    db.session.commit()
    return jsonify({'message': 'Company data updated successfully!'})

@app.route('/api/company-data/<int:id>', methods=['DELETE'])
def delete_company_data(id):
    data = CompanyData.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return jsonify({'message': 'Company data deleted successfully!'})




@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
