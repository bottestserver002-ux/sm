from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
import calendar
from datetime import timedelta

from database import get_db

from models import (
    PlanningMonth,
    PlanningWeek,
    PlanningDay,
    PlanningTask
)

from schemas import (
    MonthCreate,
    MonthUpdate,

    WeekCreate,
    WeekUpdate,

    DayCreate,
    DayUpdate,

    TaskCreate,
    TaskUpdate
)

router = APIRouter(
    prefix="/planning",
    tags=["Planning"]
)

@router.post("/month")
def create_month(
    data: MonthCreate,
    db: Session = Depends(get_db)
):

    month = PlanningMonth(

        user_id=data.user_id,

        title=data.title,

        goal=data.goal,

        note=data.note,

        start_date=data.start_date,

        end_date=data.end_date

    )

    db.add(month)

    db.commit()

    db.refresh(month)

    return month

@router.get("/month/{user_id}")
def get_months(
    user_id:int,
    db:Session=Depends(get_db)
):

    return db.query(
        PlanningMonth
    ).filter(

        PlanningMonth.user_id==user_id

    ).order_by(

        PlanningMonth.start_date.desc()

    ).all()

@router.get("/month/detail/{id}")
def get_month(
    id:int,
    db:Session=Depends(get_db)
):

    return db.query(

        PlanningMonth

    ).filter(

        PlanningMonth.id==id

    ).first()

@router.put("/month/{id}")
def update_month(
    id:int,
    data:MonthUpdate,
    db:Session=Depends(get_db)
):

    month=db.query(

        PlanningMonth

    ).filter(

        PlanningMonth.id==id

    ).first()

    if not month:

        return {
            "message":"Không tìm thấy"
        }

    month.title=data.title

    month.goal=data.goal

    month.note=data.note

    month.start_date=data.start_date

    month.end_date=data.end_date

    month.status=data.status

    db.commit()

    return{

        "message":"Cập nhật thành công"

    }

@router.delete("/month/{id}")
def delete_month(
    id:int,
    db:Session=Depends(get_db)
):

    month=db.query(

        PlanningMonth

    ).filter(

        PlanningMonth.id==id

    ).first()

    if not month:

        return{

            "message":"Không tìm thấy"

        }

    db.delete(month)

    db.commit()

    return{

        "message":"Đã xóa"

    }


@router.post("/week")
def create_week(
    data:WeekCreate,
    db:Session=Depends(get_db)
):

    week=PlanningWeek(

        month_id=data.month_id,

        title=data.title,

        week_number=data.week_number,

        goal=data.goal,

        note=data.note

    )

    db.add(week)

    db.commit()

    db.refresh(week)

    return week


@router.get("/week/{month_id}")
def get_weeks(
    month_id:int,
    db:Session=Depends(get_db)
):

    return db.query(

        PlanningWeek

    ).filter(

        PlanningWeek.month_id==month_id

    ).order_by(

        PlanningWeek.week_number

    ).all()


@router.get("/week/detail/{id}")
def get_week(
    id:int,
    db:Session=Depends(get_db)
):

    return db.query(

        PlanningWeek

    ).filter(

        PlanningWeek.id==id

    ).first()

@router.put("/week/{id}")
def update_week(
    id: int,
    data: WeekUpdate,
    db: Session = Depends(get_db)
):

    week = db.query(
        PlanningWeek
    ).filter(
        PlanningWeek.id == id
    ).first()

    if not week:
        return {
            "message": "Không tìm thấy tuần"
        }

    week.title = data.title
    week.week_number = data.week_number
    week.goal = data.goal
    week.note = data.note
    week.status = data.status

    db.commit()

    return {
        "message": "Cập nhật thành công"
    }

@router.delete("/week/{id}")
def delete_week(
    id: int,
    db: Session = Depends(get_db)
):

    week = db.query(
        PlanningWeek
    ).filter(
        PlanningWeek.id == id
    ).first()

    if not week:
        return {
            "message": "Không tìm thấy tuần"
        }

    db.delete(week)

    db.commit()

    return {
        "message": "Đã xóa"
    }

@router.post("/day")
def create_day(
    data: DayCreate,
    db: Session = Depends(get_db)
):

    day = PlanningDay(

        week_id=data.week_id,

        date=data.date,

        title=data.title,

        goal=data.goal,

        note=data.note

    )

    db.add(day)

    db.commit()

    db.refresh(day)

    return day

@router.get("/day/{week_id}")
def get_days(
    week_id: int,
    db: Session = Depends(get_db)
):

    return db.query(

        PlanningDay

    ).filter(

        PlanningDay.week_id == week_id

    ).order_by(

        PlanningDay.date

    ).all()

@router.get("/day/detail/{id}")
def get_day(
    id: int,
    db: Session = Depends(get_db)
):

    return db.query(

        PlanningDay

    ).filter(

        PlanningDay.id == id

    ).first()

@router.put("/day/{id}")
def update_day(
    id: int,
    data: DayUpdate,
    db: Session = Depends(get_db)
):

    day = db.query(
        PlanningDay
    ).filter(
        PlanningDay.id == id
    ).first()

    if not day:

        return {
            "message": "Không tìm thấy"
        }

    day.date = data.date
    day.title = data.title
    day.goal = data.goal
    day.note = data.note
    day.status = data.status

    db.commit()

    return {
        "message": "Cập nhật thành công"
    }

@router.delete("/day/{id}")
def delete_day(
    id: int,
    db: Session = Depends(get_db)
):

    day = db.query(
        PlanningDay
    ).filter(
        PlanningDay.id == id
    ).first()

    if not day:

        return {
            "message": "Không tìm thấy"
        }

    db.delete(day)

    db.commit()

    return {
        "message": "Đã xóa"
    }

@router.post("/task")
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db)
):

    task = PlanningTask(

        day_id=data.day_id,

        title=data.title,

        description=data.description,

        location=data.location,

        position=data.position,

        partner=data.partner,

        start_time=data.start_time,

        end_time=data.end_time,

        deadline=data.deadline,

        priority=data.priority,

        note=data.note,

        status="Todo",

        completed=False

    )

    db.add(task)

    db.commit()

    db.refresh(task)

    return task

@router.get("/task/{day_id}")
def get_tasks(
    day_id: int,
    db: Session = Depends(get_db)
):

    return db.query(

        PlanningTask

    ).filter(

        PlanningTask.day_id == day_id

    ).order_by(

        PlanningTask.start_time

    ).all()

@router.get("/task/detail/{id}")
def get_task(
    id: int,
    db: Session = Depends(get_db)
):

    return db.query(

        PlanningTask

    ).filter(

        PlanningTask.id == id

    ).first()

@router.put("/task/{id}")
def update_task(
    id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = db.query(
        PlanningTask
    ).filter(
        PlanningTask.id == id
    ).first()

    if not task:

        return {
            "message": "Không tìm thấy Task"
        }

    task.title = data.title

    task.description = data.description

    task.location = data.location

    task.position = data.position

    task.partner = data.partner

    task.start_time = data.start_time

    task.end_time = data.end_time

    task.deadline = data.deadline

    task.priority = data.priority

    task.status = data.status

    task.completed = data.completed

    task.note = data.note

    db.commit()

    return {

        "message": "Cập nhật thành công"

    }

@router.delete("/task/{id}")
def delete_task(
    id: int,
    db: Session = Depends(get_db)
):

    task = db.query(

        PlanningTask

    ).filter(

        PlanningTask.id == id

    ).first()

    if not task:

        return {

            "message": "Không tìm thấy"

        }

    db.delete(task)

    db.commit()

    return {

        "message": "Đã xóa"

    }

@router.put("/task/complete/{id}")
def complete_task(
    id: int,
    db: Session = Depends(get_db)
):

    task = db.query(

        PlanningTask

    ).filter(

        PlanningTask.id == id

    ).first()

    if not task:

        return {

            "message": "Không tìm thấy"

        }

    task.completed = not task.completed

    if task.completed:

        task.status = "Done"

    else:

        task.status = "Doing"

    db.commit()

    return {

        "message": "OK",

        "completed": task.completed

    }

@router.get("/today/{user_id}")
def today_task(
    user_id: int,
    db: Session = Depends(get_db)
):

    today = date.today()

    return (

        db.query(PlanningTask)

        .join(PlanningDay)

        .join(PlanningWeek)

        .join(PlanningMonth)

        .filter(

            PlanningMonth.user_id == user_id,

            PlanningDay.date == today

        )

        .order_by(

            PlanningTask.start_time

        )

        .all()

    )

# ==========================================================
# DASHBOARD
# ==========================================================

@router.get("/dashboard/{user_id}")
def dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):

    today = date.today()

    tasks = (

        db.query(PlanningTask)

        .join(PlanningDay)

        .join(PlanningWeek)

        .join(PlanningMonth)

        .filter(

            PlanningMonth.user_id == user_id,

            PlanningDay.date == today

        )

        .all()

    )

    total = len(tasks)

    completed = len(

        [t for t in tasks if t.completed]

    )

    doing = len(

        [t for t in tasks if not t.completed]

    )

    expired = len(

        [

            t

            for t in tasks

            if t.deadline

            and t.deadline < datetime.utcnow()

            and not t.completed

        ]

    )

    progress = 0

    if total > 0:

        progress = round(

            completed / total * 100,

            1

        )

    return {

        "today": str(today),

        "tasks": total,

        "completed": completed,

        "doing": doing,

        "expired": expired,

        "progress": progress

    }

# ==========================================================
# PROGRESS
# ==========================================================

@router.get("/progress/{user_id}")
def progress(
    user_id: int,
    db: Session = Depends(get_db)
):

    tasks = (

        db.query(PlanningTask)

        .join(PlanningDay)

        .join(PlanningWeek)

        .join(PlanningMonth)

        .filter(

            PlanningMonth.user_id == user_id

        )

        .all()

    )

    total = len(tasks)

    completed = len(

        [x for x in tasks if x.completed]

    )

    doing = len(

        [x for x in tasks if not x.completed]

    )

    expired = len(

        [

            x

            for x in tasks

            if x.deadline

            and x.deadline < datetime.utcnow()

            and not x.completed

        ]

    )

    percent = 0

    if total:

        percent = round(

            completed / total * 100,

            1

        )

    return {

        "total": total,

        "completed": completed,

        "doing": doing,

        "expired": expired,

        "progress": percent

    }

# ==========================================================
# CALENDAR
# ==========================================================

@router.get("/calendar/{user_id}")
def calendar(
    user_id: int,
    db: Session = Depends(get_db)
):

    days = (

        db.query(PlanningDay)

        .join(PlanningWeek)

        .join(PlanningMonth)

        .filter(

            PlanningMonth.user_id == user_id

        )

        .all()

    )

    return [

        {

            "id": day.id,

            "date": day.date,

            "title": day.title

        }

        for day in days

    ]

# ==========================================================
# EXPIRED
# ==========================================================

@router.get("/expired/{user_id}")
def expired(
    user_id: int,
    db: Session = Depends(get_db)
):

    return (

        db.query(PlanningTask)

        .join(PlanningDay)

        .join(PlanningWeek)

        .join(PlanningMonth)

        .filter(

            PlanningMonth.user_id == user_id,

            PlanningTask.deadline < datetime.utcnow(),

            PlanningTask.completed == False

        )

        .order_by(

            PlanningTask.deadline

        )

        .all()

    )

# ==========================================================
# UPCOMING
# ==========================================================

@router.get("/upcoming/{user_id}")
def upcoming(
    user_id: int,
    db: Session = Depends(get_db)
):

    return (

        db.query(PlanningTask)

        .join(PlanningDay)

        .join(PlanningWeek)

        .join(PlanningMonth)

        .filter(

            PlanningMonth.user_id == user_id,

            PlanningTask.completed == False

        )

        .order_by(

            PlanningTask.deadline

        )

        .limit(10)

        .all()

    )

# ==========================================================
# SEARCH
# ==========================================================

@router.get("/search/{user_id}")
def search(
    user_id: int,
    keyword: str,
    db: Session = Depends(get_db)
):

    return (

        db.query(PlanningTask)

        .join(PlanningDay)

        .join(PlanningWeek)

        .join(PlanningMonth)

        .filter(

            PlanningMonth.user_id == user_id,

            PlanningTask.title.ilike(

                f"%{keyword}%"

            )

        )

        .all()

    )

# ==========================================================
# MONTH STATISTICS
# ==========================================================

@router.get("/month/stat/{month_id}")
def month_stat(
    month_id: int,
    db: Session = Depends(get_db)
):

    tasks = (

        db.query(PlanningTask)

        .join(PlanningDay)

        .join(PlanningWeek)

        .filter(

            PlanningWeek.month_id == month_id

        )

        .all()

    )

    total = len(tasks)

    done = len(

        [x for x in tasks if x.completed]

    )

    doing = total - done

    return {

        "total": total,

        "done": done,

        "doing": doing

    }

@router.post("/month/{month_id}/generate")
def generate_month(
    month_id: int,
    db: Session = Depends(get_db)
):

    month = db.query(
        PlanningMonth
    ).filter(
        PlanningMonth.id == month_id
    ).first()

    if not month:
        return {
            "message": "Không tìm thấy tháng"
        }

    year = month.start_date.year
    month_number = month.start_date.month

    total_days = calendar.monthrange(
        year,
        month_number
    )[1]

    week_map = {}

    for day in range(1, total_days + 1):

        current = date(
            year,
            month_number,
            day
        )

        week_number = ((day - 1) // 7) + 1

        if week_number not in week_map:

            week = PlanningWeek(

                month_id=month.id,

                title=f"Tuần {week_number}",

                week_number=week_number

            )

            db.add(week)

            db.commit()

            db.refresh(week)

            week_map[week_number] = week

        planning_day = PlanningDay(

            week_id=week_map[week_number].id,

            date=current,

            title=current.strftime("%d/%m/%Y")

        )

        db.add(planning_day)

    db.commit()

    return {
        "message": "Đã tạo lịch tháng"
    }

@router.post("/week/{week_id}/duplicate")
def duplicate_week(
    week_id: int,
    db: Session = Depends(get_db)
):

    week = db.query(
        PlanningWeek
    ).filter(
        PlanningWeek.id == week_id
    ).first()

    if not week:
        return {
            "message": "Không tìm thấy tuần"
        }

    new_week = PlanningWeek(

        month_id=week.month_id,

        title=f"Tuần {week.week_number + 1}",

        week_number=week.week_number + 1,

        goal=week.goal,

        note=week.note

    )

    db.add(new_week)

    db.commit()

    db.refresh(new_week)

    for day in week.days:

        new_day = PlanningDay(

            week_id=new_week.id,

            date=day.date + timedelta(days=7),

            title=day.title,

            goal=day.goal,

            note=day.note

        )

        db.add(new_day)

        db.commit()

        db.refresh(new_day)

        for task in day.tasks:

            new_task = PlanningTask(

                day_id=new_day.id,

                title=task.title,

                description=task.description,

                location=task.location,

                position=task.position,

                partner=task.partner,

                start_time=task.start_time,

                end_time=task.end_time,

                deadline=None,

                priority=task.priority,

                status="Todo",

                completed=False,

                note=task.note

            )

            db.add(new_task)

    db.commit()

    return {
        "message": "Đã sao chép tuần"
    }