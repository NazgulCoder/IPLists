import requests
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

def get_ipv6_prefixes(asn):
    """Fetch IPv6 prefixes for a given ASN from RIPE Stat"""
    url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        prefixes = []
        for p in data.get("data", {}).get("prefixes", []):
            # Check both CIDR notation and API's AFI field
            if ":" in p["prefix"] or p.get("afi") == "IPv6":
                prefixes.append(p["prefix"])
        return prefixes
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {asn}: {str(e)}")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON response for {asn}")
        return []

def main():
    """Main function to collect and save IPv6 prefixes"""
    all_prefixes = set()
    
    print("Starting IPv6 prefix collection...")
    for asn in ASN_LIST:
        print(f"Processing {asn}...")
        try:
            prefixes = get_ipv6_prefixes(asn)
            if prefixes:
                print(f"Found {len(prefixes)} prefixes for {asn}")
                all_prefixes.update(prefixes)
            time.sleep(1.5)  # Respect API rate limits
        except Exception as e:
            print(f"Error processing {asn}: {str(e)}")
            continue
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Save results
    output_file = 'output/vpn-ipv6.txt'
    with open(output_file, 'w') as f:
        f.write("\n".join(sorted(all_prefixes)))
    
    print("\nCollection complete!")
    print(f"Saved {len(all_prefixes)} unique IPv6 prefixes to {output_file}")

if __name__ == "__main__":
    main()
