import json
import os.path
from abc import ABC, abstractmethod

import boto3
from botocore.exceptions import ClientError
from flask import current_app


class StorageProvider(ABC):
    """
    Abstract base class for all file storage providers.
    """

    @abstractmethod
    def create_bin(self, bin_name):
        """
        Create the directory/bucket etc in the file system. Each bin should
        be separated by tenant
        :param bin_name: Name of the bin that you are creating for the tenant
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def provision(self, **kwargs):
        """
        Provision the environment.
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def save_file(self, file_name, user, file_key, content_type):
        """
        Write the file to the correct tenant bucket.
        :param content_type:
        :param file_key:
        :param file_name:
        :param user:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_file(self, user, filename):
        """
        Return the file from the tenant storage
        :param user:
        :param filename:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_file_redirect(self, user, filename):
        """
        Return the redirect to the file resource
        :param user:
        :param filename:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def list_files(self, user):
        """
        List the files in the bucket
        :param user:
        :return:
        """
        raise NotImplementedError


class S3StorageProvider(StorageProvider):

    def list_files(self, user):
        bucket_name = f"tenant-{user.tenant_id}"
        bucket = self.client.Bucket(bucket_name)
        return bucket.objects

    def __init__(self):
        self.client = self._s3_client()

    @staticmethod
    def _s3_client():
        session = boto3.session.Session(profile_name=current_app.config.get("BOTO_PROFILE"))
        endpoint_override = current_app.config.get("BOTO_ENDPOINT")
        region = current_app.config.get("DEFAULT_REGION")
        if endpoint_override:
            client = session.client("s3", endpoint_url=endpoint_override, region_name=region)
        else:
            client = session.client("s3", region_name=region)
        return client

    def create_bin(self, bin_name):
        s3_bucket_create = self.client.create_bucket(Bucket=bin_name)
        return s3_bucket_create

    def s3_version_bucket_files(self, bucket_name):
        client = self._s3_client()
        version_bucket_response = client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={"Status": "Enabled"}
        )

    def s3_create_bucket_policy(self, bucket_name):
        resource = f"arn:aws:s3:::{bucket_name}/*"
        s3_bucket_policy = {"Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Sid": "AddPerm",
                                    "Effect": "Allow",
                                    "Principal": "*",
                                    "Action": "s3:*",
                                    "Resource": resource,
                                }
                            ]}
        policy = json.dumps(s3_bucket_policy)
        s3_bucket_policy_resp = self._s3_client().put_bucket_policy(Bucket=bucket_name, Policy=policy)
        return s3_bucket_policy_resp

    def provision(self, tenant, **kwargs):
        """
        Create an S3 bucket with the correct configuration for a tenant
        :param tenant: The ID of the tenant
        :param kwargs: Provider specific arguments that may be needed
        :return:
        """
        bucket_name = f"tenant-{tenant}"
        self.create_bin(bucket_name)
        current_app.logger.info("created %s", bucket_name)
        self.s3_create_bucket_policy(bucket_name)
        self.s3_version_bucket_files(bucket_name)

    def save_file(self, file_name, user, object_name=None):
        bucket_name = f"tenant-{user.tenant_id}"

        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            current_app.logger.info("Uploading %s to %s from %s", file_name, bucket_name, object_name)
            self.client.upload_file(file_name, bucket_name, object_name)
        except ClientError as e:
            current_app.logger.error(e)
            return ""
        return f"{bucket_name}"

    def fetch_file(self, user, filename):
        bucket_name = f"tenant-{user.tenant_id}"
        return self.fetch_file_by_bucket(bucket_name, filename)

    def fetch_file_by_bucket(self, bucket_name, filename):
        return self.client.download_file(bucket_name, filename,
                                         os.path.join(current_app.config["TEMP_FILES"], filename))

    def fetch_file_redirect(self, user, filename):
        bucket_name = f"tenant-{user.tenant_id}"
        return self._fetch_file_by_bucket_redirect(bucket_name, filename)

    def _fetch_file_by_bucket_redirect(self, bucket_name, filename):
        return self.client.generate_presigned_url("get_object", Params={"Bucket": bucket_name, "Key": filename},
                                                  ExpiresIn=100)

    def list_buckets(self):
        buckets_response = self.client.list_buckets()

        # check buckets list returned successfully
        if buckets_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return buckets_response['Buckets']
