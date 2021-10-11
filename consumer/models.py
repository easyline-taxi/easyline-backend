from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import uuid

# ! External Model
from api.models import User

class Client(models.Model):
    # Client Websocket
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=200)
    created_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return str(self.channel)



# def _default_channel_expiry_time():
#     return timezone.now() + timezone.timedelta(seconds=86400)


# def _default_message_expiry_time():
#     return timezone.now() + timezone.timedelta(minutes=1)

# class GroupChannel(models.Model):
#     group_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
#     channel = models.CharField(_("Channel Name"), max_length=50)
#     expire = models.DateTimeField(_("Expires"), default=_default_channel_expiry_time)

#     def __str__(self):
#         return str(self.channel)


# class Message(models.Model):
#     channel = models.ForeignKey("GroupChannel", verbose_name=_("ChannelId"), on_delete=models.CASCADE)
#     message = models.TextField(_("message"))
#     expire = models.DateTimeField(_("Expires"), default=_default_message_expiry_time)
#     def __str__(self):
#         return str(self.channel)