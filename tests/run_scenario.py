import json
import requests
import sys
import os

def run_tests():
    with open('tests/scenario.json', 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    base_url = os.environ.get("API_URL", "http://localhost:8000")
    all_passed = True

    print(f"Start running {len(scenarios)} scenarios...\n")
    print(f"Base url: {base_url}")

    for s in scenarios:
        print(f"Сценарий: {s['scenario_name']}")
        url = base_url + s['endpoint']
        
        try:
            response = requests.request(s['method'], url, json=s['payload'])
            status = response.status_code
            
            if status == s['expected_status']:
                print(f"Success! Status: {status}")
            else:
                print(f"Error! Exected {s['expected_status']}, got {status}")
                all_passed = False
                
        except requests.exceptions.ConnectionError:
            print("Connection Error!")
            sys.exit(1)

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()