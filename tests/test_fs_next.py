"""Run FS Next's contract on an isolated Moto backend; no AWS account is used."""

import unittest
from importlib.metadata import PackageNotFoundError, distribution, requires, version

import boto3
from moto import mock_aws
from packaging.requirements import Requirement
import fs
import fs_s3fs
from fs import open_fs
from fs.test import FSTestCases
from fs_s3fs import S3FS


class TestFSNext(FSTestCases, unittest.TestCase):
    prefix = ""

    def setUp(self):
        self.mock = mock_aws()
        self.mock.start()
        self.addCleanup(self.mock.stop)
        client = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id="testing",
            aws_secret_access_key="testing",
        )
        client.create_bucket(Bucket="fs-next-tests")
        super().setUp()

    def make_fs(self):
        return S3FS(
            "fs-next-tests",
            dir_path=self.prefix,
            aws_access_key_id="testing",
            aws_secret_access_key="testing",
            region="us-east-1",
        )

    def test_distribution_and_opener(self):
        self.assertTrue(version("fs-next"))
        self.assertIn("site-packages", fs.__file__)
        self.assertIn("site-packages", fs_s3fs.__file__)
        with self.assertRaises(PackageNotFoundError):
            version("fs")
        url = "s3://testing:testing@fs-next-tests"
        with open_fs(url) as storage:
            storage.writetext("한글.txt", "FS Next")
        with open_fs(url) as storage:
            self.assertEqual(storage.readtext("한글.txt"), "FS Next")
            storage.remove("한글.txt")


class TestFSNextPrefix(TestFSNext):
    prefix = "subdirectory"


def test_distribution_metadata():
    package = distribution("fs-s3fs-next")
    assert package.version == "0.1.0"
    assert package.metadata["Requires-Python"] == ">=3.10"
    dependencies = [Requirement(value) for value in requires("fs-s3fs-next")]
    assert [d.name for d in dependencies if d.name in ("fs", "fs-next")] == ["fs-next"]
    assert not any(d.name in ("setuptools", "pkg_resources", "fs-s3fs") for d in dependencies)
    assert any(ep.group == "fs.opener" and ep.name == "s3" for ep in package.entry_points)
    for name in ("fs", "fs-s3fs"):
        with unittest.TestCase().assertRaises(PackageNotFoundError):
            version(name)
