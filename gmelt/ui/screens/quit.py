from .base import ConfirmScreen


class QuitScreen(ConfirmScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "Are you sure you want to quit?",
            cancel="[C]ancel",
            *args,
            **kwargs,
        )

        def key_q(self) -> None:
            self.dismiss(True)

        def key_c(self) -> None:
            self.dismiss(False)
