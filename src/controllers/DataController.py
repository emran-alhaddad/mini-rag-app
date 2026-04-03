from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models.enums import ResponseSignals
import os
import re
class DataController(BaseController):
    def __init__(self):
        super().__init__() 
    
    def validate_uploaded_file(self,file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_MIME_TYPES:
            return False, ResponseSignals.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.file_scalar_multiplier:
            return False, ResponseSignals.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignals.FILE_VALIDATED_SUCCESS.value

    def generate_unique_file_path(self, original_file_name: str, project_id: str):

        project_directory = ProjectController().get_project_directory(project_id)
        clean_file_name = self.get_clean_file_name(original_file_name)
        new_file_path,random_key = self._create_unique_file_path(project_directory, clean_file_name)
        
        while os.path.exists(new_file_path):
            new_file_path,random_key = self._create_unique_file_path(project_directory, clean_file_name)
        
        return new_file_path,random_key

    def get_clean_file_name(self, original_file_name: str):
        clean_file_name = re.sub(r'[^a-zA-Z0-9_.]', '', original_file_name)
        return clean_file_name.lower()

    def _create_unique_file_path(self, project_directory: str, clean_file_name: str):
        random_key = self.generate_random_string(10).lower()
        new_file_path = os.path.join(project_directory, random_key + "_" + clean_file_name)
        return new_file_path,random_key + "_" + clean_file_name