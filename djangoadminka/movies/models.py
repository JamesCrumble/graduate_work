import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Templates(CreatedMixin, UpdatedMixin):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(_('Name'), max_length=255)
    template_title = models.CharField(_('Title of template'), max_length=255)
    template_text = models.TextField(_('Text of template'))

    class Meta:
        db_table = "content\".\"template"
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self) -> str:
        return self.name


class NotificationTasks(UUIDMixin, CreatedMixin, UpdatedMixin):

    class States(models.TextChoices):
        DELIVERED = 'D', _('Delivered')
        QUEUED = 'Q', _('Queued')
        CANCELED = 'C', _('Canceled')

    class Channels(models.TextChoices):
        SMS = 'S', _('SMS')
        EMAIL = 'E', _('eMail')
        PHONE = 'P', _('Phone')

    template_id = models.ForeignKey('Templates', on_delete=models.CASCADE)
    state = models.CharField(
        max_length=1,
        choices=States.choices,
        default=States.QUEUED,
    )
    is_broadcast = models.BooleanField(_('is Broadcast'))
    body = models.JSONField(_('Notification body'))
    importance = models.SmallIntegerField(_('Importance'))
    channel = models.CharField(
        max_length=1,
        choices=Channels.choices,
        default=Channels.EMAIL,
    )
    datetime_of_dispatch = models.DateTimeField(_('Time of dispatch'), null=True, blank=True)
    datetime_when_sended = models.DateTimeField(_('Sended at'), null=True, blank=True)

    class Meta:
        db_table = "content\".\"notificationtask"
        verbose_name = _('Notification task')
        verbose_name_plural = _('Notification tasks')

    def __str__(self) -> str:
        return self.state


class NotificationStatus(UUIDMixin, CreatedMixin):

    class Statuses(models.TextChoices):
        DELIVERED = 'D', _('Delivered')
        WITHERROR = 'E', _('Error')
        INITIATED = 'I', _('Initiated')
        READED = 'R', _('Readed')

    user_id = models.UUIDField(_('User ID'))
    notification_tasks_id = models.ForeignKey('NotificationTasks', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=Statuses.choices,
        default=Statuses.INITIATED,
    )

    class Meta:
        db_table = "content\".\"notificationstatus"
        verbose_name = _('Notification status')
        verbose_name_plural = _('Notification statuses')

    def __str__(self) -> str:
        return self.status
