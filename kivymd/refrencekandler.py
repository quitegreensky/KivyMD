from kivy.uix.widget import Widget


class RefrenceHandler(Widget):
    def __init__(self, **kw):
        self._currently_bound_properties = []
        super().__init__(**kw)

    # def on_parent(self,*args):
    #     if not self.parent:
    #         print("removed")
    #         for p in self._currently_bound_properties:
    #             self.theme_cls.unbind(**p)

    def dec_disabled(self, *args, **kw):
        for p in self._currently_bound_properties:
            self.theme_cls.unbind(**p)
        super().dec_disabled(*args, **kw)
