from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title='Johannesburg 2026 Election Analytics', page_icon='🗳️', layout='wide')
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'outputs'

st.title('Johannesburg 2026 Local Government Election Analytics')
st.caption('Information cutoff: 5 October 2026 · Election: 4 November 2026 · Analytical forecast, not political opinion')

def read_csv(name):
    p = OUT / name
    return pd.read_csv(p) if p.exists() else None

metro = read_csv('metro_projection.csv')
wards = read_csv('ward_projection.csv')
leaders = read_csv('ward_leaders.csv')
answers = read_csv('assessment_answers.csv')
evidence = read_csv('evidence_register.csv')
unc = read_csv('forecast_uncertainty_diagnostic.csv')
ward_sel = read_csv('ward_selection_evidence.csv')
coal = read_csv('coalition_arithmetic.csv')
rolling = read_csv('rolling_validation.csv')

if metro is None:
    st.error('Dashboard data has not been exported yet.')
    st.code(f'Expected file: {OUT / "metro_projection.csv"}')
    st.markdown('Run **Johannesburg_2026_Election_Analytics_FINAL_FIXED.ipynb** from top to bottom, then refresh this page.')
    st.stop()

named = metro[metro.party.ne('OTHER')].sort_values('share', ascending=False)
leader = named.iloc[0]
cols = st.columns(4)
cols[0].metric('Projected largest party', str(leader.party))
cols[1].metric('Projected share', f'{leader.share:.1%}')
if 'pr_votes_estimate' in metro.columns:
    cols[2].metric('Projected valid PR votes', f'{metro.pr_votes_estimate.sum():,.0f}')
else:
    cols[2].metric('Projected valid PR votes', 'See notebook')
if answers is not None and 'required_output' in answers.columns and (answers.required_output == 'Projected turnout').any():
    cols[3].metric('Projected turnout', answers.loc[answers.required_output == 'Projected turnout', 'result'].iloc[0])
else:
    cols[3].metric('Projected turnout', 'See notebook')

st.subheader('Executive conclusion')
g = OUT / 'governance_inference.txt'
st.info(g.read_text(encoding='utf-8') if g.exists() else 'Governance inference not exported.')

left, right = st.columns([1.25, 1])
with left:
    p = metro.sort_values('share')
    fig, ax = plt.subplots(figsize=(8,5))
    ax.barh(p.party, 100*p.share)
    ax.set_xlabel('Projected valid PR vote share (%)')
    ax.set_title('Conditional projection: 4 November 2026')
    st.pyplot(fig, clear_figure=True)
with right:
    st.subheader('Projected party support')
    show = [c for c in ['party','share','pr_votes_estimate'] if c in metro.columns]
    t = metro[show].copy()
    if 'share' in t.columns:
        t['share'] = t['share'].map(lambda x: f'{x:.1%}')
    st.dataframe(t, use_container_width=True, hide_index=True)

st.subheader('Selected ward forecasts')
if leaders is not None:
    st.dataframe(leaders, use_container_width=True, hide_index=True)
if ward_sel is not None:
    with st.expander('Ward choice and geographic comparability', expanded=True):
        st.dataframe(ward_sel, use_container_width=True, hide_index=True)
if wards is not None:
    with st.expander('Ward party-share detail'):
        st.dataframe(wards, use_container_width=True, hide_index=True)

st.subheader('Coalition / governance arithmetic')
st.caption('Mathematical support combinations only. Exact 2026 council-seat allocation requires all ward winners and the statutory seat calculation; coalition agreements are not predicted.')
if coal is not None:
    st.dataframe(coal, use_container_width=True, hide_index=True)

st.subheader('Validation and uncertainty')
a, b = st.columns(2)
with a:
    if rolling is not None:
        st.dataframe(rolling, use_container_width=True, hide_index=True)
with b:
    if unc is not None:
        st.dataframe(unc, use_container_width=True, hide_index=True)

st.subheader('Evidence classification')
if evidence is not None:
    st.dataframe(evidence, use_container_width=True, hide_index=True)

with st.expander('Methodology and limitations'):
    st.markdown('''- Historical observations, derived variables and 4 November 2026 predictions are labelled separately.
- Ward identifiers are not assumed geographically stable; MDB polygon alignment determines admissible histories.
- Model selection uses temporal backtesting, not random train/test splitting.
- Persistence is retained if it validates better than Ridge; unnecessary complexity is rejected.
- 2024 provincial evidence is supporting context, not a municipal observation.
- Diagnostic uncertainty is not a calibrated probability interval.
- Largest-party support does not directly determine the executive mayor or coalition agreement.''')

st.subheader('Official data sources')
st.markdown('''- [IEC election results/downloads](https://results.elections.org.za/)
- [IEC municipal seat calculation](https://www.elections.org.za/content/Documents/Voter-education/Continuous-Voter-Education/How-Council-seats-are-calculated/)
- [MDB 2024/2026 ward delimitation](https://www.demarcation.org.za/ward-delimitation-2024-2026/)''')
