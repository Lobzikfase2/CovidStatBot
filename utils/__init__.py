"""
Пакет содержит в себе вcё, что не является необходимым для запуска бота,
как явления, но необходимого для работы конкретного бота
"""

from . import db_api
from . import misc
from .notify_admins import on_startup_notify
