import aiosqlite    
async def add_games(id,tg_id):
    db = await aiosqlite.connect("database.db")
    await db.execute("INSERT INTO games (id, user_tg_id) VALUES(?, ?)", [id, tg_id])
    await db.commit()
    await db.close()

async def get_games(id):
    db = await aiosqlite.connect("database.db")
    db.row_factory = aiosqlite.Row
    res = await db.execute("SELECT * FROM games WHERE id = ?", [id])
    games = await res.fetchone()
    await db.close()
    if games:
        return dict(games)
    return None