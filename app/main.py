from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.schemas import ReviewRequest, ReviewResponse
from app.model import Predictor

from app.database import OracleDBManager

db_manager = OracleDBManager()

predictor = Predictor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager.init_database()
    
    yield

app = FastAPI(
    title="Amazon Beauty Rating Predictor API",
    description="API для предсказания рейтинга товара по тексту отзыва",
    lifespan=lifespan
)

def get_db_manager() -> OracleDBManager:
    return db_manager

@app.post("/predict", response_model=ReviewResponse)
def predict_rating(request: ReviewRequest, db: OracleDBManager = Depends(get_db_manager)):
    input_dict = request.model_dump() 
    rating = predictor.predict(input_dict)

    db.save_prediction(input_dict['full_text'], rating)

    return ReviewResponse(predicted_rating=rating)