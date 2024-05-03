import sqlite3


conn=sqlite3.connect("data.db")
baza=conn.execute(f"""SELECT chat_id FROM foydalanuvchilar""")
conn.commit()

for i in baza:
    print(i[0])
print(baza)