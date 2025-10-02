from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DB_CONFIG

class DatabaseManager:
    """SQLAlchemy を使ったデータベース接続管理"""

    def __init__(self):
        # DB_CONFIG から接続情報を取得
        user = DB_CONFIG.user
        password = DB_CONFIG.password
        host = DB_CONFIG.host
        port = DB_CONFIG.port
        dbname = DB_CONFIG.database

        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"
        self.engine = create_engine(db_url, echo=False, future=True)

        # セッションファクトリ（scoped_sessionでスレッドセーフ）
        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine, autocommit=False, autoflush=False))

    def get_session(self):
        """新しいセッションを取得"""
        return self.SessionLocal()

    def close(self):
        """セッションと接続を閉じる"""
        self.SessionLocal.remove()
        self.engine.dispose()
        
