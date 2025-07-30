import os
import requests
import time

# === CONFIG ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Store in Replit Secrets
CHAT_ID = os.getenv("CHAT_ID")                # Store in Replit Secrets
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

# === GLOBALS ===
seen_tokens = set()

# === TELEGRAM NOTIFIER ===
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# === FETCH TOKENS FROM MULTIPLE SOURCES ===
def fetch_pumpfun_tokens():
    tokens = []
    try:
        url = "https://client-api.pump.fun/tokens/trending"
        response = requests.get(url, timeout=10)
        data = response.json()
        for token in data.get("tokens", []):
            address = token.get("id")
            name = token.get("name")
            creator = token.get("creator")
            if address and address not in seen_tokens:
                tokens.append((name, address, "Pump.fun", creator))
                seen_tokens.add(address)
    except Exception as e:
        print(f"Pump.fun API Error: {e}")
    return tokens

def fetch_dexscreener_tokens():
    tokens = []
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/solana"
        response = requests.get(url, timeout=10)
        data = response.json()
        for pair in data.get("pairs", []):
            address = pair.get("pairAddress")
            name = pair.get("baseToken", {}).get("name")
            if address and name and address not in seen_tokens:
                tokens.append((name, address, "DexScreener", "N/A"))
                seen_tokens.add(address)
    except Exception as e:
        print(f"Dexscreener API Error: {e}")
    return tokens

def fetch_moralis_tokens():
    tokens = []
    try:
        url = "https://solana-gateway.moralis.io/token/mainnet/exchange/pumpfun/new"
        headers = {"accept": "application/json", "X-API-Key": MORALIS_API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        for item in data.get("result", []):
            address = item.get("address")
            name = item.get("name")
            if address and address not in seen_tokens:
                tokens.append((name, address, "Moralis", "N/A"))
                seen_tokens.add(address)
    except Exception as e:
        print(f"Moralis API Error: {e}")
    return tokens

# === FILTERS (Placeholder for Rugcheck, Birdeye, etc.) ===
def token_passes_filters(address):
    """
    This function will check:
    - Rugcheck risk score
    - Birdeye liquidity and volume
    - TokenSniffer-like checks
    - Social activity via Bobble Maps
    - GMGN / SolSniper / Trojan bot scoring
    """
    # For now, accept all tokens (Phase 1)
    # In Phase 2, implement full API checks here
    return True

# === MAIN LOOP ===
def main():
    print("🚀 MemeSniperX Bot Started!\n")
    while True:
        all_new_tokens = []
        print("🔄 Checking trending tokens...")

        # Fetch new tokens
        all_new_tokens.extend(fetch_pumpfun_tokens())
        all_new_tokens.extend(fetch_dexscreener_tokens())
        all_new_tokens.extend(fetch_moralis_tokens())

        # Filter and notify
        for name, address, source, creator in all_new_tokens:
            if token_passes_filters(address):
                msg = (
                    f"🚀 *New Token Detected!*\n\n"
                    f"*Name:* {name}\n"
                    f"*Address:* `{address}`\n"
                    f"*Source:* {source}\n"
                    f"*Creator:* {creator}\n\n"
                    f"🔗 [Pump.fun](https://pump.fun/)\n"
                    f"📊 [Dexscreener](https://dexscreener.com/solana/{address})"
                )
                send_telegram_message(msg)
                print(f"✅ Token Passed Filters: {name} | {address}")

        print(f"🔍 {len(all_new_tokens)} new token(s) processed.")
        print("⏳ Waiting 30 seconds...\n")
        time.sleep(30)

if __name__ == "__main__":
    main()
