from app import celery
from app import app
from app import mail
from flask_mail import Message

REG_MESSAGE_TEMPLATE = 'Добрый день!\nНа ваш адрес почты был только что зарегистрирован аккаунт ' \
                       'на сайте quack-chat.ru под логином <b>{login}</b>\n' \
                       'Если это произошло по ошибке, просто проигнорируйте это письмо.'


@celery.task()
def add_together(a, b):
    return a + b


@celery.task(soft_time_limit=3, time_limit=10)
def send_registration_mail(user_email, nick):
    message = Message('Hello from Quack team!',
                      sender=app.config['ADMINS'][0], recipients=[user_email])
    message.html = REG_MESSAGE_TEMPLATE.format(login=nick)

    with app.app_context():
        mail.send(message)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task\
        (10.0,
         send_registration_mail.s('1alekseik1@gmail.com', 'alekseik1'),
         name='TEST ONLY: Send email every 10 seconds'
         )
    celery.conf.timezone = 'UTC'
