from sqlalchemy.orm import Session

from repo.models.status import Statuses, Status


class Repo:
    _session_local: Session = ...

    def __init__(self, session_local: Session):
        self._session_local = session_local

    def create_base_statuses(self):
        for status in Statuses:
            if self._session_local.query(Status).filter_by(name=status.value).first() is None:
                self._session_local.add(Status(name=status.value))

        self._session_local.commit()


