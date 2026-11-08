"""Fictional scenarios reproduced from the Milestone 3 notebook."""

import random
import hashlib
import json
SCENARIO_TYPES = ['calc_confirmed', 'calc_funding_unknown', 'calc_multiport', 'calc_after_approved_purchase', 'approval_unknown', 'approval_pending', 'ports_unknown', 'cost_unconfirmed', 'utility_unknown', 'jurisdiction_unknown', 'source_conflict', 'purchased_without_approval', 'wrong_utility', 'overview_submission']

def make_example(kind, split, variant):
    rng = random.Random(f'incentive-data-{split}-{variant}')
    case_id = 'SIM-' + hashlib.sha256(f'{split}-{variant}-{kind}'.encode()).hexdigest()[:12]
    utility = f'Prairie Demonstration Utility {rng.randrange(100, 999)}'
    chargers = rng.choice([3, 5, 7, 9, 12, 16])
    cost = rng.choice([27000, 46000, 73000, 94000, 128000])
    rate = rng.choice([900, 1400, 2200, 2800])
    cap = rng.choice([10000, 18000, 26000])
    fraction = rng.choice([0.35, 0.4, 0.5])
    customer = {'location': 'Omaha, NE', 'utility': utility, 'utility_confirmed': True, 'account_class': 'nonresidential', 'account_class_confirmed': True, 'chargers': chargers, 'charging_ports': chargers, 'ports_confirmed': True, 'total_project_cost': cost + 17000, 'eligible_project_cost': cost, 'eligible_cost_confirmed': True, 'prior_approval': True, 'purchased': False}
    program = {'source_id': case_id, 'program_type': 'utility', 'utility': utility, 'eligible_account_class': 'nonresidential', 'rebate_per_port': rate, 'percent_limit': fraction, 'maximum_rebate': cap, 'prior_approval_required': True, 'rule_text': rng.choice(['Receive program approval before purchasing equipment. Funding is limited.', 'Equipment purchases require prior approval. Awards depend on available funding.', 'Approval must come before the equipment purchase. Remaining funds are not guaranteed.'])}
    programs = [program]
    task = rng.choice(['Can we send the confirmed inputs to Python for a conditional utility estimate?', 'Review these project facts and decide whether the calculation handoff is ready.', 'The salesperson needs the next step: clarify a requirement or pass supported inputs to Python.'])
    decision, missing, questions = ('ready_for_calculation', [], [])
    caveats = ['Any estimated amount remains conditional; available funding and an award are not guaranteed.']
    summary = rng.choice(['Approval and the required project facts are confirmed, so the inputs can go to Python.', 'The supplied confirmations support a conditional calculation without another intake question.', 'There is enough confirmed information for the calculation handoff, subject to program funding.'])
    if kind == 'calc_funding_unknown':
        program['funding_remaining_confirmed'] = None
        caveats.append('Remaining funding has not been confirmed; this does not establish an award.')
        summary = 'The project inputs and approval are confirmed. Unknown remaining funding limits the estimate, but does not block the conditional calculation.'
    elif kind == 'calc_multiport':
        customer['charging_ports'] = chargers * 2
        summary = 'The confirmed port count differs from the charger count. Use the stated ports and confirmed eligible cost for the calculation.'
    elif kind == 'calc_after_approved_purchase':
        customer['purchased'] = True
        customer['approval_before_purchase_confirmed'] = True
        summary = 'Approval was received before purchase, and the required values are confirmed for a conditional calculation.'
        program['rule_text'] += ' The project record confirms approval preceded the purchase.'
    elif kind in ['approval_unknown', 'approval_pending']:
        customer['prior_approval'] = None if kind == 'approval_unknown' else False
        decision, missing = ('clarification_needed', ['prior_approval'])
        if kind == 'approval_unknown':
            questions = ['Has the required approval been received before equipment purchase?']
            summary = 'Approval status is unknown, so the required approval needs to be clarified.'
        else:
            questions = ['What is the plan to obtain the required approval before purchasing the equipment?']
            summary = rng.choice(['Approval has not been received and the equipment is not purchased. Resolve the approval step before this workflow hands off a calculation.', 'The record explicitly says approval has not been granted. Obtain it before equipment purchase and before this calculation handoff.', 'Required approval is still outstanding. The equipment has not been bought, so the next step is obtaining approval before purchase.'])
    elif kind == 'ports_unknown':
        customer['charging_ports'], customer['ports_confirmed'] = (None, False)
        decision, missing = ('clarification_needed', ['charging_ports'])
        questions = ['How many ports are confirmed, rather than just how many chargers?']
        summary = 'The supplied charger count does not confirm the number of charging ports.'
    elif kind == 'cost_unconfirmed':
        customer['eligible_cost_confirmed'] = False
        decision, missing = ('clarification_needed', ['eligible_cost_confirmed'])
        questions = ['Has the proposed eligible cost been checked against the program rules?']
        summary = 'The amount is supplied but its eligibility is unconfirmed. Do not substitute the total project cost.'
        if variant % 2:
            customer['eligible_project_cost'] = None
            missing = ['eligible_project_cost']
            questions = ['What project cost is confirmed as eligible under the program?']
            summary = 'The eligible cost is missing. The total project cost cannot replace it.'
    elif kind == 'utility_unknown':
        customer['utility'], customer['utility_confirmed'] = (None, False)
        decision, missing = ('clarification_needed', ['utility'])
        questions = ['Which utility serves this project?']
        summary = 'Establish the serving utility before moving on to this utility program.'
        if variant % 2:
            customer['utility'] = utility
            missing = ['utility_confirmed']
            questions = ['Can you confirm this named utility actually serves the project?']
            summary = 'A utility was named but has not been confirmed as the serving utility.'
    elif kind == 'jurisdiction_unknown':
        task = 'Check whether this government program could apply to the project location.'
        programs = [{'source_id': case_id, 'program_type': 'government', 'jurisdiction': None, 'rule_text': 'Businesses in the state can apply before work begins.'}]
        decision, missing = ('clarification_needed', ['program_jurisdiction'])
        questions = ['Which state is covered by the program?']
        summary = 'The program does not identify its state. A customer location alone cannot establish the program jurisdiction.'
    elif kind == 'source_conflict':
        programs.append(dict(program, source_id=case_id + '-2', rebate_per_port=rate + 700, maximum_rebate=cap + 4000))
        decision = 'source_conflict'
        questions = ['Which of these conflicting program versions is authoritative?']
        summary = 'Both the rate and cap differ between sources, with no evidence identifying the authoritative version.'
    elif kind == 'purchased_without_approval':
        customer['purchased'], customer['prior_approval'] = (True, False)
        customer['approval_before_purchase_confirmed'] = False
        decision = 'not_applicable'
        summary = rng.choice(['The project purchased equipment without the required prior approval and does not meet the stated timing rule.', 'Approval was not received before the equipment was bought, so this project fails the program timing requirement.', 'The purchase is already complete and required approval was not received. This program does not apply under the supplied rule.'])
    elif kind == 'wrong_utility':
        program['utility'] = 'Different Demonstration Utility'
        decision = 'not_applicable'
        summary = 'The confirmed serving utility does not match the utility covered by this program.'
    elif kind == 'overview_submission':
        task = 'Explain this government program and its application timing. No estimate is requested.'
        programs = [{'source_id': case_id, 'program_type': 'government', 'jurisdiction': 'Nebraska', 'rule_text': 'Submit the application before construction begins. Awards depend on funding.'}]
        customer['charging_ports'], customer['eligible_project_cost'] = (None, None)
        customer['ports_confirmed'], customer['eligible_cost_confirmed'] = (False, False)
        decision = 'potential_match'
        summary = 'The Nebraska program may be relevant. It requires submission before construction, not a stated approval-before-construction step.'
    inputs = None
    if decision == 'ready_for_calculation':
        inputs = {'charging_ports': customer['charging_ports'], 'rebate_per_port': rate, 'eligible_project_cost': cost, 'percent_limit': fraction, 'maximum_rebate': cap}
    expected = {'decision': decision, 'missing_fields': missing, 'questions': questions, 'summary': summary, 'calculation_inputs': inputs, 'caveats': caveats, 'source_ids': [p['source_id'] for p in programs]}
    keys = list(customer)
    rng.shuffle(keys)
    customer = {key: customer[key] for key in keys}
    return {'case_id': case_id, 'family': kind, 'split': split, 'variant': variant, 'payload': {'task': task, 'customer': customer, 'program_evidence': programs}, 'expected': expected}
