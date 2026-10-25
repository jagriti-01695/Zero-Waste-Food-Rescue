from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
load_dotenv()

from config import Config
from forms import RegistrationForm, LoginForm, FoodForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

saved_food = db.Table('saved_food',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    foods = db.relationship('Food', backref='donor', lazy=True)
    requests = db.relationship('Request', backref='receiver', lazy=True)
    saved_foods = db.relationship('Food', secondary=saved_food, lazy='subquery',
        backref=db.backref('saved_by', lazy=True))

    @property
    def average_rating(self):
        ratings = Rating.query.filter_by(donor_id=self.id).all()
        if not ratings:
            return 0
        return round(sum(r.score for r in ratings) / len(ratings), 1)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)  
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default="Available") 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = db.Column(db.String(50), nullable=True) # Storing as string for simplicity (YYYY-MM-DD)
    cost_type = db.Column(db.String(50), nullable=False, default='Free')
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)

   
    food = db.relationship('Food', backref='requests', lazy=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def check_expiries():
    expired = False
    for food in Food.query.filter_by(status='Available').all():
        if food.expiry_date:
            try:
                expiry_dt = datetime.strptime(food.expiry_date, '%Y-%m-%dT%H:%M')
                if datetime.now() > expiry_dt:
                    food.status = 'Expired'
                    expired = True
            except ValueError:
                pass
    if expired:
        db.session.commit()

@app.route('/')
def home():
    check_expiries()
    foods = Food.query.all()
    
    now = datetime.now()
    for f in foods:
        f.is_expiring_soon = False
        f.formatted_expiry = f.expiry_date
        if f.expiry_date:
            try:
                exp_time = datetime.strptime(f.expiry_date, '%Y-%m-%dT%H:%M')
                diff = exp_time - now
                if diff.total_seconds() > 0:
                    if diff.days == 0:
                        hours = int(diff.total_seconds() // 3600)
                        mins = int((diff.total_seconds() % 3600) // 60)
                        if hours > 0:
                            f.formatted_expiry = f"in {hours}h {mins}m"
                        else:
                            f.formatted_expiry = f"in {mins}m"
                    elif diff.days == 1:
                        f.formatted_expiry = f"Tomorrow, {exp_time.strftime('%I:%M %p')}"
                    else:
                        f.formatted_expiry = exp_time.strftime('%b %d, %I:%M %p')
                    
                    if f.status == 'Available' and diff.total_seconds() < 12 * 3600:
                        f.is_expiring_soon = True
                else:
                    f.formatted_expiry = "Expired"
            except ValueError:
                pass

    def sort_key(f):
        status_order = {'Available': 0, 'Requested': 1, 'Completed': 2, 'Expired': 3}
        exp_time = datetime.max
        if f.expiry_date:
            try:
                exp_time = datetime.strptime(f.expiry_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass
        return (status_order.get(f.status, 4), exp_time)

    foods.sort(key=sort_key)
    
    return render_template('home.html', foods=foods)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered! Please login.", "warning")
            return redirect(url_for('login'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, role=form.role.data) # type: ignore
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        flash("Invalid credentials", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home'))


@app.route('/add_food', methods=['GET', 'POST'])
@login_required
def add_food():
    if current_user.role not in ["donor", "admin"]:
        flash("Only donors can add food!", "danger")
        return redirect(url_for('home'))

    form = FoodForm()
    if form.validate_on_submit():
        image_file = 'default.jpg'
        if form.image.data:
            file = form.image.data
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file = filename

        food = Food(title=form.title.data, description=form.description.data, location=form.location.data, # type: ignore
                    donor_id=current_user.id, expiry_date=form.expiry_date.data, cost_type=form.cost_type.data, image_file=image_file) # type: ignore
        db.session.add(food)
        db.session.commit()
        flash("Food added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_food.html', form=form)

@app.route('/edit_food/<int:food_id>', methods=['GET', 'POST'])
@login_required
def edit_food(food_id):
    if current_user.role not in ["donor", "admin"]:
        flash("Only donors can edit food!", "danger")
        return redirect(url_for('home'))

    food = Food.query.get_or_404(food_id)
    if food.donor_id != current_user.id and current_user.role != 'admin':
        flash("You can only edit your own donations!", "danger")
        return redirect(url_for('dashboard'))

    form = FoodForm()
    if request.method == 'GET':
        form.title.data = food.title
        form.description.data = food.description
        form.location.data = food.location
        form.cost_type.data = food.cost_type
        form.expiry_date.data = food.expiry_date

    if form.validate_on_submit():
        food.title = form.title.data
        food.description = form.description.data
        food.location = form.location.data
        food.cost_type = form.cost_type.data
        food.expiry_date = form.expiry_date.data
        
        if form.image.data:
            file = form.image.data
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            food.image_file = filename

        db.session.commit()
        flash("Food updated successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('edit_food.html', form=form, food=food)


@app.route('/delete_food/<int:food_id>', methods=['POST'])
@login_required
def delete_food(food_id):
    if current_user.role not in ["donor", "admin"]:
        flash("Only donors can delete food!", "danger")
        return redirect(url_for('home'))

    food = Food.query.get_or_404(food_id)
    if food.donor_id != current_user.id and current_user.role != 'admin':
        flash("You can only delete your own donations!", "danger")
        return redirect(url_for('dashboard'))

    Request.query.filter_by(food_id=food.id).delete()
    
    for user in food.saved_by:
        user.saved_foods.remove(food)

    db.session.delete(food)
    db.session.commit()
    flash("Food deleted successfully!", "success")
    return redirect(url_for('dashboard'))


@app.route('/request_food/<int:food_id>', methods=['POST'])
@login_required
def request_food(food_id):
    if current_user.role != "receiver":
        flash("Only receivers can request food!", "danger")
        return redirect(url_for('home'))

    food = Food.query.get_or_404(food_id)
    
    if food.donor_id == current_user.id:
        flash("You cannot request your own food listing!", "danger")
        return redirect(url_for('home'))
    if food.status != "Available":
        flash("This food is not available anymore.", "warning")
        return redirect(url_for('home'))

    food.status = "Requested"
    new_request = Request(receiver_id=current_user.id, food_id=food_id) # type: ignore
    db.session.add(new_request)
    db.session.commit()
    flash("Food requested successfully!", "success")
    return redirect(url_for('home'))


@app.route('/complete_food/<int:food_id>', methods=['POST'])
@login_required
def complete_food(food_id):
    food = Food.query.get_or_404(food_id)
    if current_user.id != food.donor_id:
        flash("Not allowed!", "danger")
        return redirect(url_for('home'))

    food.status = "Completed"
    db.session.commit()
    flash("Food marked as completed!", "success")
    return redirect(url_for('home'))

@app.route('/my_food_requests')
@login_required
def my_food_requests():
    if current_user.role != "donor":
        flash("Only donors can view requests!", "danger")
        return redirect(url_for('home'))

    requests = Request.query.join(Food).filter(Food.donor_id == current_user.id).all()
    return render_template('my_requests.html', requests=requests)



@app.route('/dashboard')
@login_required
def dashboard():
    check_expiries()
    if current_user.role == "donor":
        donated_foods = Food.query.filter_by(donor_id=current_user.id).all()
        active_requests = Request.query.join(Food).filter(Food.donor_id == current_user.id, Food.status == "Requested").all()
        return render_template('dashboard.html', donated_foods=donated_foods, active_requests=active_requests)
    else:
        requested_foods = Request.query.filter_by(receiver_id=current_user.id).all()
        return render_template('dashboard.html', requested_foods=requested_foods)

@app.route('/save_food/<int:food_id>', methods=['POST'])
@login_required
def save_food(food_id):
    food = Food.query.get_or_404(food_id)
    if food in current_user.saved_foods:
        current_user.saved_foods.remove(food)
        action = "unsaved"
    else:
        current_user.saved_foods.append(food)
        action = "saved"
    db.session.commit()
    flash(f"Food {action} successfully!", "success")
    return redirect(url_for('home'))

@app.route('/rate_donor/<int:donor_id>', methods=['POST'])
@login_required
def rate_donor(donor_id):
    if current_user.role != 'receiver':
        flash('Only receivers can rate donors.', 'danger')
        return redirect(url_for('dashboard'))

    score = int(request.form.get('score', 0))
    if score < 1 or score > 5:
        flash('Invalid rating score.', 'danger')
        return redirect(url_for('dashboard'))
        
    rating = Rating(donor_id=donor_id, receiver_id=current_user.id, score=score) # type: ignore
    db.session.add(rating)
    db.session.commit()
    flash('Rating submitted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
        
    users = User.query.all()
    foods = Food.query.all()
    return render_template('admin_dashboard.html', users=users, foods=foods)

@app.route('/admin/delete_food/<int:food_id>', methods=['POST'])
@login_required
def admin_delete_food(food_id):
    if current_user.role != 'admin':
        return redirect(url_for('home'))
        
    food = Food.query.get_or_404(food_id)
    Request.query.filter_by(food_id=food.id).delete()
    for user in food.saved_by:
        user.saved_foods.remove(food)
    db.session.delete(food)
    db.session.commit()
    flash('Food listing deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('home'))
        
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete yourself.", "warning")
        return redirect(url_for('admin_dashboard'))
        
    # Delete related requests
    Request.query.filter((Request.receiver_id == user.id)).delete()
    # Delete related foods
    foods = Food.query.filter_by(donor_id=user.id).all()
    for f in foods:
        Request.query.filter_by(food_id=f.id).delete()
        for u in f.saved_by:
            u.saved_foods.remove(f)
        db.session.delete(f)
        
    Rating.query.filter((Rating.donor_id == user.id) | (Rating.receiver_id == user.id)).delete()
    
    db.session.delete(user)
    db.session.commit()
    flash('User and all associated records deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Auto-initialize database on application startup
with app.app_context():
    db.create_all()
    try:
        if User.query.count() == 0:
            from seed_amritsar import seed_database
            seed_database()
    except Exception as e:
        app.logger.warning(f"Initial seed check skipped: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(host='0.0.0.0', port=port, debug=debug)
