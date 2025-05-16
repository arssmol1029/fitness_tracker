import { getCSRFToken } from './functions.js';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.prev-month, .next-month').forEach(button => {
        button.addEventListener('click', function() {
            anotherMonth(this);
        });
    });

    async function anotherMonth(button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';

        const [year, month] = button.value.split('-');
        fetch(`${window.URLS.mainPage}?year=${year}&month=${month}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => updateCalendar(data))
        .finally(() => {
            button.disabled = false;
            button.innerHTML = button.classList.contains('prev-month') 
                ? '<i class="bi bi-chevron-left"></i>' 
                : '<i class="bi bi-chevron-right"></i>';
        });
    }

    function updateCalendar(data) {
        document.querySelector('.month-title').textContent = data.month_name;
        
        document.querySelector('.prev-month').value = data.prev_month;
        document.querySelector('.next-month').value = data.next_month;
        
        const calendarGrid = document.querySelector('.calendar-grid');
        calendarGrid.innerHTML = '';
        
        const weekdaysRow = document.createElement('div');
        weekdaysRow.className = 'row weekdays text-center mb-2';
        
        data.weekdays.forEach(day => {
            const dayCol = document.createElement('div');
            dayCol.className = 'col p-2';
            dayCol.innerHTML = `<strong>${day}</strong>`;
            weekdaysRow.appendChild(dayCol);
        });
        
        calendarGrid.appendChild(weekdaysRow);
        
        data.weeks.forEach(week => {
            const weekRow = document.createElement('div');
            weekRow.className = 'row week';
            
            week.forEach(day => {
                const dayCell = document.createElement('div');
                dayCell.className = `col p-2 day-cell text-center ${day.is_today ? 'bg-primary bg-opacity-10' : ''}`;
                
                if (day.in_month) {
                    dayCell.innerHTML = `
                        <a href=${window.URLS.workoutDay}?date=${day.date_str} 
                            class="day-link d-block rounded-circle mx-auto 
                            ${day.has_workout ? 'bg-success text-white' : 'text-dark'}"
                            style="width: 36px; height: 36px; line-height: 36px;">
                            ${day.day_num}
                        </a>
                    `;
                } else {
                    dayCell.innerHTML = '<span class="d-block text-muted">―</span>';
                }

                weekRow.appendChild(dayCell);
            });
            
            calendarGrid.appendChild(weekRow);
        });
    }
})