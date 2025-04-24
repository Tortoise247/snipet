import requests  # Add this import for Redmine API interaction
import json  # For saving and loading window position
import email
import os

import os
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button
from tkinterdnd2 import TkinterDnD, DND_FILES
from email import policy
from email.parser import BytesParser


POSITION_FILE = "window_position.json"


def save_window_position(x, y):
    """Save the window position to a file."""
    with open(POSITION_FILE, "w") as f:
        json.dump({"x": x, "y": y}, f)

def load_window_position():
    """Load the window position from a file."""
    if os.path.exists(POSITION_FILE):
        with open(POSITION_FILE, "r") as f:
            try:
                position = json.load(f)
                return position.get("x", 100), position.get("y", 100)
            except json.JSONDecodeError:
                pass
    return 100, 100  # Default position if no file exists or error occurs

def register_to_redmine(subject, body):
    """Register the EML content to Redmine as a new issue."""
    # Redmine API configuration
    REDMINE_URL = "http://localhost:3000"
    API_KEY = "a685044e79fef4bbd77d57886afe06d4ba09dbe6"
    PROJECT_ID = "dummy"

    # API endpoint for creating an issue
    url = f"{REDMINE_URL}/issues.json"

    # Issue data
    data = {
        "issue": {
            "project_id": PROJECT_ID,
            "subject": subject,
            "description": body
        }
    }

    # Headers for authentication and content type
    headers = {
        "X-Redmine-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    # Send the POST request
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Issue successfully created in Redmine!")
        else:
            messagebox.showerror("Error", f"Failed to create issue: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")




