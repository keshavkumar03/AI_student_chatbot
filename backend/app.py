from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import google.generativeai as genai
from model.model import db
from model.model import Query
from model.user import User

app = Flask(__name__)
CORS(app)
API_KEY = "AIzaSyBV6x24Il9iVIV2o_3r5lJPO7rmdfYhTNM"
genai.configure(api_key=API_KEY)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///queries.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize the app with the database
db.init_app(app)

# Create all database tables before serving requests
with app.app_context():
    db.create_all()
    
    
@app.route('/', methods=['GET'])
def information():
    return jsonify({'message': 'Welcome to the student chatbot API!'})


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_username = data.get('username')
    new_password = data.get('password')

    user = User(username=new_username, password=new_password)
    db.session.add(user)
    db.session.commit()
    response = jsonify({"message": "User registered successfully"})
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow requests from any origin
    return response
    

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        response= jsonify({"message": "Login successful"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        response= jsonify({"message": "Invalid username or password"}), 401
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    

@app.route('/chat-history', methods=['GET'])
def get_chat_history():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401

    user_chats = Query.query.filter_by(user_id=current_user.id).all()
    chat_history = [{"timestamp": chat.timestamp, "input": chat.text} for chat in user_chats]

    return jsonify(chat_history)

@app.route('/generate-response', methods=['POST', 'OPTIONS'])
def generate_response():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
        return ('', 204, headers)
    data = request.get_json()
    input_text = data['input']
    new_query = Query(text=input_text)
    db.session.add(new_query)
    db.session.commit()
    input_prompt = f"""
    Hello Act Like a very skilled and A dedicated psychologist with significant experience
    in student mental health and counseling. Skilled in analyzing student mental health 
    issues and providing personalized tips and guidance for improvement. Committed to 
    enhancing the overall mental well-being of students within the educational environment.
    problem and description: {input_text}
    I want the response in one single string having the structure
    {{"problem Summary":"",how_normal:"", "how it can be improved": "", "the cause of the problem": "", "the potential solutions": ""}}
    """
    
    response = genai.GenerativeModel('gemini-pro').generate_content(input_prompt)
    response_json = json.loads(response.text)
    structured_response = {
        "problemSummary": response_json["problem Summary"],
        "howNormal": response_json["how_normal"],
        "howImproved": response_json["how it can be improved"],
        "causeOfProblem": response_json["the cause of the problem"],
        "potentialSolutions": response_json["the potential solutions"]
    }
    
    return jsonify(structured_response)

if __name__ == '__main__':
    app.run(debug=True)
