
from app.llm.prompt import SYSTEM_PROMPT, build_analysis_prompt

company = "Apple"

answer = """
Samsung offers better battery life than Apple.
However, Apple has a more polished operating system.
"""

prompt = build_analysis_prompt(company, answer)

print("SYSTEM PROMPT LOADED:")
print(bool(SYSTEM_PROMPT))

print("\nGENERATED INPUT PROMPT:")
print(prompt)
