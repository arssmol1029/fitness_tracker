import { getCSRFToken, deleteObject, hasEmptyRequired, showErrorModal } from './functions.js';

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('save-exercise').addEventListener('click', function() {
        const name = document.getElementById('exercise-name').value;
        const isOwnWeight = document.getElementById('is-own-weight').checked;
        
        if (hasEmptyRequired()) {
            return;
        }
        
        const formData = new FormData();
        formData.append('name', name);
        formData.append('is_own_weight', String(isOwnWeight));

        fetch(window.URLS.exerciseCreate, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => response.json())
            .then(response => {
                if (response.status === 'error') {
                    bootstrap.Modal.getInstance(document.getElementById('add-exercise-modal')).hide();
                    document.getElementById('add-exercise-form').reset();
                    showErrorModal(data.message);
                    return;
                }

                const data = response.data;

                const badge = data.is_own_weight
                    ? `<span class="badge bg-info ms-2" title="С собственным весом">
                            <i class="bi bi-person-arms-up"></i>
                        </span>`
                    : ''

                const exerciseItem = document.createElement('div');
                exerciseItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                exerciseItem.innerHTML = `
                    <div>
                        ${data.name}
                        ${badge}
                    </div>
                    <button 
                        data-delete-url="${window.URLS.exerciseDelete}/${data.id}"
                        data-parent-selector=".list-group-item"
                        class="btn btn-sm btn-outline-danger delete-btn"
                    >
                        <i class="bi bi-trash"></i>
                    </button>
                `;
                
                document.getElementById('exercises-list').appendChild(exerciseItem);
                exerciseItem.querySelector('.delete-btn').addEventListener('click', function(e) {
                    e.preventDefault();
                    const parentToRemove = this.closest(this.dataset.parentSelector);
                    deleteObject(this.dataset.deleteUrl, parentToRemove);
                });
                
                bootstrap.Modal.getInstance(document.getElementById('add-exercise-modal')).hide();
                document.getElementById('add-exercise-form').reset();
            })
            .catch(() => {
                bootstrap.Modal.getInstance(document.getElementById('add-exercise-modal')).hide();
                document.getElementById('add-exercise-form').reset();
                showErrorModal();
            })
    });
});