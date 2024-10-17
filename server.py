from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)
CORS(app)

# PostgreSQL database connection string from Render
engine = create_engine('postgresql://portfolio_db_cjbj_user:53neyS5lEX4iQVzLUpxtOsiXElplgVzD@dpg-cs8itc23esus73aqlbu0-a.frankfurt-postgres.render.com:5432/portfolio_db_cjbj')

# Base for declarative models
Base = declarative_base()

# Define the 'messages' table with a timestamp field
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Add timestamp with default as current time (UTC)

# Create the table in the database
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)

@app.route('/send_message', methods=['POST'])
def send_message():
    session = Session()  # Create a new session for this request
    data = request.json  # Retrieve JSON data from the frontend
    name = data.get('name')
    email = data.get('email')
    description = data.get('description')

    # Create a new message object with timestamp and add it to the database
    new_message = Message(name=name, email=email, description=description)
    try:
        session.add(new_message)
        session.commit()  # Save the new message in the database
        return jsonify({"message": "Message received!"}), 200
    except Exception as e:
        session.rollback()  # Roll back in case of an error
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()  # Always close the session

@app.route('/get_messages', methods=['GET'])
def get_messages():
    session = Session()  # Create a new session for this request
    try:
        # Query all the messages from the database
        messages = session.query(Message).all()

        # Return the messages in JSON format, including the timestamp
        return jsonify([{
            'date_time': message.timestamp.strftime("%d/%m/%Y %H:%M:%S"),  # Format the timestamp for output
            'name': message.name,
            'email': message.email,
            'description': message.description
        } for message in messages]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()  # Always close the session

if __name__ == '__main__':
    app.run(debug=True)
