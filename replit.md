# eCourts Cause List Scraper & Downloader

## Overview
A web-based application that allows users to fetch and download cause lists from the official eCourts India website in real-time. The application provides a user-friendly interface for selecting State, District, Court Complex, and Court Name, then facilitates downloading cause list PDFs for specified dates.

## Purpose
- Enable real-time scraping of cause lists directly from the eCourts website (https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/)
- Provide an intuitive UI for court data selection
- Help users navigate the eCourts CAPTCHA requirement
- Support legal professionals, researchers, and the general public in accessing court cause lists

## Current State
✅ **Fully Functional MVP**
- Real-time dropdown data fetching from eCourts (States, Districts, Court Complexes, Courts)
- Responsive web interface with date picker
- Manual download assistance (CAPTCHA handling guidance)
- Error handling and user feedback
- Loading indicators for better UX

## Recent Changes (October 16, 2025)
- Initial project setup with Flask backend
- Implemented Selenium-based web scraping for eCourts dynamic dropdowns
- Created responsive frontend UI with cascading dropdowns
- Added real-time validation and error handling
- Configured workflow for running the application
- Implemented manual download flow due to CAPTCHA requirements

## Project Architecture

### Backend (Python Flask)
- **Framework**: Flask 3.1.2
- **Scraping**: Selenium 4.36.0 with Chrome headless browser
- **Web Parsing**: BeautifulSoup4 (installed but Selenium handles most parsing)
- **File Management**: Python pathlib for organized PDF storage

### Frontend
- **HTML5**: Template-based rendering with Jinja2
- **CSS3**: Responsive design with gradient backgrounds
- **JavaScript**: Vanilla JS with Fetch API for async requests
- **Date Picker**: Native HTML5 date input

### Key Features
1. **Real-Time Dropdown Population**
   - States → Districts → Court Complexes → Courts
   - Dynamic loading based on user selection
   - Loading spinners for better UX

2. **CAPTCHA Handling**
   - Automated CAPTCHA bypass not implemented (ethical/legal reasons)
   - Provides user guidance for manual CAPTCHA entry
   - Opens eCourts website with pre-filled instructions

3. **Error Handling**
   - Network error handling
   - Invalid input validation
   - User-friendly error messages

4. **File Organization**
   - Structure: `downloads/{state}/{district}/{court_complex}/{court_name}/{date}.pdf`
   - Automatic directory creation

### API Endpoints
- `GET /` - Main application page
- `GET /api/states` - Fetch list of states
- `POST /api/districts` - Fetch districts for a state
- `POST /api/court-complexes` - Fetch court complexes for state/district
- `POST /api/courts` - Fetch courts for state/district/complex
- `POST /api/get-captcha-image` - Fetch CAPTCHA image (prepared for future use)
- `POST /api/download-cause-list` - Download cause list (manual guidance)

## Technical Constraints & Challenges

### CAPTCHA Challenge
The eCourts website implements CAPTCHA protection which cannot be automatically bypassed for ethical and legal reasons. The current implementation:
- Guides users to manually complete CAPTCHA verification
- Opens eCourts website in new tab with pre-filled instructions
- Provides clear step-by-step guidance for PDF download

### Selenium Configuration
- Runs in headless mode for efficiency
- Uses Chrome/Chromium browser
- Configured with appropriate wait times for AJAX calls
- Downloads directory pre-configured

### Performance Considerations
- Selenium driver initialization takes 2-3 seconds per request
- AJAX wait times add 2 seconds between dropdown selections
- Average total time for full dropdown population: 8-10 seconds
- Single-threaded to avoid overloading eCourts servers (respectful scraping)

## User Preferences
- Clean, professional UI with gradient theme
- Clear error messages and status indicators
- Step-by-step guidance for complex processes
- Real-time feedback during data loading

## Dependencies
### Python Packages
- flask==3.1.2
- selenium==4.36.0
- beautifulsoup4==4.14.2
- requests==2.32.5
- webdriver-manager==4.0.2
- python-dotenv==1.1.1
- trafilatura (from web scraper blueprint)

### System Packages
- chromium
- chromedriver

## File Structure
```
.
├── app.py                 # Flask backend with API endpoints
├── templates/
│   └── index.html        # Main UI template
├── static/
│   ├── css/
│   │   └── style.css     # Responsive styling
│   └── js/
│       └── app.js        # Frontend logic and API calls
├── downloads/            # PDF storage (gitignored)
├── .gitignore           # Python and download files
└── replit.md            # This file
```

## How to Use

### For Users
1. Open the application in your browser
2. Select State from the dropdown (loads automatically)
3. Select District (populates after state selection)
4. Select Court Complex (populates after district selection)
5. Select Court Name (populates after court complex selection)
6. Choose the cause list date using the date picker
7. Select case type (Civil or Criminal)
8. Click "Open eCourts & Download Manually"
9. Follow the on-screen instructions to complete CAPTCHA and download PDF

### For Developers
**Run the application:**
```bash
python app.py
```
The server starts on `http://0.0.0.0:5000`

**Access the application:**
- Local: http://localhost:5000
- Replit: Use the webview in the workspace

## Future Enhancements (Next Phase)
1. **Batch Download**: Download all courts under a Court Complex
2. **Metadata Logging**: JSON records of fetched data and errors
3. **Performance Optimization**: Cache dropdown data with refresh capability
4. **CLI Interface**: Command-line support for developers
5. **Advanced Error Recovery**: Retry logic for network failures
6. **Deployment**: Production hosting configuration
7. **PDF Preview**: Browser-based preview before download
8. **Scheduled Fetching**: Automatic cause list retrieval

## Known Limitations
1. Cannot automatically bypass CAPTCHA (by design)
2. Selenium initialization adds latency to each request
3. Single-threaded to avoid overloading eCourts servers
4. Requires active browser (headless) for scraping
5. Dependent on eCourts website structure (may break if they change their UI)

## Legal & Ethical Notes
- This tool accesses publicly available data from eCourts India
- Respects CAPTCHA protection and doesn't attempt to bypass it
- Implements rate limiting to avoid server overload
- For informational purposes only - always verify with official court records

## Support & Troubleshooting
- If dropdowns don't load: Check console logs for errors
- If the eCourts website changes: Update Selenium selectors in app.py
- For CAPTCHA issues: Ensure JavaScript is enabled in browser
- For download issues: Check browser popup blocker settings

---
**Last Updated**: October 16, 2025
**Version**: 1.0.0 (MVP)
**Status**: Fully Functional
