import gradio as gr


def launch_gradio(ask_fn):
    def _infer(question: str):
        out = ask_fn(question)
        status = out.get("status", "unknown")
        sources = []
        for i, c in enumerate(out.get("contexts", [])[:5]):
            md = c.get("metadata", {})
            src = md.get("source", md.get("doc_id", "unknown"))
            snippet = c.get("text", "")[:220].replace("\n", " ")
            sources.append(f"[{i+1}] {src} :: {snippet}")
        source_text = "\n".join(sources) if sources else "No sources (status indicates no grounded retrieval)."
        return out.get("answer", ""), source_text, status

    demo = gr.Interface(
        fn=_infer,
        inputs=gr.Textbox(label="Ask your local knowledge base", lines=3, placeholder="Ask for policy constraints, evidence-backed summary, or cited requirements..."),
        outputs=[
            gr.Textbox(label="Answer", lines=10),
            gr.Textbox(label="Retrieved Sources", lines=10),
            gr.Textbox(label="Status", lines=1),
        ],
        title="Proferio Demo",
        description="Grounded local RAG with citation-oriented answers and visible retrieval traces.",
        examples=[
            ["What safeguards are required for traceable AI outputs?"],
            ["Summarize governance requirements and cite sources."],
            ["What should be logged for auditability?"],
        ],
    )
    return demo
