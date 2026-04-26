from pydantic import BaseModel, Field

class ReviewRequest(BaseModel):
    full_text: str = Field(..., description="Полный текст отзыва")

class ReviewResponse(BaseModel):
    predicted_rating: int = Field(..., description="Предсказанный рейтинг от 1 до 5")