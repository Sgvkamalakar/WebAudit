import json
import subprocess
from playwright.sync_api import sync_playwright

url = '<URL>'
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page()
    page.goto(url)
    
    command = f'lighthouse {url} --only-categories=accessibility,performance,seo --output=json'
    audit_result = subprocess.run(command, shell=True, capture_output=True, text=False, encoding='utf-8')
    
    browser.close()
    
    if audit_result.returncode == 0:  
        
        try:
            audit_json = json.loads(audit_result.stdout)
            with open('audit_report.json', 'w') as file:
                json.dump(audit_json, file, indent=2)
            accessibility_rating = audit_json['categories']['accessibility']['score']
            performance_rating = audit_json['categories']['performance']['score']
            seo_rating = audit_json['categories']['seo']['score']
            print(f"\nAccessibility Rating: {accessibility_rating}")
            print(f"\nPerformance Rating: {performance_rating}")
            print(f"\nSEO Rating: {seo_rating}")
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            
        except KeyError:
            print("One or more ratings not found in the audit result.")
            
    else:
        print(f"Error running Lighthouse: {audit_result.stderr}")
