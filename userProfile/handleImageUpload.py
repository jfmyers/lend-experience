from userProfile.models import Profile
from lxp import settings
import os
import boto
from boto.s3.key import Key

class ImageToS3:
    def __init__(self, full_temp_file_name, s3_file_name):
        self.full_temp_file_name = full_temp_file_name
        self.s3_file_name = s3_file_name
        self.upload_result = self.send_image_to_s3()
        
    def send_image_to_s3(self):
      try:
        bucket_name = settings.BUCKET_NAME      
        # Connect to the AWS S3 bucket
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(bucket_name)              
        # Create a key to keep track of our file in the storage 
        k = Key(bucket)
        k.key = self.s3_file_name
        k.set_contents_from_filename(self.full_temp_file_name)
        # Make it public so it can be accessed publicly,
        # Using a URL like http://s3.amazonaws.com/bucket_name/key
        k.make_public()
        # Remove the file from the web server's temp directory
        os.remove(self.full_temp_file_name)
        return True
      except:
        return False
    

def image_upload(temp_file_name, s3_file_name, user_id):   
    # Get the fill path of the uploaded file so we can send it to S3.
    full_temp_file_name = os.path.join(settings.BASE_DIR, "temp", temp_file_name)
    
    # Upload the image via ImageToS3.
    upload = ImageToS3(full_temp_file_name, s3_file_name).upload_result
    
    # Did it work?
    if upload is True:
        p = Profile.objects.get(pk=user_id)
        p.pic = s3_file_name
        p.save(update_fields=['pic'])
        return True
    else:
        return False