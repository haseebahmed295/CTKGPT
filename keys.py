import keyboard

class KeyboardHandler:
    def __init__(self, app):
        self.app = app
        self.keys = {'ctrl+-':self.on_ctrl_minus , 'ctrl+=':self.on_ctrl_plus, 'enter':self.app.prompt}
        self.add_keys(self.keys)

    def add_keys(self , keys):
        for key in keys:
            keyboard.add_hotkey(key, keys[key])
        
    def on_ctrl_minus(self):
        if self.app.font.cget('size') > 1:
            self.app.font.configure(size = self.app.font.cget('size') - 1)
        else:
            self.app.font.configure(size = 2)
        

    def on_ctrl_plus(self):
        if self.app.font.cget('size') > 1:
            self.app.font.configure(size = self.app.font.cget('size') + 1)
        else:
            self.app.font.configure(size = 2)
        