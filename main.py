"""
Enterprise Multi-Agent HR Assistant — FastAPI entry point.

Architecture:
  Employee Request -> FastAPI -> RouterAgent
    -> HR Policy Agent / Benefits Agent / Payroll Agent / Procurement Agent
    -> Legal Agent / Compliance Agent / Facilities Agent
    -> RAG retrieval + workflow actions

Model backend: Google Gemini via Vertex AI
Agent framework: Google ADK
RAG backend: configurable (Agent Search, RAG Engine, Vector Search, or stub)
Observability: Cloud Logging + Cloud Trace
Security: IAM service account + Secret Manager + guardrails
"""

import asyncio
import logging
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from opentelemetry import trace

from config import APP_NAME, API_HOST, API_PORT
from agents import router_agent
from observability import setup_telemetry, trace_agent_call
from security import get_credentials, initialise_vertex

logger = logging.getLogger(__name__)


class AskRequest(BaseModel):
    query: str
    user_id: str | None = None
    session_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    user_id: str
    session_id: str


async def run_agent(
    query: str,
    tracer: trace.Tracer,
    user_id: str | None = None,
    session_id: str | None = None,
) -> str:
    """Run the Router Agent and return the final response text."""
    user_id = user_id or f"user-{uuid.uuid4().hex[:8]}"
    session_id = session_id or f"session-{uuid.uuid4().hex[:8]}"

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    runner = Runner(
        agent=router_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    with trace_agent_call(tracer, "RouterAgent", user_id, session_id):
        message = types.Content(
            role="user",
            parts=[types.Part(text=query)],
        )
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message,
        ):
            if event.is_final_response():
                return event.content.parts[0].text

    raise RuntimeError(
        f"Agent returned no final response for query={query!r} "
        f"user_id={user_id} session_id={session_id}"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", APP_NAME)
    get_credentials()
    initialise_vertex()
    app.state.tracer = setup_telemetry()
    yield
    logger.info("Shutting down %s", APP_NAME)


app = FastAPI(
    title="Enterprise HR Assistant",
    description="Google ADK + Gemini Enterprise Agent Platform HR assistant",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": APP_NAME}


@app.post("/ask", response_model=AskResponse)
async def ask(body: AskRequest, req: Request) -> AskResponse:
    if not body.query or not body.query.strip():
        raise HTTPException(status_code=400, detail="query is required")
    try:
        tracer = req.app.state.tracer
        answer = await run_agent(body.query, tracer, body.user_id, body.session_id)
        return AskResponse(
            answer=answer,
            user_id=body.user_id or f"user-{uuid.uuid4().hex[:8]}",
            session_id=body.session_id or f"session-{uuid.uuid4().hex[:8]}",
        )
    except Exception as e:
        logger.exception("ask failed query=%s", body.query)
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=False)
