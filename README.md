# eCourts Cause List Scraper & Downloader

A web-based application that allows users to fetch and download cause lists from the official eCourts India website in real-time.

## Features

- **Real-Time Data Fetching**: Dynamically scrapes dropdown data (States, Districts, Court Complexes, Courts) directly from eCourts website
- **User-Friendly Interface**: Clean, responsive UI with cascading dropdowns
- **Date Selection**: Pick any date for cause list retrieval
- **Case Type Selection**: Choose between Civil and Criminal cause lists
- **Smart Guidance**: Provides step-by-step instructions to handle CAPTCHA requirement
- **Error Handling**: Robust error messages and loading indicators

## How It Works

The eCourts website requires CAPTCHA verification for security. This application:
1. Fetches real-time dropdown data using Selenium web automation
2. Allows users to select their desired court details
3. Guides users to manually complete CAPTCHA on the official eCourts website
4. Provides clear instructions for downloading the PDF

## Installation

### Prerequisites
- Python 3.11+
- Chromium/Chrome browser
- Chromedriver

### Setup

1. Install dependencies:
```bash
pip install flask selenium beautifulsoup4 requests webdriver-manager python-dotenv trafilatura
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Select State**: Choose from the dropdown (loads automatically on page load)
2. **Select District**: Dropdown populates after state selection
3. **Select Court Complex**: Dropdown populates after district selection
4. **Select Court Name**: Dropdown populates after court complex selection
5. **Choose Date**: Pick the cause list date using the date picker
6. **Select Case Type**: Choose Civil or Criminal
7. **Click "Open eCourts & Download Manually"**: Follow the on-screen instructions
8. **On eCourts Website**: 
   - The system shows you all your selections
   - Enter the CAPTCHA code displayed
   - Click Civil or Criminal button
   - PDF downloads automatically

## Technical Stack

### Backend
- **Flask 3.1.2**: Web framework
- **Selenium 4.36.0**: Browser automation for scraping
- **BeautifulSoup4**: HTML parsing
- **Python pathlib**: File management

### Frontend
- **HTML5/CSS3**: Responsive design with gradient theme
- **Vanilla JavaScript**: Fetch API for async requests
- **Native date picker**: No external dependencies

## Project Structure

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
├── downloads/            # PDF storage (created automatically)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── replit.md            # Detailed documentation
```

## API Endpoints

- `GET /` - Main application page
- `GET /api/states` - Fetch list of states
- `POST /api/districts` - Fetch districts for a state
- `POST /api/court-complexes` - Fetch court complexes for state/district
- `POST /api/courts` - Fetch courts for state/district/complex
- `POST /api/get-captcha-image` - Fetch CAPTCHA image (prepared for future use)
- `POST /api/download-cause-list` - Manual download guidance

## Key Features Explained

### Real-Time Scraping
The application uses Selenium to interact with the eCourts website in real-time, ensuring:
- Always up-to-date dropdown options
- No cached or stale data
- Accurate court information

### CAPTCHA Handling
For legal and ethical reasons, the application:
- Does NOT attempt to bypass CAPTCHA
- Provides clear user instructions
- Opens the official eCourts website for manual completion
- Shows all pre-selected values to minimize user effort

### Resource Management
- Proper driver cleanup with try-finally blocks
- Prevents zombie Chrome processes
- Efficient session management

## Configuration

### Selenium Options
The Chrome driver is configured with:
- Headless mode for efficiency
- No sandbox mode for Replit environment
- Disabled automation detection
- Configured download directory

### Performance
- Average response time: 3-5 seconds per dropdown
- AJAX wait time: 2 seconds between selections
- Total dropdown population: ~8-10 seconds

## Limitations

1. **CAPTCHA Requirement**: Cannot automatically bypass CAPTCHA (by design)
2. **Performance**: Selenium initialization adds latency
3. **Single-threaded**: To avoid overloading eCourts servers
4. **Structure Dependency**: May break if eCourts changes their website structure

## Future Enhancements

- [ ] Batch download for all courts in a Court Complex
- [ ] Metadata logging and storage
- [ ] Performance optimization with caching
- [ ] CLI interface for developers
- [ ] Advanced error recovery
- [ ] PDF preview functionality
- [ ] Scheduled automatic fetching

## Legal & Ethical Notes

- Accesses publicly available data from eCourts India
- Respects CAPTCHA protection
- Implements rate limiting to avoid server overload
- For informational purposes only
- Always verify with official court records

## Troubleshooting

### Dropdowns Not Loading
- Check browser console for errors
- Verify internet connection
- Ensure eCourts website is accessible

### eCourts Website Changes
- Update Selenium selectors in app.py
- Check element IDs match current eCourts structure

### Download Issues
- Disable browser popup blocker
- Ensure JavaScript is enabled
- Try different browser

## Support

For issues or questions:
1. Check the console logs
2. Review the replit.md file for detailed documentation
3. Verify eCourts website accessibility

## License

This project is for educational and informational purposes only.

## Acknowledgments

- Data source: [eCourts India](https://services.ecourts.gov.in/ecourtindia_v6/)
- Built with Flask, Selenium, and modern web technologies
