import boto3
import json
import hashlib
from datetime import datetime, timedelta



def generate_s3_key(user_id, file_name):

    return hashlib.sha224(user_id.encode()+ file_name.encode()).hexdigest()

def store_s3(request, key, user_id, data):
        ##TODO : put user_id, file_name
        s3 = boto3.client('s3',
            aws_access_key_id=request.app.config.AWS_ACCESS_KEY,
            aws_secret_access_key=request.app.config.AWS_SECRET_KEY, config= boto3.session.Config(signature_version='s3v4'), region_name="ap-south-1")

    

        s3.put_object(Bucket= request.app.config.BUCKET_NAME,
                                    Key=key,
                                   Body= json.dumps(data),
                                   Metadata={'user_id': user_id})

        s3.put_object_acl(Bucket=request.app.config.BUCKET_NAME, Key=key, ACL="public-read")
        #key.set_metadata('Content-Type', 'image/jpeg')


        # s3.put_object_tagging(Bucket=request.app.config.BUCKET_NAME, Key=key,\
        #             Tagging=request.app.config.S3_OBJECT_TAGS)

        expires = datetime.utcnow() + timedelta(days=(25 * 365))

        #url = s3.generate_presigned_url('get_object', Params = {'Bucket': request.app.config.BUCKET_NAME, 'Key': key}, ExpiresIn =expires.strftime("%s"))
        return "https://s3.ap-south-1.amazonaws.com/personal-demo-bucket/{}".format(key)
    


