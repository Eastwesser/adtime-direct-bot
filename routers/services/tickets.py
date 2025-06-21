import uuid
from datetime import datetime


def generate_ticket_number():
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    unique_part = uuid.uuid4().hex[:6].upper()
    return f"ATD-{date_part}-{unique_part}"
