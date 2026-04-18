from pydantic import BaseModel, Field


class DiaryCreateRequest(BaseModel):
    destination_name: str
    title: str
    content: str
    cover_image_url: str | None = None
    media_urls: list[str] = Field(default_factory=list)


class DiarySearchRequest(BaseModel):
    query: str


class DiaryCompressionRequest(BaseModel):
    content: str


class DiaryOut(BaseModel):
    id: int
    title: str
    destination_name: str
    content: str
    views: int
    rating: float
    media_urls: list[str] = Field(default_factory=list)


class DiaryListResponse(BaseModel):
    items: list[dict] = Field(default_factory=list)


class DiarySearchResponse(BaseModel):
    query: str
    items: list[dict] = Field(default_factory=list)
