from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Table Blueprint
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Create tables automatically
with app.app_context():
    db.create_all()

# --- THE NEW REGISTRATION LOGIC ---
@app.route("/register", methods=["POST"])
def register_user():
    # 1. Grab the raw data sent by the user from the browser/form
    data = request.get_json()
    
    # 2. Extract the individual fields
    input_username = data.get('username')
    input_email = data.get('email')
    input_password = data.get('password')
    
    # 3. Validation: Make sure they didn't send blank details
    if not input_username or not input_email or not input_password:
        return jsonify({"message": "Error: All fields are required!"}), 400
        
    # 4. Check if the username or email already exists in our filing cabinet
    existing_user = User.query.filter((User.username == input_username) | (User.email == input_email)).first()
    if existing_user:
        return jsonify({"message": "Error: User or Email already registered!"}), 400

    # 5. Create a brand new record row based on our User layout
    new_user = User(username=input_username, email=input_email, password=input_password)
    
    # 6. Put the record inside the filing cabinet and click "Save Changes"
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Success: User registered successfully in the database!"}), 201

# Home route
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)