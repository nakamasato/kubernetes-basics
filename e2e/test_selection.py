import unittest

from run import TARGETS, select


class SelectionTest(unittest.TestCase):
    def test_unrelated(self):
        self.assertEqual(select(["README.md", "08-setup-eks-cluster/README.md"]), [])

    def test_manifest_or_chapter_documentation(self):
        self.assertEqual(select(["05-kubernetes-resources/04-deployment/deployment.yaml"]), ["deployment"])
        self.assertEqual(select(["04-kubectl/README.md"]), ["kubectl"])

    def test_suite(self):
        self.assertEqual(select(["e2e/suites/service.sh"]), ["service"])

    def test_shared(self):
        for path in ["e2e/run.py", "e2e/lib.sh", ".github/workflows/e2e.yml"]:
            self.assertEqual(select([path]), list(TARGETS))

    def test_multiple_and_deleted_paths(self):
        self.assertEqual(select(["04-kubectl/deleted.yaml", "07-debug-kubernetes/a.yaml",
                                 "04-kubectl/pod-test.yaml"]), ["kubectl", "debug"])
