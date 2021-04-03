


from sqlalchemy import create_engine
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

import moneypot

engine_string = "postgresql+psycopg2://{user}:{password}@{host}/{name}".format(**moneypot.config._sections['database'])

engine = create_engine(engine_string)
base = declarative_base()


Session = sessionmaker(bind=engine)  
session = Session()

base.metadata.create_all(engine)

session.commit()  

# Create 
res = engine.execute("SELECT * FROM test_stock")


# db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")  
# db.execute("INSERT INTO films (title, director, year) VALUES ('Doctor Strange', 'Scott Derrickson', '2016')")


#create sensor data hypertable
query_create_sensordata_table = """CREATE TABLE ticker (
                                        time TIME NOT NULL,

                                        temperature DOUBLE PRECISION,
                                        cpu DOUBLE PRECISION,
                                        FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                        );"""