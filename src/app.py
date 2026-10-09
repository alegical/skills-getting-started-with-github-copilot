"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path


def normalize_email(email: str) -> str:
    return email.strip().lower()

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["alegical@gmail.com", "Alexa S"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["alegical2@gmail.com", "Ale S1"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["alegical3@gmail.com", "Ale S3"]
    },
    "Soccer Team": {
        "description": "Build teamwork and practice soccer skills in training and scrimmages",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["alegical4@gmail.com", "Ale S4"]
    },
    "Basketball Club": {
        "description": "Develop shooting, passing, and defensive skills through drills and games",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["alegical5@gmail.com", "Ale S5"]
    },
    "Drama Club": {
        "description": "Explore acting, scene work, and live performance techniques",
        "schedule": "Mondays and Wednesdays, 3:45 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["alegical6@gmail.com", "Ale S6"]
    },
    "Art Studio": {
        "description": "Create drawings, paintings, and mixed-media projects in a creative studio",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["alegical7@gmail.com", "Ale S7"]
    },
    "Math Olympiad": {
        "description": "Practice advanced problem solving and compete in mathematics challenges",
        "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
        "max_participants": 12,
        "participants": ["alegical8@gmail.com", "Ale S8"]
    },
    "Debate Team": {
        "description": "Research topics, build arguments, and compete in formal debate events",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["alegical9@gmail.com", "Ale S9"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    normalized_email = normalize_email(email)

    # Validate student is not already signed up
    if normalized_email in {normalize_email(participant) for participant in activity["participants"]}:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Validate activity has capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is already full")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = normalize_email(email)
    participant_emails = [normalize_email(participant) for participant in activity["participants"]]

    if normalized_email not in participant_emails:
        raise HTTPException(status_code=404, detail="Student is not signed up for this activity")

    for participant in list(activity["participants"]):
        if normalize_email(participant) == normalized_email:
            activity["participants"].remove(participant)
            break

    return {"message": f"Removed {normalized_email} from {activity_name}"}
