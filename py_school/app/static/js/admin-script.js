/* ===================================
   ADMIN PANEL JAVASCRIPT
   Denov 2-son ixtisoslashtirilgan maktab
   =================================== */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin panel loaded successfully');
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

/**
 * Confirm delete action
 */
function confirmDeleteAction(itemName = 'element') {
    return confirm(`Bu ${itemName}ni o'chirishni istaysizmi? Bu amalni qaytara olmaysiz.`);
}

/**
 * Show success notification
 */
function showSuccess(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <i class="fas fa-check-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

/**
 * Show error notification
 */
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Show warning notification
 */
function showWarning(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
}

/**
 * Form validation before submit
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    // Bootstrap validation
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        showError('Iltimos, barcha majburiy maydonlarni to\'ldiring');
        return false;
    }
    return true;
}

/**
 * Enable/disable loading state on button
 */
function setButtonLoading(buttonId, isLoading = true) {
    const button = document.getElementById(buttonId);
    if (!button) return;
    
    if (isLoading) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Yuklanmoqda...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || 'Jo\'natish';
    }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Validate file size
 */
function validateFileSize(file, maxSizeMB = 5) {
    const maxBytes = maxSizeMB * 1024 * 1024;
    if (file.size > maxBytes) {
        showError(`Fayl juda katta. Maksimal hajm: ${maxSizeMB}MB`);
        return false;
    }
    return true;
}

/**
 * Validate file type
 */
function validateFileType(file, allowedTypes) {
    if (!allowedTypes.includes(file.type)) {
        showError(`Faqat ${allowedTypes.join(', ')} fayl turlari qabul qilinadi`);
        return false;
    }
    return true;
}

/**
 * Preview image before upload
 */
function previewImage(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    if (!input || !preview) return;
    
    input.addEventListener('change', function() {
        const file = this.files[0];
        
        if (!file) {
            preview.style.display = 'none';
            return;
        }
        
        // Validate file
        if (!validateFileType(file, ['image/jpeg', 'image/png', 'image/gif'])) {
            return;
        }
        
        if (!validateFileSize(file, 5)) {
            return;
        }
        
        // Read and display image
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    });
}

/**
 * Search/filter table
 */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toUpperCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            let text = rows[i].textContent || rows[i].innerText;
            if (text.toUpperCase().indexOf(filter) > -1) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    });
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

/**
 * Fetch data via AJAX
 */
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        showError('Ma\'lumotni yuklashda xato bo\'ldi');
        return null;
    }
}

/**
 * Export table to CSV
 */
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        let csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    // Create download link
    const csvContent = 'data:text/csv;charset=utf-8,' + csv.join('\n');
    const link = document.createElement('a');
    link.setAttribute('href', encodeURI(csvContent));
    link.setAttribute('download', filename);
    link.click();
    
    showSuccess('Jadval eksport qilindi');
}

/**
 * Print table
 */
function printTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const printWindow = window.open('', '', 'height=400,width=800');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(table.outerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

/**
 * Auto-save form data to localStorage
 */
function autoSaveForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Load saved data
    form.querySelectorAll('input, textarea, select').forEach(field => {
        const savedValue = localStorage.getItem(`form_${formId}_${field.name}`);
        if (savedValue) {
            field.value = savedValue;
        }
    });
    
    // Save on change
    form.addEventListener('change', function() {
        form.querySelectorAll('input, textarea, select').forEach(field => {
            localStorage.setItem(`form_${formId}_${field.name}`, field.value);
        });
    });
}

/**
 * Clear form auto-save data
 */
function clearFormAutoSave(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.querySelectorAll('input, textarea, select').forEach(field => {
        localStorage.removeItem(`form_${formId}_${field.name}`);
    });
}

// Log admin panel load
console.log('Admin panel initialized successfully');
