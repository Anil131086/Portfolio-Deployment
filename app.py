from flask import Flask, request, jsonify, send_from_directory, make_response
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import jwt
from datetime import datetime, timedelta
import json
import traceback

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
SPREADSHEET_ID = '1HrNDI-Gm_Tmg0SUSe1Aa2mWxyftnTdOJc7OPmZHBMCo'

# Update range names for different sheets
LOGIN_RANGE = 'Sheet1!A:B'  # For existing login credentials
REGISTER_RANGE = 'Sheet2!A:C'  # New sheet for registration (includes email)

def get_google_sheets_service():
    try:
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        # Get credentials from environment variable
        creds_json = os.environ.get('GOOGLE_CREDENTIALS')
        if creds_json:
            creds_dict = json.loads(creds_json)
            creds = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=SCOPES)
        else:
            # Fallback to file for local development
            creds_path = os.environ.get('CREDENTIALS_PATH', r'C:\Users\hp\Desktop\Python Key\united-time-403410-8e2ac45d1b99.json')
            if not os.path.exists(creds_path):
                print(f"Error: Credentials not found in environment or at {creds_path}")
                return None
            
            creds = service_account.Credentials.from_service_account_file(
                creds_path, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=creds)
        print("Successfully connected to Google Sheets API")
        return service
    except Exception as e:
        print(f"Error setting up Google Sheets service: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

@app.route('/')
def serve_index():
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        print(f"Error serving index: {str(e)}")
        return str(e), 500

@app.route('/register')
def serve_register():
    try:
        return send_from_directory('static', 'register.html')
    except Exception as e:
        print(f"Error serving register page: {str(e)}")
        return str(e), 500

@app.route('/portfolio')
def serve_portfolio():
    try:
        return send_from_directory('static', 'portfolio.html')
    except Exception as e:
        print(f"Error serving portfolio: {str(e)}")
        return str(e), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('static', path)
    except Exception as e:
        print(f"Error serving static file {path}: {str(e)}")
        return str(e), 404

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Received login request with data: {data}")
        
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})

        username = data.get('username')
        password = data.get('password')
        remember_me = data.get('remember_me', False)

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'})

        service = get_google_sheets_service()
        if not service:
            return jsonify({'success': False, 'message': 'Could not connect to Google Sheets'})

        print(f"Fetching data from sheet: {SPREADSHEET_ID}, range: {LOGIN_RANGE}")
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=LOGIN_RANGE).execute()
        values = result.get('values', [])

        if not values:
            return jsonify({'success': False, 'message': 'No data found in spreadsheet'})

        # Check credentials against Google Sheet data
        for row in values:
            if len(row) >= 2 and row[0] == username and row[1] == password:
                response = jsonify({'success': True, 'message': 'Login successful'})
                
                if remember_me:
                    token = generate_token(username)
                    response.set_cookie('remember_token', token, max_age=30*24*60*60)  # 30 days
                
                return response

        return jsonify({'success': False, 'message': 'Invalid credentials'})

    except Exception as e:
        print(f"Login error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'message': 'An error occurred during login'})

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Received registration request with data: {data}")
        
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({'success': False, 'message': 'All fields are required'})

        service = get_google_sheets_service()
        if not service:
            return jsonify({'success': False, 'message': 'Could not connect to Google Sheets'})

        # Check if username already exists
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=LOGIN_RANGE
        ).execute()
        existing_users = result.get('values', [])
        
        if any(row[0] == username for row in existing_users if row):
            return jsonify({'success': False, 'message': 'Username already exists'})

        # Add new user to both sheets
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=LOGIN_RANGE,
            valueInputOption='RAW',
            body={'values': [[username, password]]}
        ).execute()

        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=REGISTER_RANGE,
            valueInputOption='RAW',
            body={'values': [[username, email, password]]}
        ).execute()

        return jsonify({'success': True, 'message': 'Registration successful'})

    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'message': 'An error occurred during registration'})

@app.route('/logout', methods=['POST'])
def logout():
    try:
        response = make_response(jsonify({'success': True, 'message': 'Logged out successfully'}))
        response.delete_cookie('remember_token')
        return response
    except Exception as e:
        print(f"Error during logout: {str(e)}")
        return jsonify({'success': False, 'message': 'Error during logout'})

@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        # Here you can add code to handle the contact form submission
        # For example, send an email or store in Google Sheets
        print(f"Received contact form submission: {data}")
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({'success': False, 'message': 'Error sending message'})

def generate_token(username):
    token = jwt.encode({
        'user': username,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Static folder path: {os.path.abspath('static')}")
    try:
        # Test Google Sheets connection
        service = get_google_sheets_service()
        if service:
            print("Successfully connected to Google Sheets")
        else:
            print("Warning: Could not connect to Google Sheets")
            
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
