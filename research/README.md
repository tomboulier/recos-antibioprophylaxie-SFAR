# ⚠️ Research files have moved

The benchmark framework for S-019 has been **moved to a separate repository**:

→ **[antibioprophylaxie-LLM-benchmark](../../../antibioprophylaxie-LLM-benchmark)**

## Why?

To maintain clear separation of concerns:
- **Main app** (`recos-antibioprophylaxie-SFAR`): Production webapp + API
- **Research project** (`antibioprophylaxie-LLM-benchmark`): Scientific evaluation framework

## Content moved

- `research/benchmark.md` → `antibioprophylaxie-LLM-benchmark/research/`
- `research/benchmark.json` → `antibioprophylaxie-LLM-benchmark/research/`
- `scripts/run_benchmark.py` → `antibioprophylaxie-LLM-benchmark/scripts/`
- `scripts/benchmark_md_to_json.py` → `antibioprophylaxie-LLM-benchmark/scripts/`

## Legacy files (to be cleaned up)

These files in `research/` will be removed in a future cleanup. 
For now they remain for backward compatibility.
