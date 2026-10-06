FS S3FS Next
============

S3FS is a `PyFilesystem <https://www.pyfilesystem.org/>`__ interface to
Amazon S3 cloud storage.

As a PyFilesystem concrete class,
`S3FS <http://fs-s3fs.readthedocs.io/en/latest/>`__ allows you to work
with S3 in the same way as any other supported filesystem.

Independent maintenance fork of `PyFilesystem/s3fs <https://github.com/PyFilesystem/s3fs>`_
by Will McGugan and contributors. Original MIT license and Git history are
preserved. This is not an official PyFilesystem release. Requires Python 3.10+;
uses `FS Next <https://github.com/kmsk99/fs-next>`_ while retaining the
``fs_s3fs`` import and ``s3://`` opener.

Migration
---------

Create a fresh virtual environment and replace ``fs-s3fs`` with
``fs-s3fs-next`` and ``fs`` with ``fs-next`` in your dependency declarations.
Regenerate lock files. Do not install either pair together: they provide the
same Python modules, and uninstalling one can break the other. Packages that
still require ``fs`` or ``fs-s3fs`` must update their dependency metadata first.
A constraints file cannot substitute distribution names.

::

    python -m venv .venv-next
    # Activate the environment, then:
    python -m pip install fs-s3fs-next==0.1.0
    python -m pip check

For uv or Poetry projects, make the same declaration replacements, regenerate
the lock, and sync into a fresh environment. The fork uses its own version
series: 0.1.0 is based on upstream 1.1.1 plus compatibility fixes.
To roll back, restore the previous declarations and lock into another fresh
environment rather than co-installing the packages.

Installing
----------

You can install S3FS from pip as follows:

::

    python -m pip install fs-s3fs-next

Opening a S3FS
--------------

Open an S3FS by explicitly using the constructor:

.. code:: python

    from fs_s3fs import S3FS
    s3fs = S3FS('mybucket')

Or with a FS URL:

.. code:: python

      from fs import open_fs
      s3fs = open_fs('s3://mybucket')

Downloading Files
-----------------

To *download* files from an S3 bucket, open a file on the S3 filesystem
for reading, then write the data to a file on the local filesystem.
Here's an example that copies a file ``example.mov`` from S3 to your HD:

.. code:: python

    from fs.tools import copy_file_data
    with s3fs.open('example.mov', 'rb') as remote_file:
        with open('example.mov', 'wb') as local_file:
            copy_file_data(remote_file, local_file)

Although it is preferable to use the higher-level functionality in the
``fs.copy`` module. Here's an example:

.. code:: python

    from fs.copy import copy_file
    copy_file(s3fs, 'example.mov', './', 'example.mov')

Uploading Files
---------------

You can *upload* files in the same way. Simply copy a file from a source
filesystem to the S3 filesystem. See `Moving and
Copying <https://docs.pyfilesystem.org/en/latest/guide.html#moving-and-copying>`__
for more information.

ExtraArgs
---------

S3 objects have additional properties, beyond a traditional filesystem.
These options can be set using the ``upload_args`` and ``download_args``
properties. which are handed to upload and download methods, as
appropriate, for the lifetime of the filesystem instance.

For example, to set the ``cache-control`` header of all objects uploaded
to a bucket:

.. code:: python

    import fs, fs.mirror
    s3fs = S3FS('example', upload_args={"CacheControl": "max-age=2592000", "ACL": "public-read"})
    fs.mirror.mirror('/path/to/mirror', s3fs)

see `the Boto3
docs <https://boto3.readthedocs.io/en/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS>`__
for more information.

``acl`` and ``cache_control`` are exposed explicitly for convenience,
and can be used in URLs. It is important to URL-Escape the
``cache_control`` value in a URL, as it may contain special characters.

.. code:: python

    import fs, fs.mirror
    with fs.open_fs('s3://example?acl=public-read&cache_control=max-age%3D2592000%2Cpublic') as s3fs:
        fs.mirror.mirror('/path/to/mirror', s3fs)

S3 URLs
-------

You can get a public URL to a file on a S3 bucket as follows:

.. code:: python

    movie_url = s3fs.geturl('example.mov')

Documentation
-------------

-  `PyFilesystem Wiki <https://www.pyfilesystem.org>`__
-  `S3FS Reference <http://fs-s3fs.readthedocs.io/en/latest/>`__
-  `PyFilesystem
   Reference <https://docs.pyfilesystem.org/en/latest/reference/base.html>`__

FS Next migration for Python 3.10+
----------------------------------

The migration includes ``preserve_time`` argument compatibility, safe same-path
copy/move handling and binary stream ``mode`` / ``readinto`` corrections.
S3 controls LastModified timestamps; ``preserve_time=True`` is best effort and
does not preserve S3's LastModified value (``setinfo`` cannot change it).

To run the complete FS Next contract on bucket roots and prefixes without an
AWS account or credentials::

    python -m pip install . pytest "moto[s3]==5.2.3"
    python -m pip check
    python -I -m pytest tests/test_fs_next.py -q -ra

Moto exercises local S3 API behavior. It does not certify live AWS IAM,
network failures or provider-specific behavior. This package is independently maintained and released. Related upstream fixes
were already proposed in `PR #81 <https://github.com/PyFilesystem/s3fs/pull/81>`_
(readinto) and `PR #92 <https://github.com/PyFilesystem/s3fs/pull/92>`_
(preserve_time); the contract suite reproduces those failures.
