# Release Checklist

## Core Quality

- [ ] `python scripts/smoke_test.py` passes
- [ ] `python scripts/run_benchmarks.py` runs and outputs table
- [ ] Out-of-scope query returns `status: out_of_scope`
- [ ] In-domain query returns `status: grounded`

## Demo Readiness

- [ ] `python scripts/launch_gradio.py` launches at `http://localhost:7860`
- [ ] UI shows `Answer`, `Retrieved Sources`, and `Status`
- [ ] At least 3 example prompts execute cleanly

## Documentation

- [ ] README includes quick start and benchmark command
- [ ] `docs/ARCHITECTURE.md` reflects current modules/status semantics
- [ ] Add 1 screenshot or GIF to README before public launch

## GitHub Polish

- [ ] CI workflow passes on default branch
- [ ] License and contributing docs present
- [ ] Issue templates + PR template present

## Launch Pack

- [ ] Prepare a short demo clip (30–60 sec)
- [ ] Post on r/LocalLLaMA, r/MachineLearning, X
- [ ] Include benchmark table and citation screenshot in launch post
