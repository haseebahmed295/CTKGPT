
class KeyboardHandler:
    def __init__(self, app):
        self.app = app
        self.app.bind('<Control-minus>', self.on_ctrl_minus)
        self.app.bind('<Control-equal>', self.on_ctrl_plus)
        self.app.bind('<Return>', self.on_enter)
    def on_ctrl_minus(self, event=None):
        current_size = self.app.font.cget('size')
        if current_size > 1:
            self.app.font.configure(size=current_size - 1)

    def on_ctrl_plus(self, event=None):
        self.app.font.configure(size=self.app.font.cget('size') + 1)

    def on_enter(self, event=None):
        self.app.prompt()