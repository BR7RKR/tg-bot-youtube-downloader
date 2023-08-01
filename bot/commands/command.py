from abc import ABCMeta, abstractmethod, abstractproperty, ABC

from clients.tg import UpdateObj


class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, upd: UpdateObj):
        pass

    @abstractmethod
    def is_for(self, command_definer):
        pass
