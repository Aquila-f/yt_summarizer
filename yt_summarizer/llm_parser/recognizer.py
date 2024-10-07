from yt_summarizer.llm_parser.utils.llm import get_openai_model
from yt_summarizer.llm_parser.utils.prompt import get_extract_key_prompt, get_prompt
from yt_summarizer.models.finance_summary import FinanceSummary


def key_extract(subtitle_txt: str) -> FinanceSummary:
    llm = get_openai_model()
    structured_llm = llm.with_structured_output(FinanceSummary)
    prompt = get_extract_key_prompt(subtitle_txt)
    result = structured_llm.invoke(prompt)
    print(result)
    return result
