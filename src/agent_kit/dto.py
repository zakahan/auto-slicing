from typing import Optional
from pydantic import BaseModel, Field

# "author": event.author,
# "response": event.content.parts[0].text,


class TextContent(BaseModel):
    text: str = Field(description="text content")


class Metadata(BaseModel):
    response_id: Optional[str] = Field(description="response id")
    session_id: Optional[str] = Field(description="session id")


class RunResponse(BaseModel):
    author: str = Field(description="author of the response")
    content: TextContent = Field(description="content of the response")
    metadata: Metadata = Field(description="metadata of the response")


def create_text_response(
    author: str,
    text: str,
    response_id: Optional[str] = None,
    session_id: Optional[str] = None,
):
    return RunResponse(
        author=author,
        content=TextContent(text=text),
        metadata=Metadata(
            response_id=response_id,
            session_id=session_id,
        ),
    )
