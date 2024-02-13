from fastapi import FastAPI, HTTPException, Query, Depends
from model import twoWords, twoWordsName, threeWords, threeWordsName, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_file = "word_database.db"
engine = create_engine(f"sqlite:///{db_file}", echo=True)
# Create the table if it does not exist
Base.metadata.create_all(engine)

# Dependency to get the SQLAlchemy Session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event("startup")
async def startup():
    global Session
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event("shutdown")
async def shutdown():
    global Session
    Session.close_all()

def get_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

table_mapping = {
    1: twoWords,
    2: twoWordsName,
    3: threeWords,
    4: threeWordsName,
}

@app.get("/word")
def read_word(
    word: str = Query(..., title="Search Word", description="Enter the word to search"),
    version: int = Query(..., title="Version", description="Version"),
    session = Depends(get_session)
):

    table = table_mapping.get(version)
    if not table:
        raise HTTPException(status_code=400, detail="Invalid version")

    result = session.query(table).filter(text("word = :word")).params(word=word).first()
    if not result:
        return {"word": word, 'ok': False}

    end_word = word.split(' ')[-1]
    result = session.query(table).filter(text("word LIKE :end_word")).params(end_word=end_word + ' %').order_by(func.random()).first()
    if result:
        return {"word": result.word, 'ok': True}
    else:
        return {"word": None, 'ok': True}

@app.get("/random_word")
def get_random_word(
    version: int = Query(..., title="Version", description="Version"),
    session = Depends(get_session)
):

    table = table_mapping.get(version)
    if not table:
        raise HTTPException(status_code=400, detail="Invalid version")

    # Get a random word from the table
    random_word = session.query(table).order_by(func.random()).first()
    
    if random_word:
        return {"word": random_word.word, 'ok': True}
    else:
        return {"word": None, 'ok': False}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
