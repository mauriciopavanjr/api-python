import os

class Config:
    """Base config class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration."""
    db_dir = os.path.join(os.getcwd(), "db")
    os.makedirs(db_dir, exist_ok=True)
    print(f'sqlite:///{os.path.join(os.getcwd(), "dev.db")}')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(db_dir, "dev.db")}'

class ProductionConfig(Config):
    """Production configuration."""
    db_dir = os.path.join(os.getcwd(), "db")
    os.makedirs(db_dir, exist_ok=True)
    print(f'sqlite:///{os.path.join(os.getcwd(), "dev.db")}')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(db_dir, "weather.db")}'
