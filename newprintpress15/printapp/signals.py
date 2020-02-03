from django.dispatch import Signal

send_mail1 = Signal(providing_args=["order"])
