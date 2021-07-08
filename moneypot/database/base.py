import moneypot
from sqlalchemy import create_engine
# from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}/{name}".format(
                    **moneypot.config._sections['database'])

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)

Base = declarative_base()

Session = sessionmaker(bind=engine)  
