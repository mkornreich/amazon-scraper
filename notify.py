from current_time import current_time
from database import get_key, insert_value
from logger import logger
import resend

def notify():
    logger.info("Trying to send email")
    try:
        resend.api_key = get_key("api_key")
        body = "Item name: " + get_key("name") + "\n"
        body += "Item price: " + get_key("price")
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": get_key("email_to"),
            "subject": "Amazon iPad Price Drop",
            "html": body
        })
        logger.info("Email sent successfully")
    except Exception as e:
        log = "Failed to send email. {e}".format(e = e)
        logger.error(log)
    insert_value("time_email",current_time())
