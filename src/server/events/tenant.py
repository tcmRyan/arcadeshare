from flask import current_app
from ..signals import tenant_provisioned
from ..auth import Tenant
from ..utils.storage import S3StorageProvider


def provision_s3_bucket(tenant: Tenant):
    storage = S3StorageProvider()
    storage.provision(tenant.id)
    current_app.logger.info("Bucket PROVISIONED %s", tenant.id)


tenant_provisioned.connect(provision_s3_bucket)
