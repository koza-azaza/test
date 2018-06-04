def test(sql):
	tpl = [' ADD ', '  ALL ', ' ALTER ',
	' ANALYZE ', ' AND ', ' AS ',
	' ASC ', ' ASENSITIVE ', ' AUTO INCREMENT ',
	' BDB ', ' BEFORE ', ' BERKELEYDB ',
	' BETWEEN ', ' BIGINT ', ' BINARY ',
	' BLOB ', ' BOTH ', ' BY ',
	' CALL ', ' CASCADE ', ' CASE ',
	' CHANGE ', ' CHAR ', ' CHARACTER ',
	' CHECK ', ' COLLATE ', ' COLUMN ',
	' COLUMNS ', ' CONDITION ', ' CONNECTION ',
	' ONSTRAINT ', ' CONTINUE ', ' CREATE ',
	' CROSS ', ' CURRENT_DATE ', ' CURRENT TIME ',
	' CURRENT_TIMESTAMP ', ' CURSOR ', ' DATABASE ',
	' DATABASES ', ' DAY_HOUR ', ' DAY MICROSECOND ',
	' DAY MINUTE ', ' DAY SECOND ', ' DEC ', ' DECIMAL ',
	' DECLARE ', ' DEFAULT ', ' DELAYED ', ' DELETE ', 
	' DESC ', ' DESCRIBE ', ' DETERMINISTIC ', 
	' DISTINCT ', ' DISTINCTROW ', ' DIV ', 
	' DOUBLE ', ' DROP ', ' ELSE ', ' ELSEIF ', 
	' ENCLOSED ', ' ESCAPED ', ' EXISTS ', ' EXIT ',
	' EXPLAIN ', ' FALSE ', ' FETCH ', ' FIELDS ', 
	' FLOAT ', ' FOR ', ' FORCE ', ' FOREIGN ', ' FOUND ', 
	' FRAC SECOND ', ' FROM ', ' FULLTEXT ', ' GRANT ',
	' GROUP ', ' HAVING ', ' HIGH PRIORITY ', 
	' HOUR MICROSECOND ', ' HOUR_MINUTE ', 
	' HOUR SECOND ', ' IF ', ' IGNORE ', 
	' IN ', ' INDEX ', ' INFILE ', 
	' INNER ', ' INNODB ', ' INOUT ',
	' INSENSITIVE ', ' INSERT ', ' INT ',
	' INTEGER ', ' INTERVAL ', ' INTO ', 
	' IO_THREAD ', ' IS ', ' ITERATE ',
	' JOIN ', ' KEY ', ' KEYS ',
	' KILL ', ' LEADING ', ' SELECT ', '"', '*', "'", "(", ")", ";", " "]
	exit = " " + sql.upper() + " "
	normal = True
	for i in tpl:
		if(i == " "):
			exit = exit[1:-1]		
		err = exit.count(i)
		while(err > 0):
			print("1 " + str(i))
			exit = exit[:exit.find(i)] + exit[exit.find(i) + len(i):]
			err -= 1
			normal = False
	if(normal):
		return sql
	else:
		return exit.lower()

def getUsername(tablename):
	#изначально запуск проводился от root'a
	db = MySQLdb.connect(host="localhost", user="ReadOnlyUser", passwd="ROUpassword", db="contacts", charset='utf8')
	cur = db.cursor()
	sql ='''select %s from user'''%(test(tablename))#добавлен тест строки на sql-инъекцию
	cur.execute(sql)
	j = cur.fetchall()
	out = json.dumps(j[0][0],ensure_ascii=False,indent=2,sort_keys=True)
	return out