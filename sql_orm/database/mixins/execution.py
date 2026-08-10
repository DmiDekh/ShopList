from contextlib import contextmanager

from .base import BaseMixin



class ExecutionMixin(BaseMixin):
    def execute(self, command: str, params: tuple = ()):
        self.cursor.execute(command, params)
        if not self._in_transaction:
            self.connect.commit()
            
            
    @contextmanager    
    def transaction(self):
        self._in_transaction = True
        try:
            yield self
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            self._in_transaction = False