/* ===================================
   MAIN WEBSITE JAVASCRIPT
   Denov 2-son ixtisoslashtirilgan maktab
   =================================== */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Website loaded successfully');
    
    // Initialize Bootstrap tooltips if used
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers if used
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    const preloader = document.getElementById('pagePreloader');
    if (preloader) {
        window.setTimeout(() => {
            preloader.classList.add('hidden');
            window.setTimeout(() => preloader.remove(), 400);
        }, 220);
    }

    const revealTargets = document.querySelectorAll('section, .card, .stat-box, .achievement-box');
    revealTargets.forEach(el => el.classList.add('reveal'));
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.18 });
    revealTargets.forEach(el => revealObserver.observe(el));
});

/**
 * Smooth scroll to elements with smooth-scroll class
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/**
 * Form validation helper
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    // Check if form is valid using Bootstrap validation
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

/**
 * Show success message with auto-dismiss
 */
function showSuccessMessage(message, duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <i class="fas fa-check-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.insertBefore(alertDiv, document.body.firstChild);
    
    // Auto-dismiss after duration
    setTimeout(() => {
        alertDiv.remove();
    }, duration);
}

/**
 * Show error message with auto-dismiss
 */
function showErrorMessage(message, duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.insertBefore(alertDiv, document.body.firstChild);
    
    // Auto-dismiss after duration
    setTimeout(() => {
        alertDiv.remove();
    }, duration);
}

/**
 * Format date to local format
 */
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('uz-UZ', options);
}

/**
 * Confirm before delete action
 */
function confirmDelete(message = "Aniqmi? Bu amalni qaytara olmaysiz.") {
    return confirm(message);
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showSuccessMessage('Nusxaga ko\'chirildi!');
        }).catch(err => {
            console.error('Copy failed:', err);
        });
    }
}

/**
 * Lazy loading images
 */
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy-load');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img.lazy-load').forEach(img => imageObserver.observe(img));
}

/**
 * Load more button functionality
 */
function loadMore(url, containerSelector) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const container = document.querySelector(containerSelector);
            container.innerHTML += html;
        })
        .catch(error => {
            console.error('Error loading more:', error);
            showErrorMessage('Ma\'lumotni yuklashda xato bo\'ldi');
        });
}

/**
 * Mobile menu toggle
 */
function toggleMobileMenu() {
    const menu = document.querySelector('.navbar-collapse');
    if (menu.classList.contains('show')) {
        menu.classList.remove('show');
    } else {
        menu.classList.add('show');
    }
}

/**
 * Scroll to top button
 */
window.addEventListener('scroll', () => {
    const scrollBtn = document.getElementById('scrollToTopBtn');
    if (!scrollBtn) return;
    
    if (window.scrollY > 300) {
        scrollBtn.style.display = 'block';
    } else {
        scrollBtn.style.display = 'none';
    }
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Log page load time
console.log('Page loaded in:', performance.timing.loadEventEnd - performance.timing.navigationStart, 'ms');
