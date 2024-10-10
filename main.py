import asyncio
import logging
import schedule
from datetime import datetime

from aiogram import Bot, Dispatcher
from loguru import logger
from config import BOT_TOKEN, weekday_dict, notifications, topics

logging.basicConfig(level=logging.INFO)
logger.add(
        'logging/logs.log',
        format='<green>{time:DD-MM-YYYY HH:mm:ss.SSS}</green> | <level>{level: <8}'\
            '</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}'\
            '</cyan> - <level>{message}</level>',
        level='INFO',
    )
notification_jobs:list[schedule.Job] = []
main_tasks:set[asyncio.Task] = set()

if BOT_TOKEN is not None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

def get_notification_schedule() -> dict:
    today = datetime.now().strftime("%d.%m.%y")
    current_weekday = weekday_dict[datetime.now().strftime('%w')]

    if today in notifications["пн,вт,ср,чт,пт"]["excluded_dates"]:
        return notifications["сб,вс"]
    elif today in notifications["сб,вс"]["excluded_dates"]:
        return notifications["пн,вт,ср,чт,пт"]
    elif current_weekday in ["пн", "вт", "ср", "чт", "пт"]:
        return notifications["пн,вт,ср,чт,пт"]
    else:
        return notifications["сб,вс"]

async def send_notification(chat_id:int, thread_id:int, message:str) -> None:
    await bot.send_message(chat_id=chat_id, text=message, message_thread_id=thread_id)
    logger.info(
        f"[INFO] SendMessage group_id={chat_id}, subgroup_id={thread_id}, {message=}"
        )

async def scheduler() -> None:
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

def schedule_notifications() -> None:
    logger.info("[INFO] Clear jobs")
    for job in notification_jobs:
        schedule.cancel_job(job)

    notification_jobs.clear()
    notification_schedule = get_notification_schedule()
    logger.info("[INFO] Created new jobs")
    for time, message in notification_schedule.items():
        if time != "excluded_dates":
            for group_name, data in topics.items():
                group_id = data.get("group_id")
                subgroups = data.get("subgroups")
                if group_id is None or not isinstance(group_id, int):
                    raise ValueError("group_id value error")
                if subgroups is not None and isinstance(subgroups, dict):
                    for subgroup_name, subgroup_id in subgroups.items():
                        job = schedule.every().day.at(time).do(
                            asyncio.create_task,
                            send_notification(group_id, subgroup_id, message)
                            )
                        notification_jobs.append(job)
                        logger.info(
                            f"Notification work for the time {time}, for the group "\
                            f"{group_name} (ID={group_id}) the topic {subgroup_name} "\
                            f"(ID={subgroup_id}) was created successfully."
                            )

def schedule_refresh() -> None:
    schedule.every().day.at("00:01").do(schedule_notifications)

async def main() -> None:
    schedule_refresh()
    logger.info("[INFO] Schedule for notifications at 00:01 added")
    schedule_notifications()
    logger.info("[INFO] Initial schedule creation completed")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info("[Start] Bot started!")
    logger.info(f"[INFO] {BOT_TOKEN=}")
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    loop.run_until_complete(main())
