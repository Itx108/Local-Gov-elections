# Johannesburg election analytics

Prediction date: **4 November 2026**. Information cutoff: **5 October 2026**.

Extract the complete project ZIP. Keep the notebook, model.py and data folder together.

## Install and run

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open Johannesburg_2026_Election_Analytics.ipynb and run its cells in order. An installed Jupyter app can open it directly; select a kernel with these dependencies installed.

Dashboard:
```bash
python -m streamlit run app.py
```

Checks:
```bash
python -m unittest discover -s tests -v
```

## Reproduce the evidence

Original IEC PDFs, extracted text, official geometry and source metadata are already bundled. Reconciliation and ward-data building can run offline:

```bash
python reconcile_official_results.py
python build_verified_wards.py
python model.py
```

To retrieve fresh official files on a computer with source-site access:

```bash
python collect_official_sources.py
python collect_boundaries.py
```

Review publication/vintage metadata before replacing the examination snapshot. Never import later election outcomes into this forecast. The 2026 boundary DATE is an effective election date, not an observation date. A fresh retrieval after the cutoff requires a separate availability audit.

## Contents

- Notebook and CELL_BY_CELL_GUIDE.md: 24 sequential analysis cells.
- app.py and model.py: dashboard and shared models.
- ASSESSMENT_REPORT.md: four outputs, evidence and limitations.
- data/sources.csv: direct official dataset URLs.
- data/raw/: archived original PDFs, GeoJSON and metadata.
- data/verification_audit.csv: all 30 municipal PR cells reconcile.
- data/verified_ward_crosswalk.csv: admitted histories for 2026 wards 21, 23 and 87.
- outputs/: forecasts, errors, sensitivity and geometry diagnostics.

## Scope

Persistence wins the small historical comparison; Ridge remains a fitted ML candidate. Metro support is conditional on the historical party slate. MK and RISE Mzansi are covered through explicit provincial-context scenarios, not unsupported municipal-only zero estimates. Ward histories are limited to geometrically comparable years. Earlier metro boundaries have small measured differences and their backtests remain provisional. Turnout uses an estimated registered-plus-MEC7 denominator. Coalition output is vote arithmetic, not governing-party prediction.
