from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "mysql://root:my-secret-pw@127.0.0.1:3306/chcemvediet?charset=utf8&use_unicode=0",
)
Session = sessionmaker(bind=engine)
session = Session()
