import requests
import time
import os
import json
import ipaddress
import logging
from typing import List, Set

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

ASN_LIST = [
    "AS9009",    # M247 (NordVPN)
    "AS20448",   # VPNtranet
    "AS209854",  # Surfshark
    "AS136787",  # NordVPN (TEFINCOM)
    "AS32751",   # Octovpn
    "AS212238",  # Datacamp VPN
    "AS50525",   # Privado VPN
    "AS8100",    # QuadraBet
    "AS11878",   # Tzulo
    "AS13213",   # UK2.net
    "AS46475",   # Limestone Networks
    "AS46562",   # Performive
    "AS60068",   # CDN77
    "AS199218",  # ProtonVPN
    "AS203020",  # HostRoyale
    "AS204957",  # GREEN FLOID LLC
    "AS212238",  # Datacamp Limited
    "AS216419",  # Matrix Telecom Solutions
    "AS210743",  # BABBAR-AS
    "AS200651",  # FlokiNET
    "AS394711",  # Limenet
]

BASE_URL = "https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"

def fetch_prefixes(asn: str, session: requests.Session) -> List[dict]:
    """Fetch prefixes for a given ASN."""
    url = BASE_URL.format(asn=asn)
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("prefixes", [])
    except (requests.RequestException, json.JSONDecodeError) as e:
        logging.error(f"Error fetching {asn}: {e}")
        return []

def filter_prefixes(prefixes: List[dict], ip_version: int) -> List[str]:
    """Filter prefixes based on the IP version (4 or 6)."""
    valid_prefixes = []
    for entry in prefixes:
        prefix = entry.get("prefix", "")
        if ip_version == 4:
            try:
                ipaddress.IPv4Network(prefix, strict=False)
                valid_prefixes.append(prefix)
            except ValueError:
                continue
        elif ip_version == 6:
            if ":" in prefix or entry.get("afi") == "IPv6":
                valid_prefixes.append(prefix)
    return valid_prefixes

def collect_prefixes(ip_version: int, sleep_duration: float, output_file: str) -> None:
    """Collect and save prefixes for a given IP version."""
    all_prefixes: Set[str] = set()
    with requests.Session() as session:
        logging.info(f"Starting IPv{ip_version} prefix collection...")
        for asn in ASN_LIST:
            logging.info(f"Processing {asn}...")
            prefixes = fetch_prefixes(asn, session)
            filtered = filter_prefixes(prefixes, ip_version)
            if filtered:
                logging.info(f"Found {len(filtered)} valid IPv{ip_version} prefixes for {asn}")
                all_prefixes.update(filtered)
            time.sleep(sleep_duration)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write("\n".join(sorted(all_prefixes)))
    
    logging.info(f"Saved {len(all_prefixes)} unique IPv{ip_version} prefixes to {output_file}")

if __name__ == "__main__":
    # You can easily switch between IPv4 and IPv6 collections
    collect_prefixes(ip_version=4, sleep_duration=1, output_file='output/vpn-ipv4.txt')
    collect_prefixes(ip_version=6, sleep_duration=1.5, output_file='output/vpn-ipv6.txt')
