import { getCSRFToken, hasEmptyRequired, showErrorModal } from './functions.js';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('workout-form');
    const exercisesContainer = document.getElementById('exercises-container');

    const pageDate = form.querySelector('#workout-form input[name="date"]').value;

    const checkNew = document.getElementById('is-new');
    const isNew = (JSON.parse(checkNew.value.toLowerCase()));

    const checkEditMode = document.getElementById('edit-mode');
    let isEditMode = !(JSON.parse(checkEditMode.value.toLowerCase()));
    let sortable = new Sortable(exercisesContainer, {
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
    const cancelModalEl = document.getElementById('cancel-modal');
    const closeBtn = document.getElementById('close-btn');
    
    const successModal = new bootstrap.Modal(successModalEl);
    const cancelModal = new bootstrap.Modal(cancelModalEl);

    if (isNew) {
        const templateSelect = document.getElementById('template-select');
        $(templateSelect).select2({
            ajax: {
                url: window.URLS.templateSearch,
                dataType: 'json',
                processResults: function(data) {
                    return {
                        results: data.results.map(item => {
                            return {
                                id: item.id,
                                text: item.text
                            };
                        })
                    };
                }
            },
            closeOnSelect: true,
            templateResult: function(item) {
                return item.text;
            },
            templateSelection: function(item) {
                return item.text;
            }
        });
        $(templateSelect).on('change.select2', function() {
            if (!$(this).val()) {
                fillWorkoutForm(null);
                return;
            }
            const selectedData = $(this).select2('data')[0];
            const templateId = selectedData.id;
            fetch(`${window.URLS.templateLoad}/${templateId}`)
                .then(response => response.json())
                .then(response => {
                    if (response.status === 'error') {
                        showErrorModal(response.message);
                        return;
                    }
                    const data = response.data;
                    fillWorkoutForm(data);
                });
        });

        const templateSelectReset = document.getElementById('reset-template');
        templateSelectReset.onclick = () => {
            $(templateSelect).val('').trigger('change');
        };
    }

    function fillWorkoutForm(data) {
        form.querySelector('#workout-form input[name="name"]').value = data?.name || '';
        form.querySelector('#workout-form input[name="date"]').value = pageDate;
        
        exercisesContainer.innerHTML = '';
        
        if (!data || !data.workout_exercises) {
            return;
        }
        
        data.workout_exercises.forEach((exercise) => {
            const exCard = document.getElementById('exercise-template').cloneNode(true);
            exCard.classList.remove('d-none');
            exCard.removeAttribute('id');
            
            const setsContainer = exCard.querySelector('.sets-container');
            setsContainer.innerHTML = '';
            
            exercise.ordered_sets.forEach((exercise_set) => {
                const set = document.getElementById('set-template').cloneNode(true);
                set.classList.remove('d-none');
                set.removeAttribute('id');

                set.querySelector('.reps-input').value = exercise_set.reps;

                set.querySelector('.weight-input').parentElement.hidden = exercise.is_own_weight;
                set.querySelector('.weight-input').required = !exercise.is_own_weight;
                set.querySelector('.weight-input').value = exercise_set.weight || '';
                
                set.querySelector('.remove-set').addEventListener('click', function() {
                    set.remove();
                });
                
                setsContainer.appendChild(set);
            });
            
            exCard.querySelector('.remove-exercise').addEventListener('click', function() {
                exCard.remove();  
            });
            
            exerciseSelect(exCard);
            const select = exCard.querySelector('.exercise-select');
            const option = new Option(exercise.exercise_name, exercise.exercise_id);
            $(option).attr('data-is-own-weight', exercise.is_own_weight.toString());
            select.appendChild(option);
            $(select).val(exercise.exercise_id).trigger('change');
            
            exCard.querySelector('.add-set').addEventListener('click', function() {
                addSet(exCard);
            });

            exercisesContainer.appendChild(exCard);
        });
    }

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

    changeEditMode();

    if (!isNew) {
        editBtn.addEventListener('click', changeEditMode);
    }

    async function exerciseSelect(card) {
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
            closeOnSelect: true,
            templateResult: function(item) {
                return item.text;
            },
            templateSelection: function(item) {
                if (item.is_own_weight) {
                    const selectedOption = select.options[select.selectedIndex];
                    $(selectedOption).attr('data-is-own-weight', item.is_own_weight.toString());
                }
                return item.text;
            }
        });
        $(select).on('change', function() {
            const isOwnWeight = select.options[select.selectedIndex].getAttribute('data-is-own-weight');
            const isOwnWeightBool = isOwnWeight === 'true';

            const inputs = card.querySelectorAll('.weight-input');
            inputs.forEach((input) => {
                input.parentElement.hidden = isOwnWeightBool;
                input.required = !isOwnWeightBool;
                if (isOwnWeightBool) {
                    input.value = '';
                }
            });
        });
    };

    function addSet(card) {
        const select = card.querySelector('.exercise-select');
        if (!$(select).val()) return;
        const isOwnWeight = select.options[select.selectedIndex].getAttribute('data-is-own-weight');
        const isOwnWeightBool = isOwnWeight === 'true';

        const set = document.getElementById('set-template').cloneNode(true);
        set.classList.remove('d-none');
        set.removeAttribute('id');
        
        set.querySelector('.weight-input').parentElement.hidden = isOwnWeightBool;
        set.querySelector('.weight-input').required = !isOwnWeightBool;

        const setsContainer = card.querySelector('.sets-container');
        
        set.querySelector('.remove-set').addEventListener('click', function() {
            setsContainer.removeChild(set);
        });

        setsContainer.appendChild(set);
    };

    const cards = document.querySelectorAll('.card:not(.d-none)');
    cards.forEach((card) => {
        exerciseSelect(card);

        card.querySelector('.remove-exercise').addEventListener('click', function() {
            exercisesContainer.removeChild(card);
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
        
        exerciseSelect(exCard);

        exCard.querySelector('.remove-exercise').addEventListener('click', function() {
            exercisesContainer.removeChild(exCard);
        });

        exercisesContainer.appendChild(exCard);

        const addSetBtn = exCard.querySelector('.add-set');
        addSetBtn.addEventListener('click', () => addSet(exCard));
    });
    

    saveTempBtn.addEventListener('click', async function() {       
        try{
            await saveWorkoutForm(true);
            showSuccessModal(true);
        } catch(error) {
            if (error.message) {
                showErrorModal(error.message);
            } else {
                showErrorModal('Ошибка сохранения!');
            }
            hasEmptyRequired();
        }       
    });

    
    saveBtn.addEventListener('click', async function() {
        try{
            await saveWorkoutForm(false);
            showSuccessModal(false);
        } catch(error) {
            if (error.message) {
                showErrorModal(error.message);
            } else {
                showErrorModal('Ошибка сохранения!');
            }
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
        const cards = exercisesContainer.querySelectorAll('.card:not(.d-none)');
        
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

    function showCancelModal(isClose) {
        const saveButton = cancelModalEl.querySelector('.save-btn');
        const notSaveButton = cancelModalEl.querySelector('.not-save-btn');
        const toMenuButton = cancelModalEl.querySelector('.to-menu-btn');

        saveButton.onclick = async function() {
            try{
                await saveWorkoutForm(false);
                showSuccessModal(false);
            } catch(error) {
                showErrorModal('Ошибка сохранения!');
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