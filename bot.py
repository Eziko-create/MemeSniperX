import requests, time, json, asyncio
import websockets

PUMP_URL = "https://api.pumpfunapi.org/pumpfun/new/tokens"
DEX_BOOST_URL = "https://api.dexscreener.com/token-boosts/latest/v1"
DEX_PROFILE_URL = "https://api.dexscreener.com/token-profiles/latest/v1"
BONK_WS = "wss://pumpportal.fun/api/data"

CHECK_INTERVAL = 30

def fetch_pump():
    try:
        r = requests.get(PUMP_URL, timeout=10)
        if r.status_code == 200:
            return r.json()
        print(f"Pump.fun HTTP {r.status_code} -> {r.text[:100]}")
    except Exception as e:
        print("Pump.fun Error:", e)
    return []

def fetch_dexboosts():
    try:
        r = requests.get(DEX_BOOST_URL, timeout=10)
        if r.status_code == 200:
            return r.json()
        print(f"DexScreener Boosts HTTP {r.status_code}")
    except Exception as e:
        print("DexS Boost Error:", e)
    return []

async def bonk_listener():
    async with websockets.connect(BONK_WS) as ws:
        await ws.send(json.dumps({"method": "subscribeNewToken"}))
        print("✅ Subscribed to Bonk.fun new token stream")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            print("⚡ Bonk.fun New Token:", data)

def main():
    print("🚀 MemeSniperX Bot Starting…")
    asyncio.ensure_future(bonk_listener())
    while True:
        print("\n🔄 Checking Pump.fun & DexScreener…")
        pump_list = fetch_pump()
        if pump_list:
            print("👉 Pump.fun New Tokens:", pump_list)
        dex_list = fetch_dexboosts()
        if dex_list:
            print("🔥 Dex Boosted Tokens:", dex_list)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
        
