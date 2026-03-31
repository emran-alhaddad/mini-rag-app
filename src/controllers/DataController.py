from controllers import BaseController
from fastapi import UploadFile
from models.enums import ResponseSignals
import os
class DataController(BaseController):
    def __init__(self):
        super().__init__() 
    
    def validate_uploaded_file(self,file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_MIME_TYPES:
            return False, ResponseSignals.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.file_scalar_multiplier:
            return False, ResponseSignals.FILE_SIZE_EXCEEDED.value
        return True, ResponseSignals.FILE_VALIDATED_SUCCESS.value