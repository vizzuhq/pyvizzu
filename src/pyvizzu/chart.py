import abc
import uuid

from pyvizzu.animation import Animation, AnimationMerger
from pyvizzu.method import Animate, Feature, Store
from pyvizzu.template import DisplayTarget


class Chart:
    def __init__(
        self,
        display: DisplayTarget,
    ):
        self._chart_id = uuid.uuid4().hex[:7]

        self._display_target = DisplayTarget(display)
        self._set_display_template()
        self._calls = []
        self._showed = False

        self._scroll_into_view = False

    @property
    def scroll_into_view(self):
        return self._scroll_into_view

    @scroll_into_view.setter
    def scroll_into_view(self, scroll_into_view):
        self._scroll_into_view = bool(scroll_into_view)

    def animate(self, *animations: Animation, **options):
        if not animations:
            raise ValueError("No animation was set.")

        animation = self._merge_animations(animations)
        animate = Animate(animation, options)

        self._display(
            self._display_template.ANIMATE.format(
                display_target=self._display_target,
                chart_id=self._chart_id,
                scroll=str(self._scroll_into_view).lower(),
                **animate.dump(),
            )
        )

    @staticmethod
    def _merge_animations(animations):
        if len(animations) == 1:
            return animations[0]

        merger = AnimationMerger()
        for animation in animations:
            merger.merge(animation)

        return merger

    def feature(self, name, enabled):
        self._display(
            self._display_template.FEATURE.format(
                chart_id=self._chart_id,
                **Feature(name, enabled).dump(),
            )
        )

    @abc.abstractmethod
    def store(self):
        snapshot_id = uuid.uuid4().hex[:7]
        self._display(
            self._display_template.STORE.format(
                chart_id=self._chart_id, **Store(snapshot_id).dump()
            )
        )
        return snapshot_id

    @abc.abstractmethod
    def _display(self, javascript):
        """
        Display or collect javascript code.
        """

        assert not self._showed, "cannot be used after chart.show()"
        self._calls.append(javascript)

    @abc.abstractmethod
    def _set_display_template(self):
        """
        Set display template.
        """

    @abc.abstractmethod
    def show(self):
        """
        Display collected javascript code.
        """
