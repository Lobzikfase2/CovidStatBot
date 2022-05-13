"""
Пакет содержит все созданные разработчиком миддлвари
"""

from loader import dp
from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
