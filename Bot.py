import discord
import os
import json
import re
import difflib
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("log.json")
DATABASE = {}
LOG_CACHE = []

def init_files():
    global DATABASE, LOG_CACHE
    LOG_FILE.write_text("[]", encoding="utf-8")  # reset log.json setiap boot

    try:
        with open("Database.json", "r", encoding="utf-8") as f:
            DATABASE = json.load(f)
    except:
        DATABASE = {}
        print("❌ Database.json could not be loaded")

def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())

def log_query(user: discord.abc.User, query: str, matched_keys: list[str]):
    global LOG_CACHE
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": str(user),
        "user_id": user.id,
        "query": query,
        "matched_keys": matched_keys
    }
    LOG_CACHE.append(log_entry)
    if len(LOG_CACHE) >= 5:
        if len(LOG_CACHE) > 100:
            LOG_CACHE = LOG_CACHE[-100:]
        LOG_FILE.write_text(json.dumps(LOG_CACHE, indent=2, ensure_ascii=False), encoding="utf-8")

def search_database(query: str) -> list[tuple[str, str]]:
    if not query or not DATABASE:
        return []
    query_lower = query.lower().strip()
    exact, prefix, contain = [], [], []
    for key, value in DATABASE.items():
        k = key.lower()
        if k == query_lower: exact.append((key, value))
        elif k.startswith(query_lower): prefix.append((key, value))
        elif query_lower in k: contain.append((key, value))
    if exact: return exact
    if prefix: return prefix
    if contain: return contain
    close = difflib.get_close_matches(query, DATABASE.keys(), n=3, cutoff=0.6)
    return [(k, DATABASE[k]) for k in close]

async def handle_message(message: discord.Message):
    if message.author.bot: return
    content = message.content.strip()
    if not content.startswith("?") or len(content) <= 1: return
    query = content[1:].strip()
    if not DATABASE:
        await message.channel.send("❌ Database kosong.")
        return
    results = search_database(query)
    if results:
        if len(results) > 10:
            results = results[:10]
            note = "\n\n📝 *Hanya menampilkan 10 hasil pertama.*"
        else: note = ""
        response = "\n\n".join(f"🔹 **{k}**\n{v}" for k, v in results) + note
        keys = [k for k, _ in results]
    else:
        ex = ", ".join(f"`?{k}`" for k in list(DATABASE.keys())[:3])
        response = f"❌ Tidak ditemukan: `{query}`\n\n💡 Coba: {ex}"
        keys = []
    try:
        await message.channel.send(response)
        log_query(message.author, query, keys)
    except Exception as e:
        await message.channel.send("❌ Terjadi kesalahan.")
        print(f"⚠️ {e}")