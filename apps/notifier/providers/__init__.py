from .telegram import TelegramProvider
from .email import EmailProvider
from .base import NotificationProvider
from typing import Optional

_providers = {
    "telegram": TelegramProvider,
    "email": EmailProvider,
}

def get_provider(channel: str) -> Optional[NotificationProvider]:
    provider_class = _providers.get(channel)
    if provider_class:
        return provider_class()
    return None
