import requests
import json
import time
import os

ASN_LIST = [
    "AS9009",   # M247 (NordVPN)
    "AS20448",  # VPNtranet
    "AS209854", # Surfshark
    "AS136787", # NordVPN (TEFINCOM)
    "AS32751",  # Octovpn
    "AS212238", # Datacamp VPN
    "AS50525"   # Privado VPN
]

def get_ipv4_prefixes(asn):
    url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return [
            p["prefix"] 
            for p in data.get("data", {}).get("prefixes", [])
            if "." in p["prefix"] and p["afi"] == "IPv4"  # IPv4 detection
        ]
    except Exception as e:
        print(f"Error fetching {asn}: {str(e)}")
        return []

def main():
    all_prefixes = set()
    
    for asn in ASN_LIST:
        print(f"Processing {asn}...")
        try:
            prefixes = get_ipv4_prefixes(asn)
            all_prefixes.update(prefixes)
            time.sleep(1.5)
        except Exception as e:
            print(f"Error processing {asn}: {str(e)}")
            continue
    
    os.makedirs('output', exist_ok=True)
    
    with open("output/vpn-ipv4.txt", "w") as f:
        f.write("\n".join(sorted(all_prefixes)))
    
    print(f"Found {len(all_prefixes)} IPv4 prefixes")

if __name__ == "__main__":
    main()
