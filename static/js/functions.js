export function showErrorModal(message = 'Ошибка!') {
    const errorModalEl = document.getElementById('error-modal');
    const errorModal = new bootstrap.Modal(errorModalEl);

    const errorMessage = errorModalEl.querySelector('.error-message');
    errorMessage.textContent = message;

    const errorButton = errorModalEl.querySelector('.again-btn');
    errorButton.onclick = () => location.reload();
    errorModal.show();
};


export function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                break;
            }
        }
    }
    return cookieValue;
}


export function deleteObject(url, object = null, to_reload = false) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest',
        },
    }).then(response => response.json())
        .then(response => {
            if (response.status === 'ok') {
                if (object) {
                    object.remove();
                }
                if (to_reload) {
                    location.reload();
                }
            } 
        })
}

document.querySelectorAll('.delete-btn').forEach((btn) => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const parentToRemove = this.closest(this.dataset.parentSelector);
        deleteObject(this.dataset.deleteUrl, parentToRemove, true);
    });
});


export function hasEmptyRequired() {
    document.querySelectorAll('.is-invalid').forEach(el => {
        el.classList.remove('is-invalid');
    });

    const requiredFields = document.querySelectorAll(`
        [required]:not([hidden]),
        [required]:not(.d-none)
    `);
    let emptyRequired = false;
    
    requiredFields.forEach(field => {
        if (field.checkVisibility()) {
            if (field.tagName === 'SELECT') {
                if (!field.value) {
                    emptyRequired = true;
                    const $select2Container = $(field).next('.select2-container');
                    $select2Container.addClass('is-invalid');
                }
            } else if (!field.value.trim()) {
                emptyRequired = true;
                field.classList.add('is-invalid');
            }
        }
    });

    if (emptyRequired) {
        document.querySelectorAll('.is-invalid').forEach(field => {
            const removeHighlight = () => {
                field.classList.remove('is-invalid');
                field.removeEventListener('focus', removeHighlight);
                field.removeEventListener('click', removeHighlight);
            };
            
            field.addEventListener('focus', removeHighlight);
            field.addEventListener('click', removeHighlight);
        });
    }

    return emptyRequired;
};