from sqlalchemy import create_engine
# from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker


import moneypot

DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}/{name}".format(
                    **moneypot.config._sections['database'])

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)  
# session = Session(se)

# base.metadata.create_all(engine)