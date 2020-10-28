import sqlite3
from main import casos

def create_db_tables(c):
	
	c.execute(
		'''
		CREATE TABLE casos (
			date text,
			total text
		)
		'''
	)

def insert_casos(c, dic):
	c.execute(
		'''
		INSERT INTO casos (date, total) VALUES ( "%s", "%s")
		''' % (str(dic.get("data")), str(dic.get("total")))
	)
	
def main():
	conn = sqlite3.connect('covid-pt.db')

	c = conn.cursor()
	#create_db_tables(c)

	casosdic = casos()
	insert_casos(c, casosdic)

	conn.commit()
	conn.close()


if __name__ == "__main__":
	main()
	print('exemplo alteração')