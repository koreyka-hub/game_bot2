import aiosqlite
# CRUD - Create, Read, Update, Delete
async def add_user(tg_id):
    db = await aiosqlite.connect("database.db")
    await db.execute("INSERT INTO users (tg_id) VALUES(?)", [tg_id])
    await db.commit()
    await db.close()
    return await get_user(tg_id)
async def get_user(tg_id):
    db = await aiosqlite.connect("database.db")
    db.row_factory = aiosqlite.Row
    res = await db.execute("SELECT * FROM users WHERE tg_id = ?", [tg_id])
    user = await res.fetchone()
    await db.close()
    if user:
        return dict(user)
    return None
async def update_age(tg_id, age):
    db = await aiosqlite.connect("database.db")
    await db.execute("UPDATE users SET age = ? WHERE tg_id = ?", [age, tg_id])
    await db.commit()
    await db.close()
    return await get_user(tg_id) # когда человека изменил — верни его

async def update_amount_of_games(tg_id):
    db = await aiosqlite.connect("database.db")
    await db.execute("UPDATE users SET amount_of_games = amount_of_games + 1 WHERE tg_id = ?", [tg_id])
    await db.commit()
    await db.close()
    return await get_user(tg_id) # когда человека изменил — верни его

async def delete_user(tg_id):
    db = await aiosqlite.connect("database.db")
    await db.execute("DELETE FROM users WHERE tg_id = ?", [tg_id])
    await db.commit()
    await db.close()
    return True