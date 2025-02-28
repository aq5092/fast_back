from fastapi import FastAPI, Depends, HTTPException, APIRouter,File, UploadFile, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import os
from database import get_db, SessionLocal # SQLAlchemy sessiyasini olish uchun yordamchi
from pydantics import UserBase, UserCreate, UserResponse,TaskBase,TaskCreate, TaskResponse, AsosPdfBase
from typing import List, Optional
import crud
from sqlalchems import  AsosPdf
from pathlib import Path

router = APIRouter()






@router.post("/userc/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.get("/users/", response_model=List[UserResponse])
def get_all_users(db:Session= Depends(get_db)):
    users = crud.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users

@router.get("/pdfs/", response_model=List[AsosPdfBase])
def get_all_pdfs(db: Session = Depends(get_db)):
    pdfs = crud.get_pdfs(db)
    if not pdfs:
        raise HTTPException(status_code=404, detail="PDF files not found")
    return pdfs

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/useru/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/userd/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": f"User with ID {user_id} deleted"}


BASE_DIR = "storage"
os.makedirs(BASE_DIR, exist_ok=True)
# PDF fayllarni saqlash uchun joy
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_asos/")
async def upload_asos(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db = SessionLocal()
    pdf_file = AsosPdf(filename=file.filename)
    db.add(pdf_file)
    db.commit()
    db.close()
    return {"filename": file.filename, "url": f"/pdf/{file.filename}"}  # Fayl URL manzili
    

@router.post("/taskc/{user_id}", response_model=TaskResponse)
def create_task_endpoint(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_task(db, task, user_id)


@router.get("/tasks/", response_model=List[TaskResponse])
def get_all_tasks(db: Session= Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks

@router.get("/task/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int,db:Session=Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.get_task_by_id(db, task_id)

@router.get("/users/{user_id}/tasks/", response_model=List[TaskResponse])
def get_user_tasks_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_tasks_by_user(db, user_id)

@router.put("/tasku/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/taskd/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": f"Task with ID {task_id} deleted"}


# 📁 Papka yaratish
@router.post("/create-folder/")
def create_folder(parent_path: str, folder_name: str):
    folder_path = os.path.join(BASE_DIR, parent_path, folder_name)
    if os.path.exists(folder_path):
        raise HTTPException(status_code=400, detail="Bunday papka allaqachon mavjud")
    os.makedirs(folder_path)
    return {"message": f"Papka '{folder_name}' yaratildi"}

# 📂 Papkalar va fayllar daraxtini olish
def get_folder_tree(path: str):
    tree = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            tree.append({
                "name": item,
                "path": os.path.relpath(full_path, BASE_DIR),
                "type": "folder",
                "children": get_folder_tree(full_path)
            })
        else:
            tree.append({
                "name": item,
                "path": os.path.relpath(full_path, BASE_DIR),
                "type": "file"
            })
    return tree

@router.get("/list-folders/")
def list_folders():
    return {"tree": get_folder_tree(BASE_DIR)}


# 📤 Fayl yuklash
@router.post("/upload-file/")
def upload_file(folder_path: str, file: UploadFile = File(...)):
    save_path = os.path.join(BASE_DIR, folder_path, file.filename)
    
    if not os.path.exists(os.path.join(BASE_DIR, folder_path)):
        raise HTTPException(status_code=404, detail="Papka topilmadi")
    
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    db = SessionLocal()
    pdf_file = AsosPdf(filename=file.filename)
    db.add(pdf_file)
    db.commit()
    db.close()
    
    return {"message": f"Fayl '{file.filename}' '{folder_path}' papkasiga yuklandi"}

# 🗑️ Fayl yoki papkani o‘chirish
@router.delete("/delete-item/")
def delete_item(item_path: str, filename: str, db: Session = Depends(get_db)):
    full_path = os.path.join(BASE_DIR, item_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Element topilmadi")
    
    if os.path.isdir(full_path):
        shutil.rmtree(full_path)
    else:
        os.remove(full_path)
    
    deleted_pdf = crud.delete_pdf(db, filename)
    if not deleted_pdf:
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    return {"message": f"'{item_path}' o‘chirildi"}

# 📥 Faylni yuklab olish
from fastapi.responses import FileResponse

@router.get("/download-file/")
def download_file(file_path: str):
    full_path = os.path.join(BASE_DIR, file_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")
    return FileResponse(full_path, media_type="application/octet-stream", filename=os.path.basename(full_path))




# PDF faylni o‘qish
@router.get("/{file_path:path}")  # `/d/` dan keyingi butun yo‘lni oladi
def get_pdf(file_path: str):
    # Agar foydalanuvchi `\` bilan jo‘natsa, uni `/` ga almashtiramiz
    normalized_path = file_path.replace("\\", "/")  

    file_path = os.path.join(BASE_DIR, normalized_path)
    
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf")
    
    return {"error": "File not found"}


# 🔍 Qidirish funksiyasi
@router.get("/search/")
def search_files(query: str):
    result = []

    for root, dirs, files in os.walk(BASE_DIR):
        for name in files + dirs:
            if query.lower() in name.lower():
                full_path = os.path.relpath(os.path.join(root, name), BASE_DIR)
                result.append({"name": name, "path": full_path})

    return {"results": result}


