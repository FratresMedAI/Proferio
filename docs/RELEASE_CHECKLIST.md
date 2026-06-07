# Release Checklist

## Core Quality

- [x] `python scripts/smoke_test.py --backend fallback --no-persist-index` passes (Tier A)
- [x] `python scripts/run_benchmarks.py --backend fallback --no-persist-index` runs and outputs table
- [x] Out-of-scope query returns `status: out_of_scope`
- [x] In-domain query returns `status: grounded`
- [ ] `python scripts/smoke_test.py --backend ollama` passes on RunPod (Tier B)

## Demo Readiness

- [ ] `python scripts/launch_gradio.py --backend ollama` launches at `http://localhost:7860` on RunPod
- [x] UI shows `Answer`, `Retrieved Sources`, and `Status`
- [ ] At least 3 example prompts execute cleanly with Ollama on RunPod

## Documentation

- [x] README includes quick start and benchmark command
- [x] `docs/ARCHITECTURE.md` reflects current modules/status semantics
- [x] Banner image in README
- [x] `docs/ACCEPTANCE.md` and `docs/RUNPOD.md` added

## GitHub Polish

- [x] CI workflow passes on default branch (Tier A)
- [x] License and contributing docs present
- [x] Issue templates + PR template present

## Launch Pack

- [ ] Prepare a short demo clip (30–60 sec)
- [ ] Post on r/LocalLLaMA, r/MachineLearning, X
- [ ] Include benchmark table and citation screenshot in launch post
