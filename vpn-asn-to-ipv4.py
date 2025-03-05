import requests
import time
import os
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

def get_ipv4_prefixes(asn):
    """Fetch IPv4 prefixes for a given ASN from RIPE Stat"""
    url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"
    try:
        # Add custom headers to avoid being blocked
        headers = {
            'User-Agent': 'VPN-IP-List-Generator/1.0 (+https://github.com/your-repo)'
        }
        response = requests.get(url, headers=headers, timeout=45)
        response.raise_for_status()
        data = response.json()
        
        print(f"Raw response for {asn}: {json.dumps(data, indent=2)}")  # Debug
        
        prefixes = []
        for p in data.get("data", {}).get("prefixes", []):
            # Alternative verification method
            if p.get("afi") == "IPv4" and len(p["prefix"].split('.')) == 4:
                prefixes.append(p["prefix"])
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
            print(f"Found {len(prefixes)} prefixes for {asn}")
            if prefixes:
                print("Sample prefixes:", prefixes[:3])
            all_prefixes.update(prefixes)
            time.sleep(3)  # Increased delay
        except Exception as e:
            print(f"Critical error processing {asn}: {str(e)}")
            continue
    
    # Save results
    os.makedirs('output', exist_ok=True)
    output_file = 'output/vpn-ipv4.txt'
    
    with open(output_file, 'w') as f:
        f.write("\n".join(sorted(all_prefixes)))
    
    print("\nFinal Results:")
    print(f"Total ASNs checked: {len(ASN_LIST)}")
    print(f"Unique IPv4 prefixes collected: {len(all_prefixes)}")
    print(f"Output file: {output_file}")

if __name__ == "__main__":
    main()
