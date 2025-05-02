import { getCSRFToken } from './functions.js';

function myConfirm(message = "Вы уверены?", title = "Подтверждение", callback) {
    const confirmModal = new bootstrap.Modal(document.getElementById('customConfirm'));
    const modalTitle = document.getElementById('confirmTitle');
    const modalBody = document.getElementById('confirmBody');
    const okButton = document.getElementById('confirmOk');
    
    modalTitle.textContent = title;
    modalBody.textContent = message;
    
    confirmModal.show();
    
    okButton.onclick = function() {
        confirmModal.hide();
        callback(true);
    };

    confirmModal._element.addEventListener('hidden.bs.modal', function() {
        callback(false);
    });
}

async function deleteObject(path) {
    try {
        fetch(path, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
        }).then(response => {
            if (response.status === 'error') {
                throw response
            }
        })
    } catch (response) {
        if (response.redirect_url) {
            window.location.href = response.redirect_url;
        }
    }
}

function confirmDelete(button) {
    myConfirm('Вы точно хотите удалить шаблон?', '', (answer) => {
        if (answer) {
            const parent = button.getAttribute('parent-selector');
            const path = button.getAttribute('path');
            deleteObject(path).then(() => {
                button.closest(parent).remove();
            });
        }
    });
}