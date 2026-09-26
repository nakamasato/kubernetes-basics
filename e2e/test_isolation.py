import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from run import run


class IsolationTest(unittest.TestCase):
    def exercise(self, fail_at=None):
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory) / "user-config"
            original.write_text("current-context: production\n")

            def command(argv, **kwargs):
                calls.append((argv, kwargs["env"].copy()))
                if len(calls) == fail_at:
                    raise subprocess.CalledProcessError(1, argv)

            with patch.dict(os.environ, {"KUBECONFIG": str(original), "E2E_ARTIFACTS": directory}):
                with patch("run.subprocess.run", side_effect=command):
                    if fail_at:
                        with self.assertRaises(subprocess.CalledProcessError):
                            run("pod")
                    else:
                        run("pod")
                self.assertEqual(os.environ["KUBECONFIG"], str(original))
            self.assertEqual(original.read_text(), "current-context: production\n")
            self.assertEqual(calls[-1][0][:3], ["kind", "delete", "cluster"])
            config = calls[0][1]["KUBECONFIG"]
            self.assertNotEqual(config, str(original))
            self.assertFalse(Path(config).parent.exists())
            for argv, env in calls:
                self.assertEqual(env["KUBECONFIG"], config)
                self.assertTrue(env["E2E_CONTEXT"].startswith("kind-kb-e2e-pod-"))
                if argv[0] == "kind" and argv[1] in ("create", "delete"):
                    self.assertEqual(argv[argv.index("--kubeconfig") + 1], config)

    def test_success(self):
        self.exercise()

    def test_creation_failure(self):
        self.exercise(fail_at=1)

    def test_suite_failure(self):
        self.exercise(fail_at=2)
