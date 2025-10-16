// Store selected values and their display names
const selectedData = {
    state: { code: '', name: '' },
    district: { code: '', name: '' },
    courtComplex: { code: '', name: '' },
    court: { code: '', name: '' },
    date: '',
    caseType: 'civil'
};

// DOM Elements
const stateSelect = document.getElementById('state');
const districtSelect = document.getElementById('district');
const courtComplexSelect = document.getElementById('court-complex');
const courtSelect = document.getElementById('court');
const dateInput = document.getElementById('date');
const caseTypeSelect = document.getElementById('case-type');
const openEcourtsBtn = document.getElementById('open-ecourts-btn');
const statusMessage = document.getElementById('status-message');
const selectedInfo = document.getElementById('selected-info');

// Spinner elements
const stateSpinner = document.getElementById('state-spinner');
const districtSpinner = document.getElementById('district-spinner');
const courtComplexSpinner = document.getElementById('court-complex-spinner');
const courtSpinner = document.getElementById('court-spinner');

// Utility functions
function showSpinner(spinner) {
    spinner.classList.add('active');
}

function hideSpinner(spinner) {
    spinner.classList.remove('active');
}

function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `alert alert-${type}`;
    statusMessage.style.display = 'block';
}

function hideStatus() {
    statusMessage.style.display = 'none';
}

function updateSelectedInfo() {
    if (selectedData.state.name && selectedData.district.name && 
        selectedData.courtComplex.name && selectedData.court.name) {
        
        document.getElementById('info-state').textContent = selectedData.state.name;
        document.getElementById('info-district').textContent = selectedData.district.name;
        document.getElementById('info-court-complex').textContent = selectedData.courtComplex.name;
        document.getElementById('info-court').textContent = selectedData.court.name;
        document.getElementById('info-date').textContent = selectedData.date || '-';
        document.getElementById('info-case-type').textContent = selectedData.caseType.charAt(0).toUpperCase() + selectedData.caseType.slice(1);
        
        selectedInfo.style.display = 'block';
        openEcourtsBtn.disabled = !selectedData.date;
    } else {
        selectedInfo.style.display = 'none';
        openEcourtsBtn.disabled = true;
    }
}

// Fetch states on page load
async function loadStates() {
    try {
        showSpinner(stateSpinner);
        const response = await fetch('/api/states');
        const data = await response.json();
        
        if (data.success) {
            stateSelect.innerHTML = '<option value="">-- Select State --</option>';
            data.states.forEach(state => {
                const option = document.createElement('option');
                option.value = state.value;
                option.textContent = state.text;
                option.dataset.name = state.text;
                stateSelect.appendChild(option);
            });
        } else {
            showStatus('Failed to load states: ' + data.error, 'error');
        }
    } catch (error) {
        showStatus('Error loading states: ' + error.message, 'error');
    } finally {
        hideSpinner(stateSpinner);
    }
}

// Load districts when state is selected
async function loadDistricts(stateCode, stateName) {
    try {
        selectedData.state = { code: stateCode, name: stateName };
        selectedData.district = { code: '', name: '' };
        selectedData.courtComplex = { code: '', name: '' };
        selectedData.court = { code: '', name: '' };
        
        districtSelect.innerHTML = '<option value="">-- Select District --</option>';
        courtComplexSelect.innerHTML = '<option value="">-- Select Court Complex --</option>';
        courtSelect.innerHTML = '<option value="">-- Select Court --</option>';
        
        districtSelect.disabled = true;
        courtComplexSelect.disabled = true;
        courtSelect.disabled = true;
        
        showSpinner(districtSpinner);
        
        const response = await fetch('/api/districts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ state_code: stateCode })
        });
        
        const data = await response.json();
        
        if (data.success) {
            data.districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district.value;
                option.textContent = district.text;
                option.dataset.name = district.text;
                districtSelect.appendChild(option);
            });
            districtSelect.disabled = false;
        } else {
            showStatus('Failed to load districts: ' + data.error, 'error');
        }
    } catch (error) {
        showStatus('Error loading districts: ' + error.message, 'error');
    } finally {
        hideSpinner(districtSpinner);
        updateSelectedInfo();
    }
}

// Load court complexes when district is selected
async function loadCourtComplexes(districtCode, districtName) {
    try {
        selectedData.district = { code: districtCode, name: districtName };
        selectedData.courtComplex = { code: '', name: '' };
        selectedData.court = { code: '', name: '' };
        
        courtComplexSelect.innerHTML = '<option value="">-- Select Court Complex --</option>';
        courtSelect.innerHTML = '<option value="">-- Select Court --</option>';
        
        courtComplexSelect.disabled = true;
        courtSelect.disabled = true;
        
        showSpinner(courtComplexSpinner);
        
        const response = await fetch('/api/court-complexes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                state_code: selectedData.state.code,
                district_code: districtCode
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            data.court_complexes.forEach(complex => {
                const option = document.createElement('option');
                option.value = complex.value;
                option.textContent = complex.text;
                option.dataset.name = complex.text;
                courtComplexSelect.appendChild(option);
            });
            courtComplexSelect.disabled = false;
        } else {
            showStatus('Failed to load court complexes: ' + data.error, 'error');
        }
    } catch (error) {
        showStatus('Error loading court complexes: ' + error.message, 'error');
    } finally {
        hideSpinner(courtComplexSpinner);
        updateSelectedInfo();
    }
}

// Load courts when court complex is selected
async function loadCourts(courtComplexCode, courtComplexName) {
    try {
        selectedData.courtComplex = { code: courtComplexCode, name: courtComplexName };
        selectedData.court = { code: '', name: '' };
        
        courtSelect.innerHTML = '<option value="">-- Select Court --</option>';
        courtSelect.disabled = true;
        
        showSpinner(courtSpinner);
        
        const response = await fetch('/api/courts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                state_code: selectedData.state.code,
                district_code: selectedData.district.code,
                court_complex_code: courtComplexCode
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            data.courts.forEach(court => {
                const option = document.createElement('option');
                option.value = court.value;
                option.textContent = court.text;
                option.dataset.name = court.text;
                courtSelect.appendChild(option);
            });
            courtSelect.disabled = false;
        } else {
            showStatus('Failed to load courts: ' + data.error, 'error');
        }
    } catch (error) {
        showStatus('Error loading courts: ' + error.message, 'error');
    } finally {
        hideSpinner(courtSpinner);
        updateSelectedInfo();
    }
}

// Event listeners
stateSelect.addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    if (e.target.value) {
        loadDistricts(e.target.value, selectedOption.dataset.name);
    } else {
        districtSelect.disabled = true;
        courtComplexSelect.disabled = true;
        courtSelect.disabled = true;
        updateSelectedInfo();
    }
});

districtSelect.addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    if (e.target.value) {
        loadCourtComplexes(e.target.value, selectedOption.dataset.name);
    } else {
        courtComplexSelect.disabled = true;
        courtSelect.disabled = true;
        updateSelectedInfo();
    }
});

courtComplexSelect.addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    if (e.target.value) {
        loadCourts(e.target.value, selectedOption.dataset.name);
    } else {
        courtSelect.disabled = true;
        updateSelectedInfo();
    }
});

courtSelect.addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    if (e.target.value) {
        selectedData.court = { code: e.target.value, name: selectedOption.dataset.name };
    } else {
        selectedData.court = { code: '', name: '' };
    }
    updateSelectedInfo();
});

dateInput.addEventListener('change', (e) => {
    selectedData.date = e.target.value;
    updateSelectedInfo();
});

caseTypeSelect.addEventListener('change', (e) => {
    selectedData.caseType = e.target.value;
    updateSelectedInfo();
});

// Open eCourts website with pre-filled data
openEcourtsBtn.addEventListener('click', () => {
    if (!selectedData.date) {
        showStatus('Please select a date', 'warning');
        return;
    }
    
    // Format date for eCourts (dd/mm/yyyy)
    const dateObj = new Date(selectedData.date);
    const day = String(dateObj.getDate()).padStart(2, '0');
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const year = dateObj.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    
    // Create instructions modal/alert
    const instructions = `
📋 INSTRUCTIONS TO DOWNLOAD CAUSE LIST:

1. A new tab will open with eCourts website
2. Your selections have been noted:
   - State: ${selectedData.state.name}
   - District: ${selectedData.district.name}
   - Court Complex: ${selectedData.courtComplex.name}
   - Court: ${selectedData.court.name}
   - Date: ${formattedDate}
   - Case Type: ${selectedData.caseType.toUpperCase()}

3. On the eCourts page:
   ✓ Select the same State, District, Court Complex, and Court
   ✓ Enter the date: ${formattedDate}
   ✓ Enter the CAPTCHA code shown on screen
   ✓ Click the "${selectedData.caseType.toUpperCase()}" button
   ✓ The PDF will download automatically

Opening eCourts website now...
    `.trim();
    
    alert(instructions);
    
    // Open eCourts website in new tab
    window.open('https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/', '_blank');
    
    showStatus('eCourts website opened in new tab. Follow the instructions to download the PDF.', 'success');
});

// Set default date to today
dateInput.valueAsDate = new Date();
selectedData.date = dateInput.value;

// Load states on page load
loadStates();
