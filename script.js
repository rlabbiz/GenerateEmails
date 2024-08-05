let emailList = {};
fetch('http://127.0.0.1:8000/send/')
.then(response => response.json())
.then(data => {
    emailList = data;
})


// Set to store shown emails
let shownEmails = new Set();
let currentEmails = [];

// Function to get the selected provider from the dropdown
function getSelectedProvider() {
    const selectElement = document.getElementById('providerSelect');
    return selectElement.value;
}

// Function to load emails based on the selected provider
function loadEmails() {
    const provider = getSelectedProvider();
    
    if (provider === 'all') {
        filteredEmailList = [].concat(...Object.values(emailList));
    } else if (emailList[provider]) {
        filteredEmailList = emailList[provider];
    }    
}

// Function to get a specified number of random emails
function getRandomEmails() {
    const provider = getSelectedProvider();
    const numEmails = parseInt(document.getElementById('numEmails').value, 10);
    loadEmails(); // Load emails based on the current provider selection
    
    if (filteredEmailList.length === 0) {
        document.getElementById('output').textContent = 'No emails available for the selected provider. Please restore.';
        currentEmails = [];
        return;
    }
    
    let availableEmails = filteredEmailList.filter(email => !shownEmails.has(email));
    
    if (availableEmails.length === 0) {
        document.getElementById('output').textContent = 'All emails have been shown. Please restore.';
        currentEmails = [];
        return;
    }
    
    // Shuffle available emails and pick the first `numEmails` emails
    availableEmails = availableEmails.sort(() => Math.random() - 0.5);
    currentEmails = availableEmails.slice(0, numEmails);
    currentEmails.forEach(email => shownEmails.add(email));
    
    document.getElementById('output').textContent = `Selected emails: ${currentEmails.join(', ')}`;
}

// Function to restore all emails
function restoreEmails() {
    shownEmails.clear();
    document.getElementById('output').textContent = 'All emails restored.';
}

// Function to copy the email and password to the clipboard
function copyToClipboard() {
    if (currentEmails.length === 0) {
        document.getElementById('output').textContent = 'No email to copy.';
        return;
    }
    tmpEmails = currentEmails;
    for (let currentEmail of tmpEmails) {
        tmpEmails[tmpEmails.indexOf(currentEmail)] = currentEmail.split(':')[0];
    }
    navigator.clipboard.writeText(tmpEmails.join(';')).then(() => {
        document.getElementById('output').textContent = 'Emails and passwords copied to clipboard.';
    }).catch(err => {
        document.getElementById('output').textContent = 'Failed to copy emails and passwords.';
        console.error('Error copying text: ', err);
    });
}

// Function to open the login page of the selected provider and automate login
function openLoginPage() {
    fetch('http://127.0.0.1:8000/emails/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({emails: currentEmails})
    })
    copyToClipboard();
}


// Event listeners for buttons
document.getElementById('generateButton').addEventListener('click', getRandomEmails);
document.getElementById('restoreButton').addEventListener('click', restoreEmails);
document.getElementById('copyButton').addEventListener('click', copyToClipboard);
document.getElementById('loginButton').addEventListener('click', openLoginPage);

// Initial load of emails based on default provider selection
loadEmails();
