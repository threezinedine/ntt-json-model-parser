from typing import (
    Callable,
    List,
    Any,
)
from .Signal import Signal


class ObservableList(list):
    def __init__(self, *args, strName: str = "Observable List", **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._signal = Signal(strName)

        for element in self:
            if hasattr(element, "_signal"):
                element._signal.AttachSignal(self._signal)

    def Bind(self, cbCallback: Callable[..., Any]) -> None:
        self._signal.AddCallback(cbCallback=cbCallback, bCalled=False)

    def AttachSignal(self, signal: Signal) -> None:
        self._signal.AttachSignal(signal)

    def append(self, __object: Any) -> None:
        self._signal.Emit()
        if hasattr(__object, f"_signal"):
            getattr(__object, "_signal").AttachSignal(self._signal)
        return super().append(__object)

    def insert(self, __index , __object: Any) -> None:
        self._signal.Emit()
        if hasattr(__object, f"_signal"):
            getattr(__object, "_signal").AttachSignal(self._signal)
        return super().insert(__index, __object)

    def remove(self, __value: Any) -> None:
        self._signal.Emit()
        return super().remove(__value)

    def pop(self, __index = -1) -> Any:
        self._signal.Emit()
        return super().pop(__index)

    def clear(self) -> None:
        self._signal.Emit()
        return super().clear()

    def _ClearWithoutNotifying(self) -> None:
        super().clear()

    def __repr__(self) -> str:
        return f"<Observable List {super().__repr__()} at {id(self)}/>"