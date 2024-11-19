#!/usr/bin/env python3

"""
Copyright 2024 Yasurfer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import requests
import json
from datetime import datetime

# Global constant for ES/SPX ratio
ES_SPX_RATIO = 1.0041126541414127

# ANSI color codes for terminal output
RED = '\033[91m'
RESET = '\033[0m'

class ESPriceConverter:
    """
    A class to handle conversion between E-mini S&P 500 futures (ES) and S&P 500 index (SPX) prices
    """
    
    def __init__(self):
        """Initialize converter with base URL and request headers"""
        self.base_url = "https://blackbull.com/wp-json/bbm/get_bid/"
        self.headers = {
            'referer': 'https://blackbull.com/en/trading/instruments/futures/indices-futures/us500-spx500-future/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"'
        }
        self.es_spx_ratio = ES_SPX_RATIO

    def get_es_price(self):
        """
        Fetch current ES price from BlackBull Markets API
        Returns: float or None if request fails
        """
        params = {
            'action': 'bid',
            'symbol': 'US500.f'
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return float(data['sell'])
        except Exception as e:
            print(f"Error fetching ES price: {e}")
            return None

    def convert_spx_to_es(self, spx_value):
        """
        Convert SPX value to ES value
        Args: spx_value (float): SPX price
        Returns: float or None if conversion fails
        """
        try:
            es_value = round(spx_value * self.es_spx_ratio, 2)
            return es_value
        except Exception as e:
            print(f"Error converting SPX to ES: {e}")
            return None
            
    def convert_es_to_spx(self, es_value):
        """
        Convert ES value to SPX value
        Args: es_value (float): ES price
        Returns: float or None if conversion fails
        """
        try:
            spx_value = round(es_value / self.es_spx_ratio, 2)
            return spx_value
        except Exception as e:
            print(f"Error converting ES to SPX: {e}")
            return None

def get_live_conversion():
    """
    Get live conversion between ES and SPX prices
    Returns: str formatted conversion or None if fails
    """
    converter = ESPriceConverter()
    es_price = converter.get_es_price()
    if es_price:
        spx_value = converter.convert_es_to_spx(es_price)
        return f"ES: {es_price} → SPX: {RED}{spx_value}{RESET}"
    return None

def main():
    """Main function to handle command line interface"""
    parser = argparse.ArgumentParser(description='Convert between ES and SPX values')
    parser.add_argument('--es', type=float, help='ES value to convert to SPX')
    parser.add_argument('--spx', type=float, help='SPX value to convert to ES')

    args = parser.parse_args()
    converter = ESPriceConverter()

    if args.es is not None:
        spx_value = converter.convert_es_to_spx(args.es)
        print(f"ES: {args.es} → SPX: {RED}{spx_value}{RESET}")
    elif args.spx is not None:
        es_value = converter.convert_spx_to_es(args.spx)
        print(f"SPX: {args.spx} → ES: {RED}{es_value}{RESET}")
    else:
        # Default behavior: show live conversion
        result = get_live_conversion()
        if result:
            print(result)

if __name__ == "__main__":
    main()