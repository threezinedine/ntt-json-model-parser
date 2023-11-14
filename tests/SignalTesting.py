import unittest
from unittest.mock import Mock

from ntt_json_model_parser import Signal


class SignalTesting(unittest.TestCase):
    def test_CallTheCallbackWhenTheSignalIsBind(self):
        sigTestSignal = Signal()
        testCallback = Mock()

        sigTestSignal.AddCallback(testCallback)

        testCallback.assert_called_once()

    def test_CallTheCallbackWhenTheSignalIsEmitted(self):
        sigTestSignal = Signal()
        testCallback = Mock()
        sigTestSignal.AddCallback(testCallback)

        sigTestSignal.Emit()

        self.assertEqual(
            testCallback.call_count,
            2,
            f"The Callback must be called twice but is called {testCallback.call_count}"
        )

    def test_NotCallTheCallbackWhenBindingIfNotRequired(self):
        sigTestSignal = Signal()
        testCallback = Mock()

        sigTestSignal.AddCallback(testCallback, bCalled=False)

        testCallback.assert_not_called()

    def test_SignalWhichIsFollowByAnotherSignal(self):
        sigSrcTestSignal = Signal()
        sigFollowedTestSignal = Signal()
        testCallback = Mock()
        sigFollowedTestSignal.AddCallback(testCallback, bCalled=False)

        sigSrcTestSignal.AttachSignal(sigFollowedTestSignal)

        sigSrcTestSignal.Emit()

        testCallback.assert_called_once()