from typing import List

try:
    import requests
except Exception:  # pragma: no cover
    requests = None

try:
    from transformers import pipeline as hf_pipeline
except Exception:  # pragma: no cover
    hf_pipeline = None


class LocalLLM:
    def __init__(self, backend: str, model_name: str):
        self.backend = backend
        self.model_name = model_name
        self._hf_pipe = None

        if self.backend == "hf" and hf_pipeline is not None:
            try:
                self._hf_pipe = hf_pipeline("text-generation", model=self.model_name)
            except Exception:
                self._hf_pipe = None

    def generate(self, prompt: str) -> str:
        if self.backend == "ollama" and requests is not None:
            try:
                resp = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": self.model_name, "prompt": prompt, "stream": False},
                    timeout=120,
                )
                resp.raise_for_status()
                return resp.json().get("response", "")
            except Exception:
                pass

        if self.backend == "hf" and self._hf_pipe is not None:
            try:
                out = self._hf_pipe(prompt, max_new_tokens=256, do_sample=False)
                if out and isinstance(out, list):
                    text = out[0].get("generated_text", "")
                    return text[len(prompt):].strip() if text.startswith(prompt) else text
            except Exception:
                pass

        return f"[Fallback {self.backend}:{self.model_name}]\nInsufficient local runtime. Echo prompt:\n{prompt[:900]}"


def build_cited_answer(question: str, contexts: List[dict], llm: LocalLLM) -> str:
    context_block = "\n\n".join(
        [f"[{i+1}] {c['text'][:500]}" for i, c in enumerate(contexts)]
    )
    prompt = (
        "Answer using only provided context. Do not invent facts. "
        "Return concise bullets and include citations like [1], [2] after each claim. "
        "If unsupported, respond exactly: Insufficient evidence.\n\n"
        f"Question: {question}\n\nContext:\n{context_block}"
    )
    answer = llm.generate(prompt)
    if contexts:
        citations = [f"[{i+1}]" for i in range(min(len(contexts), 3))]
        if not any(c in answer for c in citations):
            answer = f"{answer}\n\nSources: {' '.join(citations)}"
    return answer
