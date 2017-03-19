import sys
import mysql.connector
import tldextract
from subprocess import call
from hashids import Hashids

if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit

	ext = tldextract.extract(sys.argv[1])

	if len(ext.registered_domain) == 0:
		domain = ext.domain
	else:
		domain = ext.registered_domain
	
	cnx = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='dashboard')

	cursor = cnx.cursor(buffered=True)

	query_meta = ("SELECT id as meta_id, hash as hashed from metas where url =%s")
	add_meta = ("INSERT INTO metas (url) VALUES (%s)")
	update_meta = ("UPDATE metas set hash=%s where url=%s")

	query_site = ("SELECT id from sites where meta_id =%s")
	add_site = ("INSERT INTO sites (meta_id, full_url) VALUES (%s, %s)")


	cursor.execute(query_meta, (domain,))

	domain_hash = None
	hashids = Hashids()
	for(meta_id, hashed) in cursor:
		domain_hash = hashed
		pid = meta_id

	if domain_hash == None:
		cursor.execute(add_meta, (domain,))
		pid = cursor.lastrowid
		domain_hash = hashids.encode(pid)
		cursor.execute(update_meta, (domain_hash, domain))

	cursor.execute(query_site, (pid,))

	if not cursor.rowcount:
		cursor.execute(add_site, (pid, sys.argv[1]))
		call(["./start.sh", domain, domain_hash])
		print("New starter scripts were generated for " + domain)
	else:
		print("Nothing new was generated")

	cnx.commit()

	cursor.close()
	cnx.close()
