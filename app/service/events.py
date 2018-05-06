import env
from app.bot.funny_bot import FunnyBot
from singleton_repo import repo
from singleton_analytic import analytic

bot = FunnyBot()


class Events(object):

    def __init__(self):
        self.trigger_humor = 'humor'
        self.trigger_meme = 'meme'
        self.trigger_analytic = 'analise'
        self.triggers = {
            self.trigger_humor: self.store_humor,
            self.trigger_meme: self.get_meme,
            self.trigger_analytic: self.send_analytic_week
        }

    def send_analytic_week(self, message, image_name):
        data = repo.get_last_week()
        analize_path = analytic.analyze_report_humor(data, image_name=image_name)
        return '{}/{}'.format(env.APP_URL, analize_path)

    def store_humor(self, message, user_id, user_name):
        formated = message.split(' ')
        if len(formated) < 1:
            return 'Ops! Para salvar seu humor diario voce precisa mandar assim: {}: humor [sua nota de 0 a 5] [descricao sobre sua nota(opcional)]'.format(env.NAME_BOT)

        note = formated[0]
        description = ' '.join(formated[1:]) if len(formated) > 1 else ''
        repo.store_report('daily_report', user_id, user_name, note, description)

        return 'Ok! Obrigado! {}'.format(user_name)

    def get_meme(self, message):
        meme = bot.analyze_response(message)
        return meme

    def store_user(self, user_id, user_name):
        repo.insert_user(user_id, user_name)