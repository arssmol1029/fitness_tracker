import { getCSRFToken } from './functions.js';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('workout-form');
    const container = document.getElementById('exercises-container');
    const addBtn = document.getElementById('add-exercise');
    const saveTempBtn = document.getElementById('save-template');
    const saveBtn = document.getElementById('save-workout');
    const successModalEl = document.getElementById('success-modal');
    const errorModalEl = document.getElementById('error-modal');
    const successModal = new bootstrap.Modal(successModalEl);
    const errorModal = new bootstrap.Modal(errorModalEl);
    let currentTag = 0;

    addBtn.addEventListener('click', function() {
        const template = document.getElementById('exercise-template').cloneNode(true);
        template.classList.remove('d-none');
        template.id = 'exercise-' + currentTag;
    
        const select = template.querySelector('.exercise-select');
        select.name = 'exercise_' + currentTag;
        
        const setsInput = template.querySelector('.sets-input');
        setsInput.name = 'sets_' + currentTag;
        
        ++currentTag;

        $(select).select2({
            ajax: {
                url: window.URLS.exerciseSearch,
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return { term: params.term };
                },
                processResults: function(data) {
                    return { results: data.results };
                }
            }
        });
        
        template.querySelector('.remove-exercise').addEventListener('click', function() {
            container.removeChild(template);
        });
        
        container.appendChild(template);
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

    form.querySelectorAll('input').forEach(input => {
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
            const sets = card.querySelector('.sets-input');
            
            exercises.push({
                exercise_id: select.value,
                sets: sets.value
            });
        });
        
        return exercises;
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