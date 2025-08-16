import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body
from dotenv import load_dotenv
load_dotenv()
from processor.root_processor import RootProcessor
app = FastAPI()

UPLOAD_DIR = os.path.join(os.getenv("KB_BASE_PATH"), "raw")
FILE_STORAGE_PATH = UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)



def get_file_list() -> list[dict]:
    """获取文件列表的公共方法"""
    try:
        # 检查文件夹是否存在
        if not os.path.exists(FILE_STORAGE_PATH):
            raise FileNotFoundError(f"Directory {FILE_STORAGE_PATH} not found")
            
        # 遍历文件夹获取文件列表
        files = []
        for filename in os.listdir(FILE_STORAGE_PATH):
            file_path = os.path.join(FILE_STORAGE_PATH, filename)
            # 只返回文件，排除子目录
            if os.path.isfile(file_path):
                files.append(f"raw/{filename}")
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-files", response_model=list[str])
def list_files():
    """获取文件列表接口"""
    try:
        return get_file_list()
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...),
    file_name: str = Form(...),
    chunk_number: int = Form(...),
    total_chunks: int = Form(...)
):
    # 将分块保存到临时目录，避免与最终文件路径冲突
    temp_dir = os.path.join(UPLOAD_DIR, "temp", file_name)
    os.makedirs(temp_dir, exist_ok=True)
    chunk_path = os.path.join(temp_dir, f"chunk_{chunk_number}")

    # 写入分块文件
    with open(chunk_path, "wb") as buffer:
        buffer.write(await file.read())

    # 检查是否为最后一个分块
    if chunk_number == total_chunks:
        output_path = os.path.join(UPLOAD_DIR, file_name)
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 清理已存在的文件或目录
        if os.path.exists(output_path):
            if os.path.isdir(output_path):
                shutil.rmtree(output_path)
            else:
                os.remove(output_path)
        
        # 合并分块
        with open(output_path, "wb") as outfile:
            for i in range(1, total_chunks + 1):
                chunk_file = os.path.join(temp_dir, f"chunk_{i}")
                with open(chunk_file, "rb") as infile:
                    outfile.write(infile.read())
                os.remove(chunk_file)  # 删除分块文件
        
        # 删除临时目录
        shutil.rmtree(temp_dir)
        return {"message": f"File {file_name} uploaded successfully", "path": f"raw/{file_name}"}

    return {"message": f"Chunk {chunk_number} of {file_name} uploaded successfully", "path": f"raw/{file_name}"}



@app.post("/submit")
async def create_task(
    task_id: str = Body(..., description="task id such as uuid"),
    raw_path: str =  Body(..., description="raw path"),
    introduction: str = Body(..., description="introduction of TV anchor")
):
    query = {
        "task_id": task_id,
        "raw_video": raw_path,
        "introduction": introduction
    }
    root_prc = RootProcessor()
    result = await root_prc.run(query=query)
    return result
    