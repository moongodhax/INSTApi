from ..Utils import INSTApi_Utils

from PIL import Image
import re

class INSTApi_Publish(INSTApi_Utils):
    def publish_photo(me, filename):
        im = Image.open(filename)
        width, height = im.size
        
        photo_data = open(filename, 'rb').read()
        upload_id = me.upload_photo(photo_data)
        
        configure_options = {
            'upload_id': upload_id,
            'width': width,
            'height': height,
        }
        
        return me.configure(configure_options)
    
    def publish_story(me, filename):
        im = Image.open(filename)
        width, height = im.size
        
        photo_data = open(filename, 'rb').read()
        upload_id = me.upload_photo(photo_data)
        
        configure_options = {
            'upload_id': upload_id,
            'width': width,
            'height': height,
        }
        
        return me.configure_to_story(configure_options)