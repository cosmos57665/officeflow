from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.services import ask_service, docs_service, inbox_service, minutes_service


client = TestClient(app)


def test_demo_endpoints_avoid_llm_and_transcribe():
    with patch.object(minutes_service.transcribe, "transcribe") as transcribe_audio, \
            patch.object(minutes_service.llm, "ask_claude_json_with_provider") as minutes_ai, \
            patch.object(inbox_service.llm, "ask_claude_json_with_provider") as inbox_ai, \
            patch.object(docs_service.llm, "ask_claude_json_with_provider") as docs_ai:
        minutes = client.post("/api/minutes", data={"demo": "true"})
        inbox = client.post("/api/inbox", json={"text": "", "demo": True})
        docs = client.post("/api/docs", data={"demo": "true", "doc_type": "Merit Certificate"})
        ask = client.post(
            "/api/ask/question",
            json={"question": "What is the deadline for reimbursement claims?", "demo": True},
        )

    assert minutes.status_code == 200
    assert inbox.status_code == 200
    assert docs.status_code == 200
    assert ask.status_code == 200
    transcribe_audio.assert_not_called()
    minutes_ai.assert_not_called()
    inbox_ai.assert_not_called()
    docs_ai.assert_not_called()
    assert client.get(f"/api/files/{minutes.json()['docx_file_id']}").status_code == 200
    assert client.get(f"/api/files/{docs.json()['zip_file_id']}").status_code == 200


def test_inbox_empty_live_input_is_friendly_error():
    response = client.post("/api/inbox", json={"text": " ", "demo": False})

    assert response.status_code == 400
    assert response.json()["error"] == "Please paste some emails first."


def test_minutes_rejects_wrong_file_type():
    response = client.post(
        "/api/minutes",
        data={"demo": "false"},
        files={"audio": ("notes.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400
    assert "audio file" in response.json()["error"]


def test_minutes_normalizes_ai_shapes_without_crashing_renderer():
    dirty = {
        "title": "Quick Meeting",
        "date": "Today",
        "attendees": "Asha",
        "summary": "One short summary.",
        "decisions": None,
        "action_items": [{"task": "Send note"}],
    }
    with patch.object(minutes_service, "_generate", return_value=(dirty, "groq")), patch.object(
        minutes_service, "SAMPLE_AUDIO"
    ) as sample:
        sample.exists.return_value = True
        response = client.post(
            "/api/minutes",
            data={"demo": "false", "use_sample": "true"},
        )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["attendees"] == ["Asha"]
    assert data["summary"] == ["One short summary."]
    assert data["decisions"] == ["No decisions recorded."]
    assert data["action_items"][0]["owner"] == "Not specified"


def test_docs_rejects_missing_columns():
    response = client.post(
        "/api/docs",
        data={"demo": "false", "doc_type": "Merit Certificate"},
        files={"csv": ("students.csv", b"name\nAsha\n", "text/csv")},
    )

    assert response.status_code == 400
    assert "missing required column" in response.json()["error"]


def test_ask_rejects_question_without_pdf_when_live():
    response = client.post(
        "/api/ask/question",
        json={"question": "What is the rule?", "demo": False},
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Please upload a PDF first."


def test_upload_size_limit_is_friendly():
    response = client.post(
        "/api/docs",
        data={"demo": "false", "doc_type": "Merit Certificate"},
        files={"csv": ("students.csv", b"x" * (2 * 1024 * 1024 + 1), "text/csv")},
    )

    assert response.status_code == 413
    assert "too large" in response.json()["error"]
