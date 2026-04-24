from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user_package import UserPackage

router = APIRouter(prefix="/packages", tags=["User Packages"])


# 📦 CREATE PACKAGE
@router.post("/create")
def create_package(
    user_id: int,
    sessions: int = 10,
    db: Session = Depends(get_db)
):

    # 🔍 kullanıcıda zaten package var mı?
    existing = db.query(UserPackage).filter(
        UserPackage.user_id == user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already has a package"
        )

    package = UserPackage(
        user_id=user_id,
        total_sessions=sessions,
        remaining_sessions=sessions
    )

    db.add(package)
    db.commit()
    db.refresh(package)

    return {
        "message": "Package created successfully",
        "package_id": package.id,
        "total_sessions": package.total_sessions,
        "remaining_sessions": package.remaining_sessions
    }


# 📊 GET USER PACKAGE
@router.get("/user/{user_id}")
def get_user_package(user_id: int, db: Session = Depends(get_db)):

    package = db.query(UserPackage).filter(
        UserPackage.user_id == user_id
    ).first()

    if not package:
        raise HTTPException(
            status_code=404,
            detail="Package not found"
        )

    return package


# 🔁 DECREASE SESSION (BOOKING İÇİN KULLANILIR)
@router.post("/decrease/{user_id}")
def decrease_session(user_id: int, db: Session = Depends(get_db)):

    package = db.query(UserPackage).filter(
        UserPackage.user_id == user_id
    ).first()

    if not package:
        raise HTTPException(
            status_code=404,
            detail="Package not found"
        )

    if package.remaining_sessions <= 0:
        raise HTTPException(
            status_code=400,
            detail="No remaining sessions"
        )

    package.remaining_sessions -= 1

    db.add(package)
    db.commit()
    db.refresh(package)

    return {
        "message": "Session decreased",
        "remaining_sessions": package.remaining_sessions
    }