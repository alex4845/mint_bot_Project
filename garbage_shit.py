
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Параметры подключения к базе данных PostgreSQL
db_host = '141.8.199.12'
db_port = 5432  # По умолчанию порт для PostgreSQL
db_name = 'rasputin_base.db'
db_user = 'postgres'
db_password = '20rasputin23'


# Создание подключения к базе данных
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
Session = sessionmaker(bind=engine)
session = Session()

# Создание базового класса для объявления моделей таблицы
Base = declarative_base()

class List1(Base):
    __tablename__ = 'list_1'
    number = Column(Integer, primary_key=True)
    name = Column(String)
    insta = Column(String)
    username = Column(String)
    user_id = Column(BigInteger)
    sex = Column(String)
    qr = Column(LargeBinary)
    time_m = Column(DateTime)
    manager = Column(String)

Base.metadata.create_all(engine)

#session.query(List1).get(1).user_id = 469632258

new_entry = List1(
    number=1,
    name='Иван Иванов',
    insta='ivan_ivanov_insta',
    username='ivan_ivanov_username',
    user_id=469632258,
    sex='М',
    qr=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...',
    time_m=datetime.now(),
)
session.add(new_entry)
session.commit()



all_entries = session.query(List1).all()
for i in all_entries:
    print(i.number, i.name, i.insta, i.username, i.user_id, i.time_m, i.qr)


session.close()