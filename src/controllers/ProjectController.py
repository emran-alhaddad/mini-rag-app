from controllers import BaseController
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
    
    def get_project_directory(self, project_id: str):
        project_directory = os.path.join(self.project_directory, project_id)
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)
        return project_directory