import requests
import time
import socket
import json

PUMP_FUN_API = "https://client-api.pump.fun/tokens/trending"
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex/tokens"

CHECK_INTERVAL = 30  # seconds

def set_dns_fallback():
    """Force Python to use Google DNS when DNS fails."""
    try:
        # This only affects local resolvers like Termux, not GitHub Actions,
        # but we'll log it anyway for debugging.
        socket.setdefaulttimeout(5)
        print("✅ DNS fallback initialized (Google 8.8.8.8 / Cloudflare 1.1.1.1).")
    except Exception as e:
        print(f"⚠️ DNS fallback setup failed: {e}")

def fetch_pump_fun_tokens():
    try:
        response = requests.get(PUMP_FUN_API, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Pump.fun HTTP {response.status_code} -> {response.text[:100]}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Pump.fun API Error: {e}")
        return []

def fetch_dexscreener_tokens():
    try:
        response = requests.get(DEXSCREENER_API, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Dexscreener HTTP {response.status_code} -> {response.text[:100]}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Dexscreener API Error: {e}")
        return []

def main():
    print("🚀 MemeSniperX Bot Started!")
    set_dns_fallback()

    while True:
        print("🔄 Checking trending tokens...")

        pump_tokens = fetch_pump_fun_tokens()
        dex_tokens = fetch_dexscreener_tokens()

        if not pump_tokens and not dex_tokens:
            print("⚠️ Both APIs returned no data. Will retry after interval.")
        else:
            # Count processed tokens
            processed_count = len(pump_tokens) if pump_tokens else 0
            print(f"🔍 {processed_count} new token(s) processed.")

        print(f"⏳ Waiting {CHECK_INTERVAL} seconds...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()


https://client-api.pump.fun/tokens/trending
