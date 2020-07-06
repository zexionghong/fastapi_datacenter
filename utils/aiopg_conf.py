import databases
from system_item.setting import DB_CONF

db_model = 'postgresql://{user}:{password}@{host}:{port}/{database}'
jade_db = db_model.format(**DB_CONF)
jade_db = databases.Database(jade_db, min_size=1, max_size=10)
