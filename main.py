from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth, services, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Kino API")

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Użytkownik o takiej nazwie już istnieje")
    hashed = auth.hash_password(user_data.password)
    new_user = models.User(username=user_data.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "Zarejestrowano pomyślnie"}

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Niepoprawny login lub hasło")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/screenings", response_model=list[schemas.ScreeningResponse])
def read_screenings(db: Session = Depends(database.get_db)):
    return services.get_all_screenings(db)

@app.post("/screenings", response_model=schemas.ScreeningResponse, status_code=201)
def create_new_screening(screening: schemas.ScreeningCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return services.create_screening(db, screening)

@app.delete("/screenings/{screening_id}")
def delete_existing_screening(screening_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return services.delete_screening(db, screening_id)

@app.post("/reservations", status_code=201)
def book_ticket(reservation: schemas.ReservationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return services.make_reservation(db, reservation, current_user.id)