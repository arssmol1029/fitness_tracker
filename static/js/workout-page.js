import { getCSRFToken } from './functions.js';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('workout-form');
    const container = document.getElementById('exercises-container');

    const checkNew = document.getElementById('is-new');
    const isNew = (JSON.parse(checkNew.value.toLowerCase()));

    const checkEditMode = document.getElementById('edit-mode');
    let isEditMode = !(JSON.parse(checkEditMode.value.toLowerCase()));
    let sortable = new Sortable(container, {
        animation: 150,
        handle: '.card-body',
        disabled: !isEditMode,
        ghostClass: 'drag-ghost',
        chosenClass: 'drag-chosen',
        dragClass: 'drag-item',
    });

    const editBtn = document.getElementById('edit-mode-on');
    const saveBtn = document.getElementById('save-workout');
    const saveTempBtn = document.getElementById('save-template');
    const cancelBtn = document.getElementById('edit-mode-off');
    const addExBtn = document.getElementById('add-exercise');

    const successModalEl = document.getElementById('success-modal');
    const errorModalEl = document.getElementById('error-modal');
    const cancelModalEl = document.getElementById('cancel-modal');
    const closeBtn = document.getElementById('close-btn');
    
    const successModal = new bootstrap.Modal(successModalEl);
    const errorModal = new bootstrap.Modal(errorModalEl);
    const cancelModal = new bootstrap.Modal(cancelModalEl);


    function changeEditMode() {
        if (isEditMode) {
            if (hasEmptyRequired()) {
                return;
            }
        }

        isEditMode = !isEditMode;
        checkEditMode.value = isEditMode.toString();
        sortable.option("disabled", !isEditMode);

        const hiddenEl = document.querySelectorAll('.edit-hidden');
        hiddenEl.forEach((El) => {
            El.hidden = isEditMode;
        });

        const displayedEl = document.querySelectorAll('.edit-displayed');
        displayedEl.forEach((El) => {
            El.hidden = !isEditMode;
        });

        const disabledEl = document.querySelectorAll('.edit-disabled');
        disabledEl.forEach((El) => {
            El.disabled = isEditMode;
        });

        const enabledEl = document.querySelectorAll('.edit-enabled');
        enabledEl.forEach((El) => {
            El.disabled = !isEditMode;
        });
    };

    function hasEmptyRequired() {
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });

        const requiredFields = document.querySelectorAll(`
            .edit-enabled[required]:not([hidden]),
            .edit-enabled[required]:not(.d-none)
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

    changeEditMode();

    if (!isNew) {
        editBtn.addEventListener('click', changeEditMode);
    }

    async function selectCustom(card) {
        const select = card.querySelector('.exercise-select');
        $(select).select2({
            ajax: {
                url: window.URLS.exerciseSearch,
                dataType: 'json',
                processResults: function(data) {
                    return {
                        results: data.results.map(item => {
                            return {
                                id: item.id,
                                text: item.text,
                                is_own_weight: item.is_own_weight,
                            };
                        })
                    };
                }
            },
            templateResult: function(item) {
                return item.text;
            },
            templateSelection: function(item) {
                const selectedOption = select.options[select.selectedIndex];
                $(selectedOption).data('is-own-weight', item.is_own_weight);
                return item.text;
            }
        });

        $(select).on('change.select2', function() {
            const selectedData = $(this).select2('data')[0];
            
            if (selectedData.is_own_weight) {
                $(card).find('.weight-input').val('').parent().hide();
                
            } else {
                $(card).find('.weight-input').parent().show();
            }
        });
    };

    function addSet(card) {
        const select = card.querySelector('.exercise-select');
        const selectedData = $(select).select2('data')[0];
        if (!selectedData) return;

        const set = document.getElementById('set-template').cloneNode(true);
        set.classList.remove('d-none');
        set.removeAttribute('id');
        
        if (selectedData.is_own_weight) {
            set.querySelector('.weight-input').parentElement.hidden = true;
            set.querySelector('.weight-input').required = false;
        } else {
            set.querySelector('.weight-input').parentElement.hidden = false;
            set.querySelector('.weight-input').required = true;
        }

        const setsContainer = card.querySelector('.sets-container');
        
        set.querySelector('.remove-set').addEventListener('click', function() {
            setsContainer.removeChild(set);
        });

        setsContainer.appendChild(set);
    };

    const cards = document.querySelectorAll('.card:not(.d-none)');
    cards.forEach((card) => {
        selectCustom(card);

        card.querySelector('.remove-exercise').addEventListener('click', function() {
            container.removeChild(card);
        });

        const setsContainer = card.querySelector('.sets-container');
        const sets = setsContainer.querySelectorAll('.set-row');
        sets.forEach((set) => {
            set.querySelector('.remove-set').addEventListener('click', function() {
                setsContainer.removeChild(set);
            });
        });

        const addSetBtn = card.querySelector('.add-set');
        addSetBtn.addEventListener('click', () => addSet(card));
    });

    addExBtn.addEventListener('click', function() {
        const exCard = document.getElementById('exercise-template').cloneNode(true);
        exCard.classList.remove('d-none');
        exCard.removeAttribute('id');
        
        selectCustom(exCard);

        exCard.querySelector('.remove-exercise').addEventListener('click', function() {
            container.removeChild(exCard);
        });

        container.appendChild(exCard);

        const addSetBtn = exCard.querySelector('.add-set');
        addSetBtn.addEventListener('click', () => addSet(exCard));
    });
    

    //Сохранение происходит через button, чтобы не происходила стандартная отправка формы
    saveTempBtn.addEventListener('click', async function() {       
        try{
            await saveWorkoutForm(true);
            showSuccessModal(true);
        } catch(error) {
            showErrorModal();
            hasEmptyRequired();
        }       
    });

    
    saveBtn.addEventListener('click', async function() {
        try{
            await saveWorkoutForm(false);
            showSuccessModal(false);
        } catch(error) {
            showErrorModal();
            hasEmptyRequired();
        }       
    });

    if (!isNew) {
        cancelBtn.addEventListener('click', () => showCancelModal(false));
    }

    closeBtn.addEventListener('click', function() {
        if (isNew || isEditMode) {
            showCancelModal(true);
        } else {
            window.location.href = window.URLS.mainPage;
        }
    });

    //Блокировка отправки формы при submit
    form.addEventListener('submit', async function(e) {
        e.preventDefault();  
    });

    form.querySelectorAll('.input').forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                return false;
            }
        });
    });
    
    function getExercises() {
        const exercises = [];
        const cards = container.querySelectorAll('.card:not(.d-none)');
        
        cards.forEach((card) => {
            const select = card.querySelector('.exercise-select');
            if (!select.value) return;
        
            const sets = getSets(card);
        
            exercises.push({
                exercise_id: select.value,
                sets: sets
            });
        });
        
        return exercises;
    };

    function getSets(card) {
        const sets = [];
        const setsContainer = card.querySelector('.sets-container');
        const setCards = setsContainer.querySelectorAll('.set-row');

        setCards.forEach((setCard) => {
            const weightInput = setCard.querySelector('.weight-input');
            const repsInput = setCard.querySelector('.reps-input');
            const setData = {
                reps: repsInput ? repsInput.value : null
            };
            if (weightInput && $(weightInput).is(':visible')) {
                setData.weight = weightInput.value;
            }
            
            sets.push(setData);
        });

        return sets;
    };

    async function saveWorkoutForm(isTemplate) {
        const formData = new FormData(form);
        const exercises = getExercises();
        formData.append('exercises', JSON.stringify(exercises));
        formData.append('is_template', String(isTemplate));

        try {
            const response = await fetch(form.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
    
            const data = await response.json();

            if (data.status === 'error') {
                throw await data;
            }
            
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }

            return data;
            
        } catch (error) {
            throw error;
        }
    };

    function showSuccessModal(isTemplate) {
        const message = document.getElementById('success-message');
        message.textContent = isTemplate 
          ? 'Шаблон тренировки успешно сохранен!' 
          : 'Тренировка успешно сохранена!';
        
        successModal.show();
    };
    
    function showErrorModal() {
        const errorButton = errorModalEl.querySelector('.again-btn');
  
        errorButton.onclick = () => location.reload();
        errorModal.show();
    };

    function showCancelModal(isClose) {
        const saveButton = cancelModalEl.querySelector('.save-btn');
        const notSaveButton = cancelModalEl.querySelector('.not-save-btn');
        const toMenuButton = cancelModalEl.querySelector('.to-menu-btn');

        saveButton.onclick = async function() {
            try{
                await saveWorkoutForm(false);
                showSuccessModal(false);
            } catch(error) {
                showErrorModal();
                hasEmptyRequired();
            }
        };
        if (isClose) {
            notSaveButton.hidden = true;
        } else {
            toMenuButton.hidden=true;
            notSaveButton.onclick = () => location.reload(); 
        }
        cancelModal.show();
    };
});