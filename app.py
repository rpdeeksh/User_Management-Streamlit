# Import Streamlit and other necessary libraries
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("your_connection_string")
db = client["Your_Database_Name"]["Your_Collection_Name"]

# Streamlit UI for User Management
st.title("User Management Console using NoSQL")

# Add User Section
st.header("Add User")
name = st.text_input("Name")
email = st.text_input("Email")
age = st.number_input("Age", min_value=0)

if st.button("Add User"):
    db.insert_one({"name": name, "email": email, "age": int(age)})
    st.success("User added successfully!")

# Display Users
st.header("Current Users")
users = list(db.find())
if users:
    for user in users:
        st.write(f"ID: {user['_id']} | Name: {user['name']} | Email: {user['email']} | Age: {user['age']}")

        if st.button(f"Delete {user['_id']}", key=str(user['_id']) + "_delete"):
            db.delete_one({"_id": ObjectId(user['_id'])})
            st.success("User deleted successfully!")
            st.session_state.user_data = None  # Clear the user_data to refresh UI

# Update User Section
st.header("Edit User")
user_id = st.text_input("Enter User ID to Update")

# Initialize session state for user_data if it doesn’t exist
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# Search User
if st.button("Search User"):
    user = db.find_one({"_id": ObjectId(user_id)})
    if user:
        st.session_state.user_data = user
    else:
        st.error("User not found!")

# Display update form if user_data is present in session_state
if st.session_state.user_data:
    updated_name = st.text_input("Name", value=st.session_state.user_data['name'])
    updated_email = st.text_input("Email", value=st.session_state.user_data['email'])
    updated_age = st.number_input("Age", value=st.session_state.user_data['age'], step=1)

    if st.button("Update User"):
        try:
            db.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"name": updated_name, "email": updated_email, "age": int(updated_age)}}
            )
            st.success("User updated successfully!")
            st.session_state.user_data = None  # Reset user data to clear the form
        except Exception as e:
            st.error(f"Failed to update user: {e}")
