import os, asyncio, time, logging, pathlib, aiohttp
from dotenv import load_dotenv

# .env を読み込む
load_dotenv(dotenv_path=pathlib.Path(__file__).parent / ".env")

GH_TOKEN = os.getenv("GITHUB_TOKEN")
API_URL  = os.getenv("API_URL", "http://localhost:8000")

HEADERS = {"Authorization": f"token {GH_TOKEN}",
           "Accept": "application/vnd.github+json"}

logging.basicConfig(level=logging.INFO,
    format="%(levelname)s: %(message)s")

QUERY = 'language:python location:japan "data science"'

async def fetch_users(session, page=1):
    url = f"https://api.github.com/search/users?q={QUERY}&page={page}&per_page=30"
    async with session.get(url, headers=HEADERS) as r:
        r.raise_for_status()
        return (await r.json())["items"]

async def user_detail(session, username: str):
    async with session.get(f"https://api.github.com/users/{username}",
                           headers=HEADERS) as r:
        r.raise_for_status()
        return await r.json()

async def post_candidate(session, payload):
    async with session.post(f"{API_URL}/candidates/", json=payload) as r:
        if r.status == 201:
            logging.info("✔ created %s", payload["full_name"])
        elif r.status == 400:
            logging.warning("⚠ duplicate: %s", payload["email"])
        else:
            logging.error("✖ %s %s", r.status, await r.text())

async def main(pages=1):
    async with aiohttp.ClientSession() as gh, aiohttp.ClientSession() as api:
        for p in range(1, pages + 1):
            users = await fetch_users(gh, p)
            for u in users:
                detail = await user_detail(gh, u["login"])
                name  = detail.get("name") or u["login"].title()
                email = detail.get("email") or f"{u['login']}@example.com"
                await post_candidate(api, {"full_name": name, "email": email})
            time.sleep(1)  # GitHub rate limit 対策

if __name__ == "__main__":
    asyncio.run(main(pages=1))