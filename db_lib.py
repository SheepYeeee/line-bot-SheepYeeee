import pymysql

db = pymysql.connect(host='localhost',user='root',password='0000',db='sheepyeeee_news',charset='utf8')
cur = db.cursor()


# sql="INSERT INTO `user` (`id`) SELECT %s WHERE NOT EXISTS (SELECT `id` FROM `user` WHERE `id`=%s)"

user_id = "122"
sql = "SELECT * FROM `user`"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print(row[0])
    aaa=row[0]
    db.commit()
    cur.close()
    if user_id in aaa:
        print('已經有了')
    else:
        print('還沒有喔')
        