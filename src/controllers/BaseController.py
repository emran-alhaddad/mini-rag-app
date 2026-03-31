from helpers import get_settings
import os
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.file_scalar_multiplier = 1024 * 1024 # 1MB
        self.project_directory = os.path.join(os.path.dirname(__file__), "..", self.app_settings.PROJECT_DIRECTORY)