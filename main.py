import asyncio
import logging
from datetime import datetime

import schedule
from aiogram import Bot, Dispatcher
from loguru import logger

from config import BOT_TOKEN, notifications, topics, weekday_dict

logging.basicConfig(level=logging.INFO)
logger.add(
    'logging/logs.log',
    format='<green>{time:DD-MM-YYYY HH:mm:ss.SSS}</green> | <level>{level: <8}</level>'\
        ' | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '\
        '<level>{message}</level>',
    level='INFO',
)
notification_jobs: list[schedule.Job] = []
main_tasks: set[asyncio.Task] = set()

if BOT_TOKEN is not None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()


def get_notification_schedule() -> dict:
    today = datetime.now().strftime('%d.%m.%y')
    current_weekday = weekday_dict[datetime.now().strftime('%w')]

    if today in notifications.get('пн,вт,ср,чт,пт', {}).get('excluded_dates', []):
        return notifications.get('сб,вс', {})
    elif today in notifications.get('сб,вс', {}).get('excluded_dates', []):
        return notifications.get('пн,вт,ср,чт,пт', {})
    elif current_weekday in ['пн', 'вт', 'ср', 'чт', 'пт']:
        return notifications.get('пн,вт,ср,чт,пт', {})
    else:
        return notifications.get('сб,вс', {})


async def send_notification(chat_id: int, thread_id: int, message: str) -> None:
    try:
        await bot.send_message(
            chat_id=chat_id, text=message, message_thread_id=thread_id
        )
        logger.info(
            f'SendMessage group_id={chat_id}, subgroup_id={thread_id}, {message=}'
        )
    except Exception as e:
        logger.error(
            f'Failed to send message to group_id={chat_id}, '\
            f'subgroup_id={thread_id}. Error: {e}'
        )


async def scheduler() -> None:
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logger.error(f'Error in scheduler: {e}')
        await asyncio.sleep(1)


def schedule_notifications() -> None:
    logger.info('Clear jobs')
    for job in notification_jobs:
        schedule.cancel_job(job)
    notification_jobs.clear()

    notification_schedule = get_notification_schedule()

    logger.info('Creating new jobs')
    for time, message in notification_schedule.items():
        if time != 'excluded_dates':
            try:
                datetime.strptime(time, '%H:%M')
            except ValueError as ve:
                logger.error(f'Invalid time format: {time}. Error: {ve}')
                continue

            for group_name, data in topics.items():
                group_id = data.get('group_id')
                subgroups = data.get('subgroups')

                if group_id is None or not isinstance(group_id, int):
                    logger.error(f'Invalid group_id for group {group_name}')
                    continue
                if subgroups is None or not isinstance(subgroups, dict):
                    logger.error(f'Invalid subgroups for group {group_name}')
                    continue

                for subgroup_name, subgroup_id in subgroups.items():
                    job = (
                        schedule.every()
                        .day.at(time)
                        .do(
                            asyncio.create_task,
                            send_notification(group_id, subgroup_id, message),
                        )
                    )
                    notification_jobs.append(job)
                    logger.info(
                        f'Notification for {time}, group {group_name} (ID={group_id}),'\
                        f' topic {subgroup_name} (ID={subgroup_id}) scheduled'
                    )


def schedule_refresh() -> None:
    schedule.every().day.at('00:01').do(schedule_notifications)


async def main() -> None:
    schedule_refresh()
    logger.info('Schedule for notifications at 00:01 added')
    schedule_notifications()
    logger.info('Initial schedule creation completed')
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f'Error during polling: {e}')


if __name__ == '__main__':
    logger.info('Bot started!')
    logger.info(f'BOT_TOKEN={BOT_TOKEN}')
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(scheduler())
        loop.run_until_complete(main())
    except RuntimeError as e:
        logger.error(f'RuntimeError: {e}')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
