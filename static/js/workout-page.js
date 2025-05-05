import { getCSRFToken } from './functions.js';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('workout-form');
    const container = document.getElementById('exercises-container');
    const addExBtn = document.getElementById('add-exercise');
    const saveTempBtn = document.getElementById('save-template');
    const saveBtn = document.getElementById('save-workout');
    const successModalEl = document.getElementById('success-modal');
    const errorModalEl = document.getElementById('error-modal');
    const successModal = new bootstrap.Modal(successModalEl);
    const errorModal = new bootstrap.Modal(errorModalEl);
    let exerciseTag = 0;
    let setTag = 0;

    addExBtn.addEventListener('click', function() {
        const exTemplate = document.getElementById('exercise-template').cloneNode(true);
        exTemplate.classList.remove('d-none');
        exTemplate.id = 'exercise-' + exerciseTag;
        const select = exTemplate.querySelector('.exercise-select');
        
        ++exerciseTag;

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
                $(exTemplate).find('.weight-input').parent().hide();
            } else {
                $(exTemplate).find('.weight-input').parent().show();
            }
        });
        
        

        exTemplate.querySelector('.remove-exercise').addEventListener('click', function() {
            container.removeChild(exTemplate);
        });

        container.appendChild(exTemplate);

        const addSetBtn = exTemplate.querySelector('.add-set');
        addSetBtn.addEventListener('click', function() {
            const selectedData = $(select).select2('data')[0];
            if (!selectedData) return;

            const setTemplate = document.getElementById('set-template').cloneNode(true);
            setTemplate.classList.remove('d-none');
            setTemplate.id = 'set-' + setTag;
            ++setTag;
            
            if (selectedData.is_own_weight) {
                $(setTemplate).find('.weight-input').parent().hide();
            } else {
                $(setTemplate).find('.weight-input').parent().show();
            }

            const setsContainer = exTemplate.querySelector('.sets-container');
            
            setTemplate.querySelector('.remove-set').addEventListener('click', function() {
                setsContainer.removeChild(setTemplate);
            });

            setsContainer.appendChild(setTemplate);
        });

        
    });


    //Сохранение происходит через button, чтобы не происходила стандартная отправка формы
    saveTempBtn.addEventListener('click', async (e) => {
        e.preventDefault();        
        try{
            await saveWorkoutForm(true);
            showSuccessModal(true);
        } catch(error) {
            showErrorModal();
        }       
    });

    saveBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        try{
            await saveWorkoutForm(false);
            showSuccessModal(false);
        } catch(error) {
            showErrorModal();
        }       
    });

    //Блокирую отправку формы при submit
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
    }

    function getSets(card) {
        const sets = [];
        const setsContainer = card.querySelector('.sets-container');
        const setCards = setsContainer.querySelectorAll('.set-row');;

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
    }

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
    }

    function showSuccessModal(isTemplate) {
        const message = document.getElementById('success-message');
        message.textContent = isTemplate 
          ? 'Шаблон тренировки успешно сохранен!' 
          : 'Тренировка успешно сохранена!';
        
        successModal.show();
    }
    
    function showErrorModal() {
        const errorButton = document.getElementById('error-modal-button');
  
        errorButton.onclick = () => location.reload();
        errorModal.show();
    }
});