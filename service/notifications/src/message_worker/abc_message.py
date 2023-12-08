import logging
from abc import ABC, abstractmethod

from core.psql import async_service_session_maker
from jinja2 import Template
from models import NotificationStatus, NotificationTask, NotifiedStatus
from models import Template as TemplateModel
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger('Messaging')

TITLE = str
BODY = str


class AbstractMessage(ABC):

    def __init__(self) -> None:
        self._session = async_service_session_maker()

    async def _get_msg_content(self, task_id: str) -> tuple[TITLE, BODY]:
        async with self._session:
            res = await self._session.execute(
                select(TemplateModel.template_title, TemplateModel.template_text, NotificationTask.body)
                .join(TemplateModel.id == NotificationTask.template_id)
                .where(NotificationTask.id == task_id)
            ).first()
        if res is None:
            raise TemplateBuildingError(f'Cannot build template by "{task_id=}" due nullable result')

        try:
            template_title, template_text, body = res
            return Template(template_title).render(**body), Template(template_text).render(**body)
        except BaseException as exc:
            raise TemplateBuildingError(f'Cannot build template by "{task_id=}" due error => {exc}')

    async def _failed_sent(self, user_id: str, task_id: str):
        try:
            stmt = (
                update(NotificationStatus).
                where(NotificationStatus.user_id == user_id, NotificationStatus.notification_task_id == task_id).
                values(status=NotifiedStatus.FAILED.value)
            )
            async with self._session:
                await self._session.execute(stmt)
                await self._session.commit()
        except SQLAlchemyError as err:
            log.error(f'Cannot update successfull status "{user_id=}", "{task_id=}" => {err}')

    async def _successful_sent(self, user_id: str, task_id: str):
        try:
            stmt = (
                update(NotificationStatus).
                where(NotificationStatus.user_id == user_id, NotificationStatus.notification_task_id == task_id).
                values(status=NotifiedStatus.DELIVERED.value)
            )
            async with self._session:
                await self._session.execute(stmt)

                await self._session.commit()
        except SQLAlchemyError as err:
            log.error(f'Cannot update successful status "{user_id=}", "{task_id=}" => {err}')

    @abstractmethod
    async def send(self, user_id: str, task_id: str, subject: str = ''):
        ...


class TemplateBuildingError(Exception):
    ...
