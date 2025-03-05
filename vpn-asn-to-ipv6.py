import requests
import json

ASN_LIST = [
    "AS9009",   # M247 (NordVPN)
    "AS20448",  # VPNtranet
    "AS209854", # Surfshark
    "AS136787", # NordVPN (TEFINCOM)
    "AS32751",  # Octovpn
    "AS212238", # Datacamp VPN
    "AS50525"   # Privado VPN
]

def get_ipv6_prefixes(asn):
    url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return [
            p["prefix"] 
            for p in data.get("data", {}).get("prefixes", [])
            if ":" in p["prefix"]  # Simple IPv6 detection
        ]
    except Exception as e:
        print(f"Error fetching {asn}: {str(e)}")
        return []

def main():
    all_prefixes = set()
    
    for asn in ASN_LIST:
        print(f"Processing {asn}...")
        prefixes = get_ipv6_prefixes(asn)
        all_prefixes.update(prefixes)
        time.sleep(1)  # Rate limiting
    
    with open("vpn-ipv6.txt", "w") as f:
        f.write("\n".join(sorted(all_prefixes)))
    
    print(f"Found {len(all_prefixes)} IPv6 prefixes")

if __name__ == "__main__":
    main()
