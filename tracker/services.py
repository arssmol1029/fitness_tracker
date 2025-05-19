from django.utils import timezone
from datetime import date, timedelta
from calendar import monthrange, monthcalendar
from .models import Workout

class WorkoutCalendar:
    @staticmethod
    def get_month_data(user, year=None, month=None):
        today = timezone.now().date()
        year = year or today.year
        month = month or today.month
        
        weeks = monthcalendar(year, month)
        workout_dates = set(Workout.objects.filter(
            user=user,
            date__month=month,
            date__year=year,
            is_template=False
        ).values_list('date', flat=True))
        
        calendar_weeks = []
        for week in weeks:
            week_days = []
            for day in week:
                day_date = date(year, month, day) if day else None
                week_days.append({
                    'date_str': day_date.strftime('%Y-%m-%d') if day_date else None,
                    'day_num': day,
                    'in_month': bool(day),
                    'has_workout': day_date in workout_dates if day else False,
                    'is_today': day_date == today if day else False
                })
            calendar_weeks.append(week_days)
        
        calendar_data = {
            'weeks': calendar_weeks,
            'month_name': date(year, month, 1).strftime('%B %Y'),
            'weekdays': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'prev_month': (date(year, month, 1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m'),
            'next_month': (date(year, month, 28) + timedelta(days=4)).replace(day=1).strftime('%Y-%m'),
            'today': timezone.now().date().strftime('%Y-%m-%d')
        }
        
        return calendar_data