from abc import ABCMeta, abstractmethod

from bot.clients.tg import Update


class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, upd: Update):
        pass

    @abstractmethod
    def is_for(self, command_definer: Update):
        pass
