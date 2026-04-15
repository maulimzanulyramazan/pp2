from datetime import datetime, timedelta
current_data = datetime.now()
aftertendays = current_data + timedelta(days=30)
print(current_data.strftime("%d/%m/%Y , %H:%M:%S"))
print(aftertendays.strftime("%d/%h/%y , %H:%M:%S"))