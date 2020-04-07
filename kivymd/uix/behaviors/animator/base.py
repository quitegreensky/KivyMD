from kivy.clock import Clock
from kivy.graphics import PushMatrix, PopMatrix, Color, Rectangle, Rotate
from functools import partial
import time


class Animator:
    """
	Animator
	========
	Base Class for Animators

	Parameters
	----------
	widget: widget to be animated

	duration: [optional], defaults to 1

	repeat: [optional], defaults to True
	
	Attributes
	----------
	anim_complete:
		Called internally upon completition of an animation

	_initialize:
		Used to set properties of the 'widget' prior to animation

	"""

    def __init__(self, widget, duration=1, repeat=True):
        self.widget = widget
        self.duration = duration
        self._repeat = repeat
        self._original = {}
        self.attr = ["opacity", "height", "width", "pos_hint", "angle"]

        setattr(self.widget, "origin_", "")
        setattr(self.widget, "angle", 0)
        setattr(self.widget, "axis", tuple((0, 0, 1)))

        for key in self.attr:
            self._original[key] = getattr(self.widget, key)

    @classmethod
    def anim_complete(cls, obj, inst, widget):
        if obj._repeat:
            for key, val in obj._original.items():
                setattr(widget, key, val)
            obj._update_canvas()

            inst.unbind(on_complete=obj.anim_complete)
            time.sleep(0.3)  # just to make repeatition visually clear
            Clock.schedule_once(partial(obj.start_,), 0)

        else:
            inst.stop(widget)

    def _initialize(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self.widget, key, val)
        self._update_canvas()

    def _animate(self, anim_obj):
        self._update_canvas()  # this is to reset any previous animation value
        anim_obj.cancel_all(self.widget)
        anim_obj.bind(on_progress=self._update_canvas)
        anim_obj.bind(on_complete=partial(self.anim_complete, self))
        anim_obj.start(self.widget)

    def _update_canvas(self, *args):
        self.widget.canvas.before.remove_group("animator_group")
        with self.widget.canvas.before:
            PushMatrix(group="animator_group")
            dsh = {
                "axis": getattr(self.widget, "axis"),
                "angle": getattr(self.widget, "angle"),
                "origin": getattr(self.widget, "origin_")
                or getattr(self.widget, "center"),
            }
            Rotate(**dsh, group="animator_group")
        self.widget.canvas.after.remove_group("animator_group")
        with self.widget.canvas.after:
            PopMatrix(group="animator_group")
