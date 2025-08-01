import requests, time, json, asyncio

# Try to import websockets for Bonk.fun
try:
    import websockets
    BONK_ENABLED = True
except ImportError:
    print("⚠️ Websockets not installed—Bonk.fun stream disabled.")
    BONK_ENABLED = False

PUMP_URL = "https://api.pumpfunapi.org/pumpfun/new/tokens"
DEX_BOOST_URL = "https://api.dexscreener.com/token-boosts/latest/v1"
DEX_SEARCH_URL = "https://api.dexscreener.com/latest/dex/search?q=SOL"
BONK_WS = "wss://pumpportal.fun/api/data"

CHECK_INTERVAL = 30

def fetch_json(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        print(f"⚠️ {url} HTTP {r.status_code} -> {r.text[:100]}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return {}

async def bonk_listener():
    async with websockets.connect(BONK_WS) as ws:
        await ws.send(json.dumps({"method": "subscribeNewToken"}))
        print("✅ Subscribed to Bonk.fun live token stream")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            print("⚡ Bonk.fun New Token:", data)

async def main():
    print("🚀 MemeSniperX Starting…")
    if BONK_ENABLED:
        asyncio.create_task(bonk_listener())
    while True:
        print("\n🔄 Fetching Pump.fun and DexScreener data")
        pump_json = fetch_json(PUMP_URL)
        pump_tokens = pump_json.get("data", [])
        if pump_tokens:
            print("👉 Pump.fun tokens:", pump_tokens[:2])
        else:
            print("⚠️ No Pump.fun tokens right now.")

        dex_boost = fetch_json(DEX_BOOST_URL)
        if isinstance(dex_boost, list):
            print("🔥 Dex Boost tokens:", dex_boost[:2])
        else:
            print("⚠️ Dex Boost returned empty or non-list")

        dex_search = fetch_json(DEX_SEARCH_URL)
        pairs = dex_search.get("pairs", [])
        if pairs:
            print("🔍 DexScreener SOL search pairs:", pairs[:2])

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
    
