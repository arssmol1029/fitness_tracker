function getCSRFToken() {
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
        if (response.redirect) {
            window.location.href = response.redirect;
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