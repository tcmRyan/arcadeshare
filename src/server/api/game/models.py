import os

from flask_login import current_user
from flask import current_app
from src.server import db
from src.server.signals import game_created, game_updated
from src.server.utils.storage import S3StorageProvider
from werkzeug.utils import secure_filename


class Game(db.Model):
    __bind_key__ = "__tenant__"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    bucket = db.Column(db.String)
    thumbnail = db.Column(db.String)
    version = db.Column(db.Integer, default=0)

    def upload_game(self, file, user):
        """
        Save the Flask file upload to temp storage, upload to cloud storage and then clean up temp file
        :param file: Flask File object that is the game file
        :param user: owner of the agame
        :return:
        """
        self.bucket = self._save_file(file, user)
        db.session.add(self)
        db.session.commit()

    def save_thumbnail(self, file, user):
        self.thumbnail = self._save_file(file, user, )
        db.session.add(self)
        db.session.commit()

    def _save_file(self, file, user):
        file.filename = secure_filename(file.filename)
        storage = S3StorageProvider()
        save_path = os.path.join(current_app.config["TEMP_FILES"], file.filename)
        bucket_path = f"{self.name}/{file.filename}"
        current_app.logger.info("saving file %s as %s to %s", save_path, user.username, bucket_path)
        storage.save_file(save_path, user, bucket_path)
        return bucket_path

    def download_game(self):
        """
        Download the game to local disk.
        :return:
        """
        storage = S3StorageProvider()
        return storage.fetch_file_by_bucket(self.bucket, self.name)

    def download_redirect(self, path):
        """
        Provide the redirect url to the AWS resource so that the user can download.
        :return:
        """
        storage = S3StorageProvider()
        return storage.fetch_file_redirect(current_user, path)

    def save(self, new=False):
        """
        Save the Game to the DB.  If this is a new game the `game_created` event will be sent. If the game exists, the
        `game_updated` event will be sent.
        :return:
        """
        if self.version:
            self.version = int(self.version) + 1
        else:
            self.version = 1
        db.session.add(self)
        db.session.commit()
        if new:
            current_app.logger.info("Create Game event: %s", self.name)
            game_created.send(self)
        else:
            current_app.logger.info("Update Game event: %s", self.name)
            game_updated.send(self)
