from twilio.rest import Client
import settings

# Twilio Client
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

# Sends a message to the number specified in settings
def send_sms(message):
    message = client.messages.create(
        to = settings.PHONE_NUM,
        from_ = settings.TWILIO_NUM,
        body = message
    )

# Sends all sales
def send_sales(sales):
    msg = ""
    for sale in sales:
        msg += sale + '\n'
    send_sms(msg)