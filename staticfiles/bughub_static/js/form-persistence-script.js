// Function to save form data to local storage
function saveFormData(formId) {
    const form = document.getElementById(formId);
    const formData = {};

    for (const element of form.elements) {
        if (element.name) {
            if (element.type === 'checkbox' || element.type === 'radio') {
                formData[element.name] = element.checked;
            } else {
                formData[element.name] = element.value;
            }
        }
    }
    //Finish it
    localStorage.setItem(formId, JSON.stringify(formData));
}

// Function to load form data from local storage
function loadFormData(formId) {
    const savedData = localStorage.getItem(formId);
    if (savedData) {
        const formData = JSON.parse(savedData);
        const form = document.getElementById(formId);

        for (const [name, value] of Object.entries(formData)) {
            const element = form.elements[name];
            if (element) {
                if (element.type === 'checkbox' || element.type === 'radio') {
                    element.checked = value;
                } else {
                    element.value = value;
                }
            }
        }
    }
}

// Function to clear form data from local storage
function clearFormData(formId) {
    localStorage.removeItem(formId);
}

// Set up form persistence for a given form
function setupFormPersistence(formId) {
    const form = document.getElementById(formId);

    // Load saved data when page loads
    window.addEventListener('load', () => loadFormData(formId));

    // Save data as user types
    form.addEventListener('input', () => saveFormData(formId));

    // Clear data when form is submitted successfully
    form.addEventListener('submit', (e) => {
        // Don't prevent the default submit action
        if (form.checkValidity()) {
            // Use setTimeout to ensure this runs after the form submission
            setTimeout(() => clearFormData(formId), 0);
        }
    });
}

// Set up persistence for add post form
setupFormPersistence('add-post-form');

// Set up persistence for edit post form
setupFormPersistence('edit-post-form');