"""Intake and live checks for the reviewed DTE eFleet Level 2 program."""

import copy
import json
import streamlit as st

from official_checks import evaluate_review, run_live_checks, bundle_bytes, verify_live_report
from official_program import (AGREEMENT_URL, SOURCE_URL, NETWORK_URL, PROGRAM,
                              SCENARIOS, CHECK_LABELS, REVIEW_DATE, make_official_case,
                              build_payload)


def tri_state(label, value, key):
    options = ['Confirmed / agreed', 'Not met', 'Unknown']
    index = 0 if value is True else 1 if value is False else 2
    selected = st.selectbox(label, options, index=index, key=key)
    return [True, False, None][options.index(selected)]


def render_official(runtime, model_ready, render_result):
    st.caption('COMMERCIAL FLEET CHARGING · OFFICIAL PROGRAM REVIEW')
    st.title('DTE eFleet: review the facts before estimating')
    st.write('Review a fictional fleet project against DTE’s published Level 2 requirements. The model proposes a next step; Python checks the planning facts and any calculation handoff.')
    st.info('Official program rules, fictional customer examples. Any displayed amount is a published per-port ceiling before DTE review and discretionary caps, not an approved award.')
    st.caption(f'Agreement revision: September 2026 · Sources reviewed: {REVIEW_DATE} · No live funding or service-territory lookup')
    project, results, evidence, checks, model = st.tabs(['Project review', 'Latest result', 'Official sources', 'Run example checks', 'Model and evaluation'])
    with project:
        label = st.selectbox('Example project', list(SCENARIOS), key='dte_scenario')
        kind = SCENARIOS[label]
        if st.session_state.get('dte_previous_case') != kind:
            st.session_state.dte_previous_case = kind
            st.session_state.pop('dte_review', None)
        customer = copy.deepcopy(make_official_case(kind)['customer'])
        with st.form('dte_form_' + kind):
            st.subheader('Account, site, and equipment')
            a, b = st.columns(2)
            with a:
                customer['location'] = st.text_input('Project location', value=customer['location'])
                customer['utility'] = st.text_input('Serving utility', value=customer['utility'])
                customer['charging_ports'] = st.number_input('Confirmed Level 2 port count', min_value=0, max_value=10000, value=customer['charging_ports'], step=1)
                choice = st.selectbox('Electric Choice customer?', ['No', 'Yes', 'Unknown'], index=2 if customer['electric_choice_customer'] is None else int(customer['electric_choice_customer']))
                customer['electric_choice_customer'] = {'No': False, 'Yes': True, 'Unknown': None}[choice]
                paths = {'Dedicated DTE meter': 'dedicated_meter', 'Qualified network provider': 'qualified_network', 'Neither requirement met': 'neither', 'Unknown': 'unknown'}
                path = st.selectbox('Meter or network arrangement confirmed', list(paths), index=list(paths.values()).index(customer['meter_network_path']))
                customer['meter_network_path'] = paths[path]
                grids = {'DTE confirmed these commitments are not required': 'not_required_confirmed', 'Applicable commitments agreed with DTE': 'commitments_agreed', 'Applicable commitments declined': 'declined', 'Not yet confirmed with DTE': 'unknown'}
                grid = st.selectbox('Load commitments and demand ceilings', list(grids), index=list(grids.values()).index(customer['grid_commitment_status']))
                customer['grid_commitment_status'] = grids[grid]
            with b:
                for name, title in CHECK_LABELS.items():
                    customer[name] = tri_state(title, customer[name], kind + '_' + name)
            st.caption('Confirmations are supplied project facts, not independent utility verification. The agreement also covers documents, site permissions, electrical work and permits, data sharing, taxes, and other continuing obligations. Read it before confirming the review.')
            submitted = st.form_submit_button('Review project', type='primary', disabled=not model_ready, width='stretch')
        if not model_ready:
            st.caption('Load the saved fine-tuned model in the sidebar to run a review.')
        if submitted:
            st.session_state.pop('dte_review', None)
            try:
                payload = build_payload(customer)
                with st.spinner('The saved fine-tuned model is reviewing the official evidence...'):
                    generation = runtime.generate(payload)
                st.session_state.dte_review = evaluate_review(payload, generation)
            except Exception as error:
                st.error(str(error))
        if st.session_state.get('dte_review'):
            st.divider()
            render_result(st.session_state.dte_review, 'dte_project')
    with results:
        render_result(st.session_state.get('dte_review'), 'dte_result')
    with evidence:
        st.subheader('Official sources and what they support')
        st.link_button('DTE eFleet program page', SOURCE_URL)
        st.link_button('September 2026 rebate agreement', AGREEMENT_URL)
        st.link_button('DTE linked network and equipment document', NETWORK_URL)
        st.write('The eFleet agreement supplies the Level 2 rate, Electric Choice reduction, requirements, and DTE’s discretion over caps and awards. The linked equipment document contains separate program sections; this app does not treat another section’s rate as the eFleet rate.')
        st.write('The calculation uses $2,500 per port for a standard customer, or $875 per port for Electric Choice. It does not apply the fictional percentage limit or fixed cap. A positive planning check supports only this upper-bound calculation; it does not establish final eligibility.')
        st.write('There is no automatic website update or funding check. Recheck the official documents before using this snapshot beyond the course demonstration. Unsupported equipment or other programs require separate review.')
        st.json(PROGRAM, expanded=False)
    with checks:
        st.subheader('Check the saved model on six customer cases')
        st.write('These checks use the real loaded model. Complete, incomplete, Electric Choice, and wrong-utility cases are evaluated afterward against the documented rules. The expected answers are never sent to the model.')
        if st.button('Run all six examples', disabled=not model_ready, type='primary'):
            st.session_state.pop('dte_live_checks', None)
            progress = st.progress(0, text='Starting live model checks...')
            try:
                report = run_live_checks(runtime, lambda n, total, title: progress.progress(n / total, text=title))
                verify_live_report(report)
                st.session_state.dte_live_checks = report
            except Exception as error:
                st.error(str(error))
        report = st.session_state.get('dte_live_checks')
        if report:
            st.dataframe(report['summary'], hide_index=True, width='stretch')
            st.download_button('Download live check report', json.dumps(report, indent=2), file_name='official_program_live_checks.json', mime='application/json')
            st.download_button('Download individual reviews', bundle_bytes(report), file_name='official_program_reviews.zip', mime='application/zip')
            st.caption('Decision scores describe six authored examples only. Review the raw explanations separately; a structured pass does not prove every sentence is correct.')
    with model:
        from training_contract import BASE_MODEL_ID, EXPECTED_RUN_ID
        st.subheader('The fully fine-tuned DTE model')
        st.write(f'{BASE_MODEL_ID}, trained on the official-program planning workflow. Expected run: {EXPECTED_RUN_ID}. The complete model weights were updated; no LoRA adapter was used.')
        st.write('The training notebook records validation measurements and fresh authored test cases. Historical scores from the earlier fictional-program model do not describe this model. Review the saved report and the generated explanations together.')
        if model_ready:
            st.json(runtime.provenance)
