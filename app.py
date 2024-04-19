# Import all necessary libaries

from flask import Flask, render_template, request
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import requests
import subprocess
import random


app = Flask(__name__)

def get_all_href_links(page):
    href_links = page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a'));
        return links.map(link => link.href);
    }''')
    href_links=list(set(href_links))
    return href_links

def beautify_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.prettify()

def take_screenshot(url, filename):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=f"screenshots/{filename}.png")
        browser.close()
        
def get_page_load_time(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        browser.close()
        
        return load_time
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        
        if not url.startswith('http') or not url.startswith('https'):
            e="Invalid URL"
            return render_template('error.html', error_message=str(e))
        try:
            response = requests.get(url)
            
        except Exception as e:
            return render_template('error.html', error_message=str(e))
        
        response = requests.get(url)
        
        if response.status_code == 200: 
            status="UP"
            
            with sync_playwright() as p:
                
                browser = p.chromium.launch()
                page = browser.new_page()

                page.goto(url)
                
                performance_timing = page.evaluate('''() => {
                    return JSON.stringify(window.performance.timing);
                }''')
                
                performance_timing = json.loads(performance_timing)
                load_time = performance_timing['loadEventEnd'] - performance_timing['navigationStart']
                
                title = page.title()
                url = page.url

                viewport_size = page.viewport_size
                
                cookies = page.context.cookies()
                
                cookie = json.dumps(cookies, indent=4)
                
                if cookie=="[]":
                    cookie="This website does not use Cookies"

                html = page.inner_html('html')
                
                beautified_html = beautify_html(html)
                
                href_links = get_all_href_links(page)
                
                command = f'lighthouse {url} --only-categories=accessibility,performance,seo --quiet --output=json'
                audit_result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
                
                if audit_result.returncode == 0:  
                
                    try:
                        audit_json = json.loads(audit_result.stdout)
                        accessibility_rating = audit_json['categories']['accessibility']['score']
                        performance_rating = audit_json['categories']['performance']['score']
                        seo_rating = audit_json['categories']['seo']['score']
                        print(f"\nAccessibility Rating: {accessibility_rating}")
                        print(f"\nPerformance Rating: {performance_rating}")
                        print(f"\nSEO Rating: {seo_rating}")
                        
                    except json.JSONDecodeError as e:
                        err=f"Error decoding JSON: {e}"
                        print(err)
                        return render_template('error.html',error_message=err)
                    
                else:
                    err=audit_result.stderr
                    print(err)
                    return render_template('error.html',error_message=err)

                page.goto(url)
                page.screenshot(path=f'static/snapshot.png',full_page=True)

                browser.close()
                return render_template('result.html',load_time=load_time,status=status, title=title, url=url, viewport_size=viewport_size, cookie=cookie, beautified_html=beautified_html, href_links=href_links,ar=accessibility_rating,perf=performance_rating,seo=seo_rating)
        
        else:
            status="DOWN"
            return render_template('error.html',status=status)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
