
from app.llm.prompt import SYSTEM_PROMPT, build_analysis_prompt


def test_system_prompt_is_loaded():
    assert isinstance(SYSTEM_PROMPT, str)
    assert SYSTEM_PROMPT.strip()


def test_analysis_prompt_includes_company():
    prompt = build_analysis_prompt(
        company="Apple",
        answer="Apple produces premium smartphones."
    )

    assert "Apple" in prompt


def test_analysis_prompt_includes_answer():
    answer = "Apple produces premium smartphones."

    prompt = build_analysis_prompt(
        company="Apple",
        answer=answer
    )

    assert answer in prompt


def test_analysis_prompt_is_not_empty():
    prompt = build_analysis_prompt(
        company="Apple",
        answer="Apple produces premium smartphones."
    )

    assert isinstance(prompt, str)
    assert prompt.strip()
