from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"Hospital support request system-server"}
db = {
    1 : {"id":1,"title":"Hospital facility","description":"walls damaged",
     "category":"building maintenance","Status":"New"},
    2 : {"id":2,"title":"Medical equipment issue",
     "description":"Machine malfunctioning","category":"Hardware","status":"New"},
    3 : {"id":3,"title":"Hospital management issue","description":"incorrect patient information","category":"software","status":"New"}
}
#schemas
class RequestCreate(BaseModel):
    title:str
    description:str
    category:str
    status:str
    
class RequestResponse(BaseModel):
    id : int
#API
@app.get("/requests")
def request_read_by_all():
    return list(db.values())#tuples cannot be understood by pydantic so it is converted to list

@app.get("/requests/{id}")
def request_read_by_id(id:int):
    if id not in db:
        raise HTTPException(detail="request Not Found",Status_code=404)
    return db[id]

@app.post("/tickets",status_code=201,response_model=RequestResponse)
def request_create(request_payload : RequestCreate):
    new_id = max(db.keys(),default=0)+1
    db[new_id] = {"id": new_id,**request_payload.model_dump()}
    return db[new_id]

@app.put("/requests/{id}",response_model = RequestResponse)
def request_update(id:int,payload : RequestCreate):
    if id not in db:
        raise HTTPException(detail="Reques Not Found",status_code=404)
    db[id]={"id":id,**payload.model_dump()}
    return db[id]
@app.delete("/requests/{id}")
def request_delete(id : int):
    if id not in db:
        raise HTTPException(detail="Request Not Found",status_code=404)
    del db[id]
    return{"message":"Request Deleted Successfully"}
    