from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define the service table
class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    email = Column(String)
    written_details = Column(String)  # User's request details

# Define the complaint table
class Complaint(Base):
    __tablename__ = "complaint"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    email = Column(String)
    category = Column(String)         # Category of complaint (Electricity, Water, etc.)
    type = Column(String)             # Type of issue within category
    written_details = Column(String)  # User's complaint details

# Set up the database
DATABASE_URL = "sqlite:///./citizen_services.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

# Dependency to get DB session
# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Citizen Complaint and Service Request API"}
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ServiceRequest(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    written_details: str

class ComplaintRequest(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    category: str
    type: str
    written_details: str

# Endpoint for service requests
@app.post("/request-service/")
def request_service(service_request: ServiceRequest, db: Session = Depends(get_db)):
    service = Service(
        name=service_request.name,
        address=service_request.address,
        phone_number=service_request.phone_number,
        email=service_request.email,
        written_details=service_request.written_details,
    )
    db.add(service)
    db.commit()
    return {"message": "Service request has been recorded successfully"}

# Endpoint for complaints
@app.post("/raise-complaint/")
def raise_complaint(complaint_request: ComplaintRequest, db: Session = Depends(get_db)):
    complaint = Complaint(
        name=complaint_request.name,
        address=complaint_request.address,
        phone_number=complaint_request.phone_number,
        email=complaint_request.email,
        category=complaint_request.category,
        type=complaint_request.type,
        written_details=complaint_request.written_details,
    )
    db.add(complaint)
    db.commit()
    return {"message": "Complaint has been recorded successfully"}

def start_chat():
    # Initial Greeting and Options
    print("Welcome! How can we assist you today?")
    print("1. Request a Service")
    print("2. Raise a Complaint")

    choice = input("Please select an option (1 or 2): ")

    if choice == '1':
        request_service_interaction()
    elif choice == '2':
        raise_complaint_interaction()
    else:
        print("Invalid option, please try again.")

def request_service_interaction():
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    details = input("Describe the service you need: ")

    # Call the API or save in the database
    # This could be an API call to `/request-service/` with the details

    print("Your service request has been recorded successfully.")

def raise_complaint_interaction():
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")

    # Category Selection
    print("Select a category:")
    print("1. Electricity")
    print("2. Water")
    print("3. Waste")
    print("4. Road")
    print("5. Other")

    category_choice = input("Please select a category (1-5): ")
    categories = ["Electricity", "Water", "Waste", "Road", "Other"]
    category = categories[int(category_choice) - 1]

    # Type selection based on category
    type_options = {
        "Electricity": ["Street Lighting", "Frequent Cuts", "Frequent Low Voltage"],
        "Water": ["Poor Drainage", "Poor Quality Water", "No Availability of Water"],
        "Waste": ["Lack of Green Space", "Sewage Issues", "Waste Collection Service Issues", "Waste Accumulated at a Place"],
        "Road": ["Potholes", "Maintenance of Water", "Sidewalk Accessibility", "Traffic Congestion", "Public Transport"],
        "Other": ["Public Safety", "School Accessibility", "Healthcare Services", "Public Property Maintenance",
                  "Internet Connectivity", "Air Quality", "Noise Pollution", "Other"]
    }

    print("Select an issue type:")
    for i, type_option in enumerate(type_options[category], start=1):
        print(f"{i}. {type_option}")

    type_choice = input("Please select an issue type: ")
    type_of_issue = type_options[category][int(type_choice) - 1]

    complaint_details = input("Describe your complaint: ")

    # Call the API or save in the database
    # This could be an API call to `/raise-complaint/` with the details

    print("Your complaint has been recorded successfully.")
