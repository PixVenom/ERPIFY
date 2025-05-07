from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Define the database URL for MySQL
DATABASE_URL = "mysql+mysqlconnector://root:MySQLM4Pro@localhost/test"  # Replace with your MySQL credentials

# Create a SQLAlchemy engine.
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models.
Base = declarative_base()

# Define the Tea model as a SQLAlchemy model.
class Tea(Base):
    __tablename__ = "teas"  # Specify the table name

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # Added autoincrement
    name = Column(String, unique=True, index=True)  # Added unique constraint
    origin = Column(String)

    def __repr__(self):
        return f"<Tea(name='{self.name}', origin='{self.origin}')>"


# Create a database session.  This Session class is not the same as the Session type from typing.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables.  This should be done once when the application starts.
Base.metadata.create_all(bind=engine)

# Dependency to get a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Use Annotated to provide type hints for FastAPI's dependency injection.
db_dependency = Annotated[Session, Depends(get_db)]
app = FastAPI()


# Pydantic model for request validation.  This is separate from the SQLAlchemy model.
class TeaCreate(BaseModel):
    name: str
    origin: str


class TeaResponse(BaseModel):
    id: int
    name: str
    origin: str

    class Config:
        from_attributes = True  #  Enable mapping from SQLAlchemy model


@app.get("/")
def read_root():
    return {"message: Welcome to test backend"}



@app.post("/teas/", response_model=TeaResponse)
def create_tea(tea: TeaCreate, db: db_dependency):
    """
    Creates a new tea in the database.
    """
    db_tea = Tea(name=tea.name, origin=tea.origin)
    try:
        db.add(db_tea)
        db.commit()
        db.refresh(db_tea)  # Refresh to get the newly generated ID
        return db_tea
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tea name already exists")



@app.get("/teas/", response_model=List[TeaResponse])
def get_teas(db: db_dependency, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of teas from the database.
    """
    teas = db.query(Tea).offset(skip).limit(limit).all()
    return teas



@app.get("/teas/{tea_id}", response_model=TeaResponse)
def get_tea(tea_id: int, db: db_dependency):
    """
    Retrieves a specific tea by its ID.
    """
    tea = db.query(Tea).filter(Tea.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea



@app.put("/teas/{tea_id}", response_model=TeaResponse)
def update_tea(tea_id: int, updated_tea: TeaCreate, db: db_dependency):
    """
    Updates an existing tea in the database.
    """
    db_tea = db.query(Tea).filter(Tea.id == tea_id).first()
    if not db_tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    db_tea.name = updated_tea.name
    db_tea.origin = updated_tea.origin
    try:
        db.commit()
        db.refresh(db_tea)
        return db_tea
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tea name already exists")



@app.delete("/teas/{tea_id}", response_model=TeaResponse)
def delete_tea(tea_id: int, db: db_dependency):
    """
    Deletes a tea from the database.
    """
    db_tea = db.query(Tea).filter(Tea.id == tea_id).first()
    if not db_tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    db.delete(db_tea)
    db.commit()
    return db_tea  #  Return the deleted tea