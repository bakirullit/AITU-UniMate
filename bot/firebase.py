import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase app with your credentials
cred = credentials.Certificate('bot/config_files/firebase_security_key.json')

firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def check_user_exists(user_id):
    # Reference to the users collection
    users_ref = db.collection('users')

    # Query the user by their unique user_id
    user_doc = users_ref.document(str(user_id)).get()

    # Check if the document exists
    if user_doc.exists:
        return True  # User found
    else:
        return False 
# Function to add a new user to the database
def add_user(user_id, username, first_name, last_name, language_code, is_bot, timestamp, phone_number=None, role="Not Assigned"):
    users_ref = db.collection('users')
    users_ref.document(str(user_id)).set({
        'user_id': user_id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'language_code': language_code,
        'is_bot': is_bot,
        'timestamp': timestamp,
        'phone_number': phone_number,
        'role': role
    })

# Function to check if a user is an admin
def is_admin(user_id):
    user_ref = db.collection('users').document(str(user_id))
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict().get("role") == "admin"
    return False

# Function to update user role
def update_user_role(user_id, new_role):
    user_ref = db.collection('users').document(str(user_id))
    user_ref.update({"role": new_role})
    
# Function to get a list of all users
def get_all_users():
    users_ref = db.collection('users')
    users = users_ref.stream()
    return [user.to_dict() for user in users]

def get_user_role(user_id: str):
    """
    Retrieve the role of the user from Firebase.
    :param user_id: The user's unique Telegram ID.
    :return: The user's role (e.g., 'admin', 'student', etc.)
    """
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("role", "guest")  # Default to 'guest' if no role is found
    return "guest"  # Default if no user found

def store_message_data(user_id, message_name, message_id, chat_id):
    doc_ref = db.collection('messages').document(str(user_id))
    
    # Dynamically add the message_name as a field and save message_id and chat_id
    doc_ref.set({
        message_name: {
            'message_id': message_id,
            'chat_id': chat_id
        }
    }, merge=True) 

# Function to get saved message data from Firebase
def get_saved_message_data(chat_id):
    doc_ref = db.collection('messages').document(str(chat_id))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

async def delete_message(bot, logger, user_id, message_name):
    """
    Deletes a stored message for a user based on the message_name.
    
    Args:
        bot: The Aiogram bot instance.
        user_id: The Telegram user ID.
        message_name: The name of the message to delete.
    """
    try:
        doc_ref = db.collection('messages').document(str(user_id))
        doc = doc_ref.get()

        if doc.exists:
            message_data = doc.to_dict().get(message_name)

            if message_data:
                chat_id = message_data['chat_id']
                message_id = message_data['message_id']

                try:
                    # Delete the message using the bot instance
                    await bot.delete_message(chat_id=chat_id, message_id=message_id)
                    logger.info(f"Message '{message_name}' deleted for user {user_id}.")

                    # Remove the message from Firestore
                    doc_ref.update({message_name: firestore.DELETE_FIELD})
                except Exception as e:
                    logger.error(f"Failed to delete message '{message_name}' for user {user_id}: {e}")
            else:
                logger.warning(f"Message '{message_name}' not found for user {user_id}.")
        else:
            logger.warning(f"No Firestore document found for user {user_id}.")
    except Exception as e:
        logger.error(f"Error accessing Firestore for user {user_id}: {e}")

# Save Feedback in Firebase Firestore
from datetime import datetime

def save_feedback_to_database(user_id: int, feedback_type: str, feedback_text: str):
    try:
        feedback_ref = db.collection(feedback_type)
        feedback_data = {
            "user_id": user_id,
            "feedback_text": feedback_text,
            "timestamp": datetime.utcnow()  # Save the timestamp in UTC
        }
        
        # Add the feedback document to the Firestore collection
        feedback_ref.add(feedback_data)
        print("Feedback successfully saved to Firestore.")
    except Exception as e:
        print(f"Error saving feedback: {e}")

