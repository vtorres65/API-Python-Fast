# API REST: Interfaz de programación de Aplicaciones para compartir recursos

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

# Inicializa una variable donde tendra las caracteristicas de un API REST
app = FastAPI()

# Acá definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simular una base de datos
cursos_db = []


# CRUD: Read (Lectura) Get All: Leeremos todos los cursos que hay en la cursos_db
@app.get("/cursos/", response_model=list[Curso])
def obtener_cursos():
    return cursos_db


# CRUD: Crear (escribir) POST: agregaremos un nuevo recurso a nuestra base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # Usamos UUID para generar un ID único e irrepetible
    cursos_db.append(curso)
    return curso

# CRUD: Read (lectura) GET (individual): Leeremos el curso coincida con el ID que pida
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# CRUD Update (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el ID que mandamos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el indice exacto donde está el curso en nuestra lista (cursos_db)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD Delete (birrado o quita) DELETE Eliminamod un recurso que coincida con el ID que mandamos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
