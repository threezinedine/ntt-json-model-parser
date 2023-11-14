from typing import (
    Callable,
    List,
)


class Signal:
    def __init__(self, strName = "Signal") -> None:
        self._strName = strName
        self._cbCallbacks: List[Callable] = []
        self._followedSignals: List = []

    def Emit(self) -> None:
        for cbCallback in self._cbCallbacks:
            cbCallback()

        for signal in self._followedSignals:
            signal.Emit()

    def AddCallback(self, cbCallback: Callable, bCalled: bool = True) -> None:
        self._cbCallbacks.append(cbCallback)

        if bCalled:
            cbCallback()

    def AddCallbacks(self, cbCallbacks: List[Callable], bCalled: bool = True) -> None:
        for cbCallback in cbCallbacks:
            self.AddCallback(cbCallback, bCalled=bCalled)

    def AttachSignal(self, signal) -> None:
        self._followedSignals.append(signal)

    @property
    def Callbacks(self) -> List[Callable]:
        return self._cbCallbacks

    def __repr__(self) -> str:
        return f"<Signal name=\"{self._strName}\" />"