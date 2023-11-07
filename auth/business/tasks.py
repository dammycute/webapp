from celery import shared_task
from business.models import Investment
from datetime import datetime

@shared_task
def update_investment_value(investment_id):
    investment = Investment.objects.get(pk=investment_id)
    today = datetime.date.today()
    elapsed_months = (today.year - investment.start_date.year) * 12 + (today.month - investment.start_date.month)
    investment.current_value = investment.total_price * (1 + ((investment.roi / 12) / 100) * elapsed_months)
    investment.save()