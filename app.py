from fastapi import FastAPI, HTTPException, Query, Depends
from model import twoWords, twoWordsName, threeWords, threeWordsName, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

app = FastAPI()

db_file = "word_database.db"
engine = create_engine(f"sqlite:///{db_file}", echo=True)
# Create the table if it does not exist
Base.metadata.create_all(engine)

# Dependency to get the SQLAlchemy Session
def get_session():
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

@app.get("/word/")
def read_word(
    word: str = Query(..., title="Search Word", description="Enter the word to search"),
    version: int = Query(..., title="Version", description="Version"),
    session = Depends(get_session)
):
    table_mapping = {
        1: twoWords,
        2: twoWordsName,
        3: threeWords,
        4: threeWordsName,
    }

    table = table_mapping.get(version)
    if not table:
        raise HTTPException(status_code=400, detail="Invalid version")

    result = session.query(table).filter(text("word = :word")).params(word=word).first()
    if not result:
        raise HTTPException(status_code=404, detail="Word not found1")

    end_word = word.split(' ')[-1]
    result = session.query(table).filter(text("word LIKE :end_word")).params(end_word=end_word + '%').all()
    if result:
        return {"result": [row.word for row in result]}
    else:
        raise HTTPException(status_code=404, detail="Word not found")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
