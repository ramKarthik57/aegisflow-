from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# SQLite database file path in server directory
DATABASE_URL = "sqlite:///./aegisflow.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False) # "dispatcher" or "admin"

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(20), default="Active")
    priority = Column(String(20), default="Medium")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    transcript = Column(Text, nullable=False)
    summary = Column(Text)
    category = Column(String(50))
    victim_count = Column(Integer, default=0)
    hazards = Column(Text) # JSON string array
    recommended_units = Column(Text) # JSON string array
    dispatched_responders = Column(Text, default="[]") # JSON string list of IDs
    reasoning = Column(Text) # Explainability details
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Responder(Base):
    __tablename__ = "responders"
    id = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False) # EMS, Fire, Police
    status = Column(String(50), default="Available") # Available, Dispatched, Offline
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    user = Column(String(50), nullable=False)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Pre-populate responders if database is empty
    if db.query(Responder).count() == 0:
        responders = [
            Responder(id="AMB-01", name="Ambulance 01 (Gachibowli)", type="EMS", status="Available", latitude=17.4401, longitude=78.3489),
            Responder(id="FIRE-02", name="Fire Engine 02 (Jubilee Hills)", type="Fire", status="Available", latitude=17.4319, longitude=78.4075),
            Responder(id="POLICE-03", name="Police Cruiser 03 (Madhapur)", type="Police", status="Available", latitude=17.4483, longitude=78.3741),
            Responder(id="AMB-04", name="Ambulance 04 (Secunderabad)", type="EMS", status="Available", latitude=17.4399, longitude=78.4983),
            Responder(id="FIRE-05", name="Fire Engine 05 (Charminar)", type="Fire", status="Available", latitude=17.3616, longitude=78.4747),
        ]
        db.add_all(responders)
        
    # Pre-populate some historical mock incidents for stats/filters
    if db.query(Incident).count() == 0:
        historical_incidents = [
            Incident(
                status="Resolved",
                priority="High",
                latitude=17.4450,
                longitude=78.3800,
                transcript="There's an elderly gentleman having shortness of breath near Cyber Towers.",
                summary="Elderly male with severe respiratory distress treated and transported.",
                category="Medical Emergency",
                victim_count=1,
                hazards='["Hypoxia"]',
                recommended_units='["EMS"]',
                dispatched_responders='["AMB-01"]',
                reasoning="Caller reported shortness of breath in elderly patient. High cardiac risk indicator.",
                created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=5)
            ),
            Incident(
                status="Resolved",
                priority="Medium",
                latitude=17.4200,
                longitude=78.4100,
                transcript="Minor fender bender blocking one lane on Road No 36.",
                summary="Two-car collision, no injuries, traffic managed.",
                category="Traffic Accident",
                victim_count=0,
                hazards='["Traffic Obstruction"]',
                recommended_units='["Police"]',
                dispatched_responders='["POLICE-03"]',
                reasoning="Fender bender with no injuries. Classified as medium priority due to road blockage.",
                created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=8)
            )
        ]
        db.add_all(historical_incidents)
        
    # Pre-populate default users (password bcrypt hashed: 'aegis123')
    if db.query(User).count() == 0:
        # Hashed password for 'aegis123' using a simple hash check for mock bcrypt inside database file
        # We can use passlib.hash.bcrypt or a standard hash. Let's use bcrypt hash for security
        from passlib.hash import pbkdf2_sha256
        users = [
            User(username="dispatcher", password_hash=pbkdf2_sha256.hash("aegis123"), role="dispatcher"),
            User(username="admin", password_hash=pbkdf2_sha256.hash("aegis123"), role="admin"),
        ]
        db.add_all(users)

    db.commit()
    db.close()
