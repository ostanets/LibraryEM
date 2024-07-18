from logging_config import configure_logging
from repo.database import Database
from repo.repo import Repo

configure_logging()

if __name__ == '__main__':
    Database.init_db()
    repo = Repo(Database.get_session())

    repo.create_base_statuses()
