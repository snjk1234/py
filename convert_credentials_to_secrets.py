"""
This script converts credentials.json to Streamlit secrets format (TOML)
Run this locally and copy the output to Streamlit Cloud Secrets
"""
import json

try:
    with open('credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    print("=" * 60)
    print("Copy everything below to Streamlit Cloud Secrets:")
    print("=" * 60)
    print()
    print("[gcp_service_account]")
    
    for key, value in creds.items():
        # Handle private_key specially to preserve \n
        if key == "private_key":
            # Escape quotes and preserve newlines
            value = value.replace('"', '\\"')
            print(f'{key} = "{value}"')
        else:
            print(f'{key} = "{value}"')
    
    print()
    print("=" * 60)
    print("✅ Done! Copy the above text to Streamlit Cloud")
    print("=" * 60)
    
except FileNotFoundError:
    print("❌ Error: credentials.json not found!")
    print("Make sure you run this script in the same folder as credentials.json")
except Exception as e:
    print(f"❌ Error: {e}")
