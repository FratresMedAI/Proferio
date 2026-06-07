# Contributing

## Setup

1. Install dependencies from `requirements.txt` or `environment.yml`.
2. Run notebooks from `notebooks/` in order.
3. Keep examples reproducible with local-first defaults.

## Notebook standards

- Keep each notebook runnable top-to-bottom.
- Use explicit configuration cells.
- Avoid hidden side effects between cells.
- Include a short validation section for outputs.

## Code standards

- Keep reusable logic in `src/proferio/`.
- Prefer typed functions and dataclasses/pydantic models.
- Keep modules backend-agnostic where possible.

## Pull requests

- Describe what changed and why.
- Add/update notebook sections that demonstrate behavior.
- Keep changes focused and easy to review.
- State the **target branch** (`main` or `defense`) in the PR description.

## Branch hygiene

- **`main`** — general Fratres X Med AI starter kit. No defense-specific corpus or eval artifacts.
- **`defense`** — defense knowledge-grounding overlay only. Merge `main` into `defense` regularly to pick up shared fixes.
- **Never merge `defense` → `main`** without explicit review — defense corpus and eval sets must not leak into the general starter.
- Synthetic defense documents must include the header `SYNTHETIC — FOR EVALUATION ONLY` on every file.
