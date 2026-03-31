from fastapi import APIRouter, UploadFile, Depends, HTTPException
from helpers import get_settings, Settings
from controllers import DataController, ProjectController
from models.enums import ResponseSignals
import os
import aiofiles

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    data_controller = DataController()
    result, message = data_controller.validate_uploaded_file(file)
    if not result:
        raise HTTPException(status_code=400, detail=message)

    project_controller = ProjectController()
    project_directory = project_controller.get_project_directory(project_id)
    file_path = os.path.join(project_directory, file.filename)
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while content := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{ResponseSignals.FILE_UPLOAD_FAILED.value}: {e}")
        
    return {"message": ResponseSignals.FILE_UPLOAD_SUCCESS.value}