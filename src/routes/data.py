from fastapi import APIRouter, UploadFile, Depends, HTTPException
from helpers import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models.enums import ResponseSignals
import os
import aiofiles
import logging
from .shemes import ProcessRequest

logger = logging.getLogger("uvicorn.error")

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

    project_path = ProjectController().get_project_directory(project_id)
    file_path, file_id = data_controller.generate_unique_file_path(file.filename, project_id)
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while content := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(content)
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"{ResponseSignals.FILE_UPLOAD_FAILED.value}: {e}")

    return {"message": ResponseSignals.FILE_UPLOAD_SUCCESS.value, "file_id": file_id}



@data_router.post("/process/{project_id}")
async def process_data(project_id: str, request: ProcessRequest):
   file_id = request.file_id
   chunk_size = request.chunk_size
   chunk_overlap = request.chunk_overlap
   do_reset = request.do_reset
   process_controller = ProcessController(project_id=project_id)
   file_content = process_controller.get_file_content(file_id)
   file_chunks = process_controller.process_file_content(file_content=file_content, file_id=file_id, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
   
   if file_chunks is None or len(file_chunks) == 0:
       raise HTTPException(status_code=400, detail=ResponseSignals.FILE_PROCESSING_FAILED.value)
   return {"message": ResponseSignals.FILE_PROCESSING_SUCCESS.value, "file_chunks": file_chunks} 
