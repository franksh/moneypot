import csv
import psycopg2
import psycopg2.extras
import moneypot

connection = psycopg2.connect(host=moneypot.config['database']['HOST'],
                              database=moneypot.config['database']['NAME'],
                              user=moneypot.config['database']['USER'],
                              password=moneypot.config['database']['PASSWORD'])

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("select * from test_stock where price<900")

# In case it fails:
# connection.rollback()
# TO commit changes to the db:
# connection.commit()

result = cursor.fetchall()

print (result)

cursor.close()
