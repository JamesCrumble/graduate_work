from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from settings import settings

from .abc_message import AbstractMessage, log


class Email(AbstractMessage):

    async def send(self, user_id: str, task_id: str):
        if not settings.sg_api_key:
            log.info('Sendgrid api key is not specified')
            return

        try:
            title, body = await self._get_msg_content(task_id)
        except Exception as exc:
            log.error(exc)
            await self._failed_sent(user_id, task_id)

        message = Mail(
            from_email=settings.from_email,

            # Using only because idea is get email from auth db (not from api). So please, dont't blame a lot <3
            to_emails='test@yandex.com',
            subject=title,
            html_content=body
        )
        try:
            sg = SendGridAPIClient(settings.sg_api_key)
            response = sg.send(message)

            log.info(f'Sendgrid status code: {response.status_code=}. {user_id=} {task_id=}')
            log.debug(f'Sendgrid message body: {response.body}')
            log.debug(f'Sendgrid headers:\n {response.headers}')

            await self._successful_sent(user_id, task_id)
        except Exception as exc:
            log.error(exc)
            await self._failed_sent(user_id, task_id)
