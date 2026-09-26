from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.auth import get_current_user
from app.database import get_session
from app.models import JobApplication, User
from app.schemas import (
    JobApplicationCreate,
    JobApplicationOut,
    JobApplicationUpdate,
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post(
    "/",
    response_model=JobApplicationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application: JobApplicationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_application = JobApplication(
        **application.model_dump(),
        user_id=current_user.id,
    )

    session.add(new_application)
    session.commit()
    session.refresh(new_application)

    return new_application


@router.get("/", response_model=list[JobApplicationOut])
def get_all_applications(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    applications = session.exec(
        select(JobApplication).where(
            JobApplication.user_id == current_user.id
        )
    ).all()

    return applications


@router.get("/{application_id}", response_model=JobApplicationOut)
def get_one_application(
    application_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    application = session.get(JobApplication, application_id)

    if not application or application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    return application


@router.patch("/{application_id}", response_model=JobApplicationOut)
def update_application(
    application_id: int,
    application_update: JobApplicationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    application = session.get(JobApplication, application_id)

    if not application or application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    update_data = application_update.model_dump(exclude_unset=True)

    for field_name, value in update_data.items():
        setattr(application, field_name, value)

    session.add(application)
    session.commit()
    session.refresh(application)

    return application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    application = session.get(JobApplication, application_id)

    if not application or application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    session.delete(application)
    session.commit()

    return {
        "message": "Job application deleted successfully"
    }