"""Streamlit application for the DSC670 commercial fleet incentive assistant."""

from pathlib import Path
import copy
import json
import os

os.environ.setdefault('USE_TF', '0')
os.environ.setdefault('USE_FLAX', '0')
os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')

import streamlit as st

from example_cases import make_example
from incentive_logic import review_generated_answer, strict_json, validate_payload
from model_runtime import find_model_folder, load_saved_model
from training_contract import BASE_MODEL_ID, EXPECTED_RUN_ID

st.set_page_config(page_title='Fleet Incentive Assistant', layout='wide', initial_sidebar_state='expanded')
st.markdown('''<style>
    .block-container {padding-top:2rem; max-width:1260px;}
    [data-testid="stSidebar"] {background-color:#edf3f7;}
    h1, h2, h3 {color:#173e52;}
    [data-testid="stMetric"] {border-top:2px solid #167d8d; padding-top:.6rem;}
</style>''', unsafe_allow_html=True)

SCENARIOS = {
    'Complete utility project': 'calc_confirmed',
    'Funding still needs confirmation': 'calc_funding_unknown',
    'Multiple ports per charger': 'calc_multiport',
    'Purchase after confirmed approval': 'calc_after_approved_purchase',
    'Approval status unknown': 'approval_unknown',
    'Approval not received': 'approval_pending',
    'Port count missing': 'ports_unknown',
    'Eligible cost unconfirmed': 'cost_unconfirmed',
    'Serving utility unconfirmed': 'utility_unknown',
    'Government jurisdiction missing': 'jurisdiction_unknown',
    'Conflicting program sources': 'source_conflict',
    'Purchase without required approval': 'purchased_without_approval',
    'Different serving utility': 'wrong_utility',
    'Government program overview': 'overview_submission',
}
STATUS = {
    'clarification_needed': 'More information needed',
    'source_conflict': 'Program sources conflict',
    'not_applicable': 'Project does not meet the supplied rules',
    'potential_match': 'Potential program match',
    'ready_for_calculation': 'Model proposes a calculation',
}


@st.cache_resource(show_spinner=False)
def get_model(folder, device_choice):
    # Keep the model in memory instead of loading it after every form interaction.
    return load_saved_model(folder, device_choice)


def approval_index(value):
    return 0 if value is True else 1 if value is False else 2


def render_result(review, view_key):
    if not review:
        st.info('Enter the project facts and run a review to see the assistant\'s response.')
        return
    generation = review['generation']
    checked = review['checked']
    official = 'planning_checks' in checked
    st.caption('Results for the most recently submitted project facts')
    if checked['validation_error']:
        st.error('The model\'s response could not be accepted. No estimate was calculated.')
        st.write(checked['validation_error'])
    else:
        response = checked['response']
        st.subheader('Model proposes a per-port ceiling' if official and response['decision'] == 'ready_for_calculation' else STATUS[response['decision']])
        st.write(response['summary'])
        if checked['calculation_blocked']:
            st.error('Python blocked the proposed calculation.')
            st.write(checked['calculation_blocked'])
        if checked['estimate']:
            estimate = checked['estimate']
            if estimate.get('kind') == 'published_per_port_ceiling':
                st.metric('Published per-port ceiling — before DTE caps and review', f"${estimate['conditional_estimate']:,.2f}")
                st.write(f"{estimate['charging_ports']} confirmed ports × ${estimate['rebate_per_port']:,.2f} per port.")
                st.warning(estimate['explanation'])
            else:
                st.metric('Conditional incentive estimate', f"${estimate['conditional_estimate']:,.2f}")
                st.caption('Illustrative program only. Funding, eligibility, and an award are not guaranteed.')
                st.dataframe(
                    [{'Limit': name, 'Amount (USD)': f'${amount:,.2f}'}
                     for name, amount in estimate['limits'].items()],
                    hide_index=True, width='stretch',
                )
                st.write('The estimate uses the lowest of the per-port allowance, eligible-cost percentage, and program cap.')
        if response['questions']:
            st.markdown('**Questions to resolve**')
            for question in response['questions']:
                st.write('• ' + question)
        if response['missing_fields']:
            st.caption('Fields requiring confirmation: ' + ', '.join(response['missing_fields']))
        if response['caveats']:
            st.markdown('**Conditions to keep in view**')
            for caveat in response['caveats']:
                st.write('• ' + caveat)
        st.caption('Source IDs: ' + ', '.join(response['source_ids']))
        st.warning('Review the explanation against the supplied evidence. Passing the field checks does not prove every sentence is accurate.')
    if official:
        unresolved = [r for r in checked['planning_checks'] if r['status'] != 'confirmed']
        if unresolved:
            st.markdown('**Independent Python check: facts still to resolve**')
            for row in unresolved:
                st.write(f"• {row['requirement']}: {row['status']}")
        else:
            st.caption('Independent Python check: the supplied planning facts are complete. Final DTE approval and discretionary caps remain unresolved.')
        if checked.get('model_decision_matches_checks') is False:
            st.error('The model’s decision differs from the independent planning checks. The original model answer is retained below.')
        with st.expander('Independent planning checklist'):
            st.dataframe(checked['planning_checks'], hide_index=True, width='stretch')
    left, center, right = st.columns(3)
    left.metric('Response time', f"{generation['seconds']:.2f} s")
    center.metric('Input tokens', generation['input_tokens'])
    right.metric('Generated tokens', generation['output_tokens'])
    with st.expander('Model response and calculation checks'):
        st.code(checked['raw_response'], language='json')
        st.json({key: value for key, value in checked.items() if key != 'raw_response'})
    with st.expander('Submitted customer facts and program evidence'):
        st.json(review['payload'])
    st.download_button(
        'Download this review', json.dumps(review, indent=2, ensure_ascii=False),
        file_name='fleet_incentive_review.json', mime='application/json',
        key='download_' + view_key,
    )


with st.sidebar:
    st.title('Fleet Incentives')
    st.caption('Dan Morrow · DSC670 final project')
    review_mode = st.selectbox('Review mode', ['Official DTE eFleet program', 'Fictional training examples'])
    st.markdown('### Saved model')
    model_folder = st.text_input('Full model folder', value=find_model_folder())
    device_choice = st.selectbox('Inference device', ['auto', 'cpu', 'mps', 'cuda'])
    if st.button('Load saved model', width='stretch'):
        st.session_state.pop('runtime', None)
        st.session_state.pop('loaded_settings', None)
        st.session_state.pop('review', None)
        try:
            with st.spinner('Checking the saved files and loading the fine-tuned model...'):
                st.session_state.runtime = get_model(model_folder, device_choice)
                st.session_state.loaded_settings = (model_folder, device_choice)
        except Exception as error:
            st.error(str(error))
    runtime = st.session_state.get('runtime')
    settings_match = st.session_state.get('loaded_settings') == (model_folder, device_choice)
    model_ready = runtime is not None and settings_match
    if model_ready:
        st.success('Fine-tuned model loaded')
        st.caption(f'Run {runtime.provenance["run_id"]} · {runtime.device.upper()}')
    else:
        st.info('Load the saved Milestone 3 model to enable reviews.')
    st.divider()
    st.markdown('### Prototype scope')
    st.write('A dated official DTE eFleet rules snapshot, plus the earlier fictional examples. No live incentive search, funding check, or guaranteed eligibility.')
    st.caption('Customer entries remain in the current app session. Model inference uses local files.')

if review_mode == 'Official DTE eFleet program':
    from official_ui import render_official
    render_official(runtime, model_ready, render_result)
    st.stop()

st.caption('COMMERCIAL FLEET CHARGING')
st.title('Incentive review, with the missing facts visible')
st.write('Review a project against supplied program rules, clarify what is missing, and calculate a conditional estimate when the inputs are confirmed.')
st.warning('Course prototype: all included programs are fictional. Use fictional customer information.')

project_tab, result_tab, evidence_tab, model_tab = st.tabs(
    ['Project review', 'Latest result', 'Program evidence', 'Model and evaluation']
)

with project_tab:
    scenario_name = st.selectbox('Example project', list(SCENARIOS))
    if st.session_state.get('scenario_name') != scenario_name:
        st.session_state.scenario_name = scenario_name
        st.session_state.pop('review', None)
    # Only the payload goes to the model; authored expected answers are not used.
    example = make_example(SCENARIOS[scenario_name], 'test', 2000)
    payload = copy.deepcopy(example['payload'])
    customer = payload['customer']
    key = SCENARIOS[scenario_name]
    with st.form('project_' + key):
        st.subheader('Customer and project facts')
        a, b = st.columns(2)
        with a:
            location = st.text_input('Project location', value=customer.get('location', ''))
            utility = st.text_input('Serving utility', value=customer.get('utility') or '')
            utility_confirmed = st.checkbox('Serving utility confirmed', value=customer.get('utility_confirmed') is True)
            account = st.text_input('Account class', value=customer.get('account_class', 'nonresidential'))
            account_confirmed = st.checkbox('Account class confirmed', value=customer.get('account_class_confirmed') is True)
        with b:
            chargers = st.number_input('Number of chargers', min_value=1, max_value=10000, value=int(customer.get('chargers') or 1))
            ports = st.number_input('Number of charging ports', min_value=0, max_value=10000, value=int(customer.get('charging_ports') or 0), help='Use 0 when the count is unknown. Chargers and ports are not interchangeable.')
            ports_confirmed = st.checkbox('Port count confirmed', value=customer.get('ports_confirmed') is True)
            total_cost = st.number_input('Total project cost (USD)', min_value=0.0, value=float(customer.get('total_project_cost') or 0), step=1000.0)
            eligible_cost = st.number_input('Eligible project cost (USD)', min_value=0.0, value=float(customer.get('eligible_project_cost') or 0), step=1000.0)
            eligible_confirmed = st.checkbox('Eligible cost confirmed against the program', value=customer.get('eligible_cost_confirmed') is True)
        st.subheader('Timing and approval')
        a, b = st.columns(2)
        with a:
            approval = st.selectbox('Required approval status', ['Received', 'Not received', 'Unknown'], index=approval_index(customer.get('prior_approval')))
        with b:
            purchased = st.checkbox('Equipment already purchased', value=customer.get('purchased') is True)
            before_purchase = st.checkbox('Approval before purchase confirmed', value=customer.get('approval_before_purchase_confirmed') is True)
        task = st.text_area('What should the assistant review?', value=payload['task'], height=90)
        with st.expander('Program evidence supplied to the model'):
            evidence_text = st.text_area('Program records (JSON)', value=json.dumps(payload['program_evidence'], indent=2), height=300)
            st.caption('Each record needs a source_id, program_type, and rule_text. These examples use fictional evidence, not live websites.')
        submitted = st.form_submit_button('Review project', type='primary', disabled=not model_ready, width='stretch')
    if not model_ready:
        st.caption('Project review becomes available after the saved fine-tuned model is loaded.')
    if submitted:
        # Clear the prior result before attempting a new review.
        st.session_state.pop('review', None)
        try:
            customer.update(
                location=location, utility=utility.strip() or None,
                utility_confirmed=utility_confirmed, account_class=account,
                account_class_confirmed=account_confirmed, chargers=int(chargers),
                charging_ports=int(ports) if ports else None, ports_confirmed=ports_confirmed,
                total_project_cost=float(total_cost),
                eligible_project_cost=float(eligible_cost) if eligible_cost else None,
                eligible_cost_confirmed=eligible_confirmed,
                prior_approval={'Received': True, 'Not received': False, 'Unknown': None}[approval],
                purchased=purchased,
            )
            if purchased:
                customer['approval_before_purchase_confirmed'] = before_purchase
            payload['task'] = task
            payload['program_evidence'] = strict_json(evidence_text)
            validate_payload(payload)
            with st.spinner('The fine-tuned model is reviewing the supplied facts...'):
                generation = runtime.generate(payload)
            checked = review_generated_answer(payload, generation['raw_response'], generation['hit_token_limit'])
            st.session_state.review = {'payload': payload, 'generation': generation, 'checked': checked}
        except Exception as error:
            st.error(f'The review did not complete: {error}')
    if st.session_state.get('review'):
        st.divider()
        render_result(st.session_state.review, 'project')

with result_tab:
    render_result(st.session_state.get('review'), 'result')

with evidence_tab:
    st.subheader('What the assistant is using')
    st.write('The model receives the customer facts and the program records for the selected example. It does not search the web or confirm that funding is available.')
    current = st.session_state.get('review')
    evidence = current['payload']['program_evidence'] if current else payload['program_evidence']
    for program in evidence:
        st.markdown('**' + program['source_id'] + '**')
        st.write(program['rule_text'])
        st.json(program, expanded=False)
    st.info('A production version would need current official sources, verification dates, and testing with real program requirements.')

with model_tab:
    st.subheader('The model behind this app')
    st.write(f'{BASE_MODEL_ID}, fully fine-tuned in Milestone 3. All 494,032,768 parameters were trainable; no LoRA adapter was used.')
    st.caption('The figures below are the recorded Milestone 3 evaluation, not scores from a new application test.')
    a, b, c = st.columns(3)
    a.metric('Strict checks passed', '25 / 28')
    b.metric('Correct decisions', '26 / 28')
    c.metric('Usable complete handoffs', '8 / 8')
    st.dataframe([
        {'Measure': 'Strict checks', 'Pretrained': '0 / 28', 'Fine-tuned': '25 / 28'},
        {'Measure': 'Decision only', 'Pretrained': '6 / 28', 'Fine-tuned': '26 / 28'},
        {'Measure': 'Usable complete calculation cases', 'Pretrained': '0 / 8', 'Fine-tuned': '8 / 8'},
        {'Measure': 'Incorrect ready decisions', 'Pretrained': '12', 'Fine-tuned': '1'},
    ], hide_index=True, width='stretch')
    st.write('The remaining strict failures involved approval that had not been received, an unconfirmed eligible cost, and confirmation of a named utility. Manual review also found an inaccurate explanation in a response that passed the structured checks.')
    st.markdown('**What Python checks separately**')
    st.write('The serving utility and account must match. Port count, eligible cost, and required approval must be confirmed. Proposed calculation values must match the evidence exactly. Python then applies the per-port allowance, cost-percentage limit, and cap.')
    if model_ready:
        st.markdown('**Loaded model provenance**')
        st.json(runtime.provenance)
    else:
        st.caption(f'Expected training run: {EXPECTED_RUN_ID}. A missing artifact disables model reviews; the app does not substitute an untrained model.')
