import os

from server.utils.storage import S3StorageProvider


def test_s3_list_files(app):
    pass


def test_s3_provision(app):
    sp = S3StorageProvider()
    sp.provision(1)
    assert len(sp.list_buckets()) == 1


def test_s3_fetch_file_redirect(app):
    pass


def test_s3_save_and_fetch_file(app, test_user, cleanup_tmp_files):
    sp = S3StorageProvider()
    sp.provision(1)

    with open("testfile.uf2", "a") as file:
        file.write("Test File")
    sp.save_file("testfile.uf2", test_user)
    os.remove("testfile.uf2")
    sp.fetch_file(test_user, "testfile.uf2")
    with open(os.path.join(app.config["TEMP_FILES"], "testfile.uf2"), "r") as file:
        line = file.readline()
        assert line == "Test File"
