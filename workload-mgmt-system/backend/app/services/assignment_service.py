from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.staff_repository import StaffRepository
from app.repositories.task_repository import TaskRepository


class AssignmentService:

    @staticmethod
    def create_assignment(db: Session, data):
        staff = StaffRepository.get_by_id(db, data.staff_id)
        task = TaskRepository.get_by_id(db, data.task_id)

        if not staff or not task:
            raise HTTPException(status_code=404, detail="Staff or Task not found")

        # Hard qualification check (never overridden)
        if staff.qualification < task.required_qualification:
            raise HTTPException(status_code=400, detail="Qualification requirement not met")

        if task.category == "Teaching" and not data.override:
            if staff.role != "ACADEMIC":
                raise HTTPException(status_code=400, detail="Only academic staff can teach")

            if staff.department != task.department:
                raise HTTPException(status_code=400, detail="Department mismatch")

            if staff.specialty != task.required_specialty:
                raise HTTPException(status_code=400, detail="Specialty mismatch")

        if data.override and not data.override_reason:
            raise HTTPException(status_code=400, detail="Override reason required")

        assignment = Assignment(
            staff_id=data.staff_id,
            task_id=data.task_id,
            override=data.override,
            override_reason=data.override_reason,
            assigned_by="ADMIN" if data.override else "SYSTEM"
        )

        return AssignmentRepository.create(db, assignment)

    @staticmethod
    def update_assignment(db, assignment_id: int, data):
        assignment = AssignmentRepository.get_by_id(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        if data.override and not data.override_reason:
            raise HTTPException(
                status_code=400,
                detail="Override reason required when override is enabled"
            )

        for key, value in data.dict(exclude_unset=True).items():
            setattr(assignment, key, value)

        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def delete_assignment(db, assignment_id: int):
        assignment = AssignmentRepository.get_by_id(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        if assignment.status == "completed":
            raise HTTPException(
                status_code=400,
                detail="Completed assignments cannot be deleted"
            )

        AssignmentRepository.delete(db, assignment)
