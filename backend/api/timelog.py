from fastapi import APIRouter
from ..utils import engine
from sqlmodel import Session, select, SQLModel
from ..utils import engine
from ..models.user import User
from ..models.timelog import TimeLog

router = APIRouter(prefix="/api/timelogs")

session = Session(engine)


# Post timelog
@router.post("/")
async def timelog(timelog: TimeLog):
    startt_to_dt = string_to_datetime(timelog.start_time)
    # Timelog.month
    month_from_dt = startt_to_dt.month
    # Timelog.year
    year_from_dt = startt_to_dt.year
    # Timelog.work_hours
    work_delta = string_to_datetime(timelog.end_time) - string_to_datetime(
        timelog.start_time
    )
    work_delta_hours = work_delta.seconds / 3600
    work_hours = "{:.2f}".format(work_delta_hours)

    # count_days = work_hours / 8

    new_timelog = TimeLog(
        id=timelog.id,
        user_id=timelog.user_id,
        username=timelog.username,
        start_time=timelog.start_time,
        end_time=timelog.end_time,
        client_id=timelog.client_id,
        epic_id=timelog.epic_id,
        epic_name=timelog.epic_name,
        count_hours=12.12,
        count_days=13.13,
        daily_value=11.11,
        month=month_from_dt,
        year=year_from_dt,
    )

    session.add(new_timelog)
    session.commit()
    return True


# Get list of timelogs
@router.get("/lists/{username},{epic_name},{month}")
async def get_timelog_list(
    username: str = None, epic_name: str = None, month: int = None
):
    if username != None:
        if epic_name != None:
            if month != None:
                statement = (
                    select(TimeLog)
                    .where(TimeLog.username == username)
                    .where(TimeLog.epic_name == epic_name)
                    .where(TimeLog.month == month)
                )
            else:
                statement = (
                    select(TimeLog)
                    .where(TimeLog.username == username)
                    .where(TimeLog.epic_name == epic_name)
                )
        else:
            statement = (
                select(TimeLog)
                .where(TimeLog.username == username)
                .where(TimeLog.month == month)
            )
    else:
        statement = (
            select(TimeLog)
            .where(TimeLog.epic_name == epic_name)
            .where(TimeLog.month == month)
        )
    results = session.exec(statement).all()
    return results


# Update timelogs
@router.put("/")
async def update_timelogs(
    username: str = None,
    epic_name: str = None,
    date: str = None,
    start_time: str = None,
):
    date_dt = string_to_datetime(date)
    date_string = date_dt.date

    statement = (
        select(TimeLog)
        .where(TimeLog.username == username)
        .where(TimeLog.epic_name == epic_name)
    )
    timelog_to_update = session.exec(statement).one()
    timelog_to_update.start_time = start_time
    session.add(timelog_to_update)
    session.commit()
    session.refresh(timelog_to_update)
    return True


# Delete timelogs
@router.delete("/")
async def delete_timelogs(
    username: str = None,
    epic_name: str = None,
    date: str = None,
):
    statement = (
        select(TimeLog)
        .where(TimeLog.username == username)
        .where(TimeLog.epic_name == epic_name)
    )
    results = session.exec(statement)
    timelog_to_delete = results.one()
    session.delete(timelog_to_delete)
    session.commit()
