import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillswap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    skills_offered = db.relationship('Skill', backref='teacher', lazy=True, 
                                    foreign_keys='Skill.teacher_id')
    skills_wanted = db.relationship('Skill', backref='learner', lazy=True,
                                   foreign_keys='Skill.learner_id')
    
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    skill = db.relationship('Skill', backref='requests')
    requester = db.relationship('User', foreign_keys=[requester_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    request = db.relationship('Request', backref='messages')
    sender = db.relationship('User')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        user_exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if user_exists:
            flash('Username or email already exists!')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        bio = request.form.get('bio')
        user.bio = bio
        
        try:
            db.session.commit()
            flash('Profile updated successfully!')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
    
    skills_offered = Skill.query.filter_by(teacher_id=user.id).all()
    skills_wanted = Skill.query.filter_by(learner_id=user.id).all()
    
    return render_template('profile.html', user=user, 
                          skills_offered=skills_offered, 
                          skills_wanted=skills_wanted)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    all_skills = Skill.query.filter(Skill.teacher_id != session['user_id']).all()
    categories = set(skill.category for skill in Skill.query.all())
    
    return render_template('dashboard.html', skills=all_skills, categories=categories)

@app.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        skill_type = request.form.get('type')  # 'offer' or 'want'
        
        new_skill = Skill(
            name=name,
            description=description,
            category=category
        )
        
        if skill_type == 'offer':
            new_skill.teacher_id = session['user_id']
        else:
            new_skill.learner_id = session['user_id']
        
        try:
            db.session.add(new_skill)
            db.session.commit()
            flash('Skill added successfully!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')
            return redirect(url_for('add_skill'))
    
    return render_template('add_skill.html')

@app.route('/request_skill/<int:skill_id>', methods=['POST'])
def request_skill(skill_id):
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    skill = Skill.query.get_or_404(skill_id)
    
    if skill.teacher_id == session['user_id']:
        flash("You can't request your own skill!")
        return redirect(url_for('dashboard'))
    
    # Check if a request already exists
    existing_request = Request.query.filter_by(
        skill_id=skill_id,
        requester_id=session['user_id'],
        recipient_id=skill.teacher_id
    ).first()
    
    if existing_request:
        flash('You have already requested this skill!')
        return redirect(url_for('dashboard'))
    
    new_request = Request(
        skill_id=skill_id,
        requester_id=session['user_id'],
        recipient_id=skill.teacher_id
    )
    
    try:
        db.session.add(new_request)
        db.session.commit()
        flash('Skill request sent successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}')
    
    return redirect(url_for('dashboard'))

@app.route('/requests')
def manage_requests():
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    # Requests received by the user
    incoming_requests = Request.query.filter_by(recipient_id=session['user_id']).all()
    
    # Requests sent by the user
    outgoing_requests = Request.query.filter_by(requester_id=session['user_id']).all()
    
    return render_template('requests.html', 
                          incoming_requests=incoming_requests,
                          outgoing_requests=outgoing_requests)

@app.route('/update_request/<int:request_id>', methods=['POST'])
def update_request(request_id):
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    skill_request = Request.query.get_or_404(request_id)
    
    # Ensure the user owns this request
    if skill_request.recipient_id != session['user_id']:
        flash('Unauthorized action!')
        return redirect(url_for('manage_requests'))
    
    action = request.form.get('action')
    
    if action == 'accept':
        skill_request.status = 'accepted'
        flash('Request accepted!')
    elif action == 'reject':
        skill_request.status = 'rejected'
        flash('Request rejected!')
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}')
    
    return redirect(url_for('manage_requests'))

@app.route('/messages/<int:request_id>', methods=['GET', 'POST'])
def messages(request_id):
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    skill_request = Request.query.get_or_404(request_id)
    
    # Ensure the user is part of this request
    if not (skill_request.requester_id == session['user_id'] or skill_request.recipient_id == session['user_id']):
        flash('Unauthorized access!')
        return redirect(url_for('manage_requests'))
    
    # Ensure the request is accepted
    if skill_request.status != 'accepted':
        flash('You can only message if the request is accepted!')
        return redirect(url_for('manage_requests'))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if content:
            new_message = Message(
                request_id=request_id,
                sender_id=session['user_id'],
                content=content
            )
            
            try:
                db.session.add(new_message)
                db.session.commit()
                flash('Message sent!')
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}')
    
    messages = Message.query.filter_by(request_id=request_id).order_by(Message.created_at).all()
    other_user = skill_request.recipient if skill_request.requester_id == session['user_id'] else skill_request.requester
    
    return render_template('messages.html', 
                          request=skill_request,
                          messages=messages,
                          other_user=other_user)

@app.route('/api/filter_skills', methods=['POST'])
def filter_skills():
    category = request.json.get('category')
    search_term = request.json.get('search_term', '')
    
    query = Skill.query.filter(Skill.teacher_id != session['user_id'])
    
    if category and category != 'all':
        query = query.filter_by(category=category)
    
    if search_term:
        query = query.filter(Skill.name.contains(search_term) | Skill.description.contains(search_term))
    
    skills = query.all()
    
    result = []
    for skill in skills:
        result.append({
            'id': skill.id,
            'name': skill.name,
            'description': skill.description,
            'category': skill.category,
            'teacher': User.query.get(skill.teacher_id).username
        })
    
    return jsonify(result)

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)