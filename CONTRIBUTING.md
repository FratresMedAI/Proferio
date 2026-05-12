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
