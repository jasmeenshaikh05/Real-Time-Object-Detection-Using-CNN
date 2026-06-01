alerts = []

def add_alert(message):

    alerts.insert(0,message)

    if len(alerts) > 20:
        alerts.pop()

def get_alerts():
    return alerts