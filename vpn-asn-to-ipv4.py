import requests
import time
import os
import ipaddress
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

def is_valid_ipv4_prefix(prefix):
    try:
        network = ipaddress.IPv4Network(prefix, strict=False)
        return True
    except ValueError:
        return False

def get_ipv4_prefixes(asn):
    """Fetch IPv4 prefixes for a given ASN from RIPE Stat"""
    url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        prefixes = []
        for entry in data.get("data", {}).get("prefixes", []):
            prefix = entry.get("prefix", "")
            if is_valid_ipv4_prefix(prefix):
                prefixes.append(prefix)
        return prefixes
        
    except Exception as e:
        print(f"Error fetching {asn}: {str(e)}")
        return []

def main():
    """Main function to collect and save IPv4 prefixes"""
    all_prefixes = set()
    
    print("Starting IPv4 prefix collection...")
    for asn in ASN_LIST:
        print(f"\nProcessing {asn}...")
        try:
            prefixes = get_ipv4_prefixes(asn)
            print(f"Raw prefixes found: {prefixes}")
            if prefixes:
                all_prefixes.update(prefixes)
                print(f"Added {len(prefixes)} valid prefixes")
            time.sleep(1)
        except Exception as e:
            print(f"Error processing {asn}: {str(e)}")
            continue
    
    # Save results
    os.makedirs('output', exist_ok=True)
    output_file = 'output/vpn-ipv4.txt'
    
    with open(output_file, 'w') as f:
        f.write("\n".join(sorted(all_prefixes)))
    
    print("\nFinal Results:")
    print(f"Total unique IPv4 prefixes: {len(all_prefixes)}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
