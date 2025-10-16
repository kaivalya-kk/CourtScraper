from flask import Flask, render_template, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)

# Base URL for eCourts
ECOURTS_URL = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"

# Downloads directory
DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

def get_driver():
    """Initialize Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Set download directory
    prefs = {
        "download.default_directory": str(DOWNLOADS_DIR.absolute()),
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/states', methods=['GET'])
def get_states():
    """Fetch list of states from eCourts"""
    driver = None
    try:
        driver = get_driver()
        driver.get(ECOURTS_URL)
        
        # Wait for state dropdown to load
        wait = WebDriverWait(driver, 10)
        state_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "sess_state_code"))
        )
        
        # Get all state options
        select = Select(state_dropdown)
        states = []
        for option in select.options:
            if option.get_attribute('value'):  # Skip empty options
                states.append({
                    'value': option.get_attribute('value'),
                    'text': option.text.strip()
                })
        
        return jsonify({'success': True, 'states': states})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@app.route('/api/districts', methods=['POST'])
def get_districts():
    """Fetch list of districts for a given state"""
    driver = None
    try:
        data = request.json
        state_code = data.get('state_code')
        
        if not state_code:
            return jsonify({'success': False, 'error': 'State code is required'}), 400
        
        driver = get_driver()
        driver.get(ECOURTS_URL)
        
        wait = WebDriverWait(driver, 10)
        
        # Select state
        state_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "sess_state_code"))
        )
        Select(state_dropdown).select_by_value(state_code)
        
        # Wait for district dropdown to populate
        time.sleep(2)  # Allow AJAX call to complete
        district_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "sess_dist_code"))
        )
        
        # Get all district options
        select = Select(district_dropdown)
        districts = []
        for option in select.options:
            if option.get_attribute('value'):
                districts.append({
                    'value': option.get_attribute('value'),
                    'text': option.text.strip()
                })
        
        return jsonify({'success': True, 'districts': districts})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@app.route('/api/court-complexes', methods=['POST'])
def get_court_complexes():
    """Fetch list of court complexes for a given state and district"""
    driver = None
    try:
        data = request.json
        state_code = data.get('state_code')
        district_code = data.get('district_code')
        
        if not state_code or not district_code:
            return jsonify({'success': False, 'error': 'State and district codes are required'}), 400
        
        driver = get_driver()
        driver.get(ECOURTS_URL)
        
        wait = WebDriverWait(driver, 10)
        
        # Select state
        state_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "sess_state_code"))
        )
        Select(state_dropdown).select_by_value(state_code)
        
        time.sleep(2)
        
        # Select district
        district_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "sess_dist_code"))
        )
        Select(district_dropdown).select_by_value(district_code)
        
        # Wait for court complex dropdown to populate
        time.sleep(2)
        court_complex_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "court_complex_code"))
        )
        
        # Get all court complex options
        select = Select(court_complex_dropdown)
        court_complexes = []
        for option in select.options:
            if option.get_attribute('value'):
                court_complexes.append({
                    'value': option.get_attribute('value'),
                    'text': option.text.strip()
                })
        
        return jsonify({'success': True, 'court_complexes': court_complexes})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@app.route('/api/courts', methods=['POST'])
def get_courts():
    """Fetch list of courts for a given state, district, and court complex"""
    driver = None
    try:
        data = request.json
        state_code = data.get('state_code')
        district_code = data.get('district_code')
        court_complex_code = data.get('court_complex_code')
        
        if not all([state_code, district_code, court_complex_code]):
            return jsonify({'success': False, 'error': 'State, district, and court complex codes are required'}), 400
        
        driver = get_driver()
        driver.get(ECOURTS_URL)
        
        wait = WebDriverWait(driver, 10)
        
        # Select state
        state_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "sess_state_code"))
        )
        Select(state_dropdown).select_by_value(state_code)
        time.sleep(2)
        
        # Select district
        district_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "sess_dist_code"))
        )
        Select(district_dropdown).select_by_value(district_code)
        time.sleep(2)
        
        # Select court complex
        court_complex_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "court_complex_code"))
        )
        Select(court_complex_dropdown).select_by_value(court_complex_code)
        
        # Wait for court dropdown to populate
        time.sleep(2)
        court_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "court_code"))
        )
        
        # Get all court options
        select = Select(court_dropdown)
        courts = []
        for option in select.options:
            if option.get_attribute('value'):
                courts.append({
                    'value': option.get_attribute('value'),
                    'text': option.text.strip()
                })
        
        return jsonify({'success': True, 'courts': courts})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@app.route('/api/get-captcha-image', methods=['POST'])
def get_captcha_image():
    """Fetch captcha image for manual entry"""
    driver = None
    try:
        data = request.json
        state_code = data.get('state_code')
        district_code = data.get('district_code')
        court_complex_code = data.get('court_complex_code')
        court_code = data.get('court_code')
        
        if not all([state_code, district_code, court_complex_code, court_code]):
            return jsonify({'success': False, 'error': 'All selection fields are required'}), 400
        
        driver = get_driver()
        driver.get(ECOURTS_URL)
        
        wait = WebDriverWait(driver, 10)
        
        # Select all dropdowns
        state_dropdown = wait.until(EC.presence_of_element_located((By.ID, "sess_state_code")))
        Select(state_dropdown).select_by_value(state_code)
        time.sleep(2)
        
        district_dropdown = wait.until(EC.presence_of_element_located((By.ID, "sess_dist_code")))
        Select(district_dropdown).select_by_value(district_code)
        time.sleep(2)
        
        court_complex_dropdown = wait.until(EC.presence_of_element_located((By.ID, "court_complex_code")))
        Select(court_complex_dropdown).select_by_value(court_complex_code)
        time.sleep(2)
        
        court_dropdown = wait.until(EC.presence_of_element_located((By.ID, "court_code")))
        Select(court_dropdown).select_by_value(court_code)
        time.sleep(1)
        
        # Get captcha image
        captcha_img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='securimage_show.php']")))
        captcha_url = captcha_img.get_attribute('src')
        
        # Get session cookies
        cookies = driver.get_cookies()
        
        return jsonify({
            'success': True,
            'captcha_url': captcha_url,
            'cookies': cookies
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@app.route('/api/download-cause-list', methods=['POST'])
def download_cause_list():
    """Download cause list PDF with user-provided captcha"""
    try:
        data = request.json
        state_code = data.get('state_code')
        state_name = data.get('state_name')
        district_code = data.get('district_code')
        district_name = data.get('district_name')
        court_complex_code = data.get('court_complex_code')
        court_complex_name = data.get('court_complex_name')
        court_code = data.get('court_code')
        court_name = data.get('court_name')
        cause_date = data.get('cause_date')
        captcha = data.get('captcha')
        case_type = data.get('case_type', 'civil')  # 'civil' or 'criminal'
        
        if not all([state_code, district_code, court_complex_code, court_code, cause_date, captcha]):
            return jsonify({'success': False, 'error': 'All fields including captcha are required'}), 400
        
        # Note: Due to CAPTCHA challenge, this is a placeholder for the download logic
        # In a real implementation, you would need to handle CAPTCHA solving
        # For now, we return instructions for manual download
        
        return jsonify({
            'success': False,
            'error': 'CAPTCHA challenge detected',
            'message': 'eCourts website requires CAPTCHA verification. Please use the manual download option.',
            'instructions': {
                'state': state_name,
                'district': district_name,
                'court_complex': court_complex_name,
                'court': court_name,
                'date': cause_date,
                'type': case_type
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
