import requests, time, json, asyncio

# Try to import websockets safely
try:
    import websockets
    BONK_ENABLED = True
except ImportError:
    print("⚠️ Websockets library not found. Bonk.fun stream disabled.")
    BONK_ENABLED = False

PUMP_URL = "https://api.pumpfunapi.org/pumpfun/new/tokens"
DEX_BOOST_URL = "https://api.dexscreener.com/token-boosts/latest/v1"
DEX_SEARCH_URL = "https://api.dexscreener.com/latest/dex/search?q=SOL"
BONK_WS = "wss://pumpportal.fun/api/data"

CHECK_INTERVAL = 30

def fetch_json(url):
    """Helper to fetch JSON with retries."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        print(f"{url} HTTP {r.status_code} -> {r.text[:100]}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return []

async def bonk_listener():
    async with websockets.connect(BONK_WS) as ws:
        await ws.send(json.dumps({"method": "subscribeNewToken"}))
        print("✅ Subscribed to Bonk.fun new token stream")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            print("⚡ Bonk.fun New Token:", data)

async def main():
    print("🚀 MemeSniperX Bot Starting…")

    # Start Bonk.fun listener if enabled
    if BONK_ENABLED:
        asyncio.create_task(bonk_listener())

    while True:
        print("\n🔄 Checking Pump.fun & DexScreener…")
        
        pump_list = fetch_json(PUMP_URL)
        if pump_list:
            print("👉 Pump.fun New Tokens:", pump_list[:2])  # Show first 2 tokens
        else:
            print("⚠️ No new Pump.fun tokens found.")

        dex_boosts = fetch_json(DEX_BOOST_URL)
        if dex_boosts:
            print("🔥 Dex Boosted Tokens:", dex_boosts[:2])
        else:
            print("⚠️ No boosted DexScreener tokens.")

        dex_search = fetch_json(DEX_SEARCH_URL)
        if dex_search:
            print("🔍 DexScreener SOL Search:", dex_search.get("pairs", [])[:2])

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
            
