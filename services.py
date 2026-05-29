from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, schemas

def create_screening(db: Session, screening_data: schemas.ScreeningCreate):
    db_screening = models.Screening(**screening_data.model_dump())
    db.add(db_screening)
    db.commit()
    db.refresh(db_screening)
    return db_screening

def get_all_screenings(db: Session):
    return db.query(models.Screening).all()

def delete_screening(db: Session, screening_id: int):
    screening = db.query(models.Screening).filter(models.Screening.id == screening_id).first()
    if not screening:
        raise HTTPException(status_code=404, detail="Nie znaleziono takiego seansu")
    db.delete(screening)
    db.commit()
    return {"message": "Seans został pomyślnie usunięty"}

def make_reservation(db: Session, reservation_data: schemas.ReservationCreate, user_id: int):
    screening = db.query(models.Screening).filter(models.Screening.id == reservation_data.screening_id).first()
    if not screening:
        raise HTTPException(status_code=404, detail="Seans o podanym ID nie istnieje")
    if reservation_data.seat_number > screening.total_seats:
        raise HTTPException(status_code=400, detail=f"Błędny numer miejsca. Ta sala ma tylko {screening.total_seats} miejsc.")

    existing_res = db.query(models.Reservation).filter(
        models.Reservation.screening_id == reservation_data.screening_id,
        models.Reservation.seat_number == reservation_data.seat_number
    ).first()
    
    if existing_res:
        raise HTTPException(status_code=422, detail="To miejsce jest już zarezerwowane przez kogoś innego!")

    db_res = models.Reservation(**reservation_data.model_dump(), user_id=user_id)
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res