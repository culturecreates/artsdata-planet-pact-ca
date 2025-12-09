import urllib.request
import json
import re

def fetch_and_extract_json():
    """
    Fetch data from PACT API and extract JSON portion
    """
    url = "https://www.pact.ca/api/membership/artsdata"
    
    try:
        # Fetch data from API
        print("Fetching data from API...")
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        
        print("Data fetched successfully!")
        
        # Find JSON array in the response
        # Look for pattern starting with [{ and ending with }]
        json_match = re.search(r'\[\{.*\}\]', data, re.DOTALL)
        
        if json_match:
            json_string = json_match.group(0)
            
            # Parse JSON to validate it
            json_data = json.loads(json_string)
            
            print(f"Found {len(json_data)} records in JSON")
            
            # Write to file with proper formatting
            with open('output.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print("JSON data saved to 'output.json'")
            return json_data
        else:
            print("No JSON array found in response")
            return None
            
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    data = fetch_and_extract_json()
    if data:
        print(f"\nFirst record preview:")
        print(json.dumps(data[0], indent=2))