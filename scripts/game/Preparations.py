from scripts.game.Exceptions import DuressException
from scripts.DI.DI import di
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name

pics = di.get('pics')


class Preparations(FunctionNameDecorator):
    def __init__(self, secrets, mpysin, mp):
        FunctionNameDecorator.__init__(self, mp.print)
        self.secrets = secrets
        self.mpysin = mpysin
        self.mp = mp

    @name
    def run(self):
        self.start_app()
        self.login()
        self.navigate_to_main_menu()
        self.finalize()

    @name
    def start_app(self):
        if not self.mpysin.check_point_multiple(
            i=100, dur=1, pics=[
                    {**pics.homescreen},
                    {**pics.home_active_btn},
                    {**pics.transfers_active_btn}
                ]
        ):
            self.mp.print('raising DuressException because critical check_point_multiple failed')
            raise DuressException

        if self.mpysin.locate(**pics.homescreen):
            self.mpysin.start_app()

    @name
    def login(self):
        skip = [pics.home_active_btn, pics.transfers_active_btn]
        for pic in skip:
            if self.mpysin.locate(**pic):
                self.mp.print('already logged in')
                return
        login_btn =  self.mpysin.locate(**pics.login_btn)
        if login_btn:
            self.mpysin.click(*login_btn, dur=2)
            pwd_field = self.mpysin.wait_for(i=10, dur=1, **pics.enter_pwd_field)
            if not pwd_field:
                self.mp.print('raising DuressException because critical part of login failed')
                raise DuressException
            self.mpysin.click(*pwd_field)
            self.mpysin.typewrite(self.secrets.fifa_password)
            self.mpysin.enter(dur=5)

    @name
    def navigate_to_main_menu(self):
        if self.mpysin.locate(**pics.home_active_btn):
            return
        home_inactive_btn = self.mpysin.locate(**pics.home_inactive_btn)
        if home_inactive_btn:
            self.mpysin.click(home_inactive_btn, dur=2)

    @name
    def finalize(self):
        # ToDo add checkpoint dass wir auch wirklich im home menu sind
        pass

