from .components.consumer import routing as consumer_routing
from .components.task import routing as task_routing

urlpatterns = consumer_routing.urlpatterns
channels_urlspattern= task_routing.channels_urlspattern