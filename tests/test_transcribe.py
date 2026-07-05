import unittest
from unittest.mock import Mock, patch

from lib import transcribe


class WhisperPreloadTests(unittest.TestCase):
    def setUp(self):
        self.old_model = transcribe._model
        self.old_thread = getattr(transcribe, "_preload_thread", None)
        self.old_started = getattr(transcribe, "_preload_started", False)
        transcribe._model = None
        transcribe._preload_thread = None
        transcribe._preload_started = False

    def tearDown(self):
        transcribe._model = self.old_model
        transcribe._preload_thread = self.old_thread
        transcribe._preload_started = self.old_started

    def test_preload_starts_one_daemon_thread(self):
        fake_thread = Mock()
        fake_thread.is_alive.return_value = True

        with patch.object(transcribe.threading, "Thread", return_value=fake_thread) as thread_cls:
            first = transcribe.preload_model_background()
            second = transcribe.preload_model_background()

        self.assertIs(first, fake_thread)
        self.assertIs(second, fake_thread)
        thread_cls.assert_called_once()
        self.assertTrue(thread_cls.call_args.kwargs["daemon"])
        fake_thread.start.assert_called_once()

    def test_preload_worker_uses_local_files_only(self):
        with patch.object(transcribe, "_get_model") as get_model:
            transcribe._preload_worker()

        get_model.assert_called_once_with(local_files_only=True)


if __name__ == "__main__":
    unittest.main()
