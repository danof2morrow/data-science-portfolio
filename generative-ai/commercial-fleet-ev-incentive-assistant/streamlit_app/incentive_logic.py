"""Validate the model's handoff and calculate supported conditional estimates."""

from decimal import Decimal, ROUND_HALF_UP
import json
import math

DECISIONS = {
    'clarification_needed', 'source_conflict', 'not_applicable',
    'potential_match', 'ready_for_calculation',
}
RESPONSE_KEYS = {
    'decision', 'missing_fields', 'questions', 'summary',
    'calculation_inputs', 'caveats', 'source_ids',
}
INPUT_KEYS = {
    'charging_ports', 'rebate_per_port', 'eligible_project_cost',
    'percent_limit', 'maximum_rebate',
}


def valid_number(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value))


def _unique_object(pairs):
    # Repeated keys can hide a different value from the one a reader sees.
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Repeated JSON key: {key}')
        result[key] = value
    return result


def strict_json(text):
    def reject_constant(value):
        raise ValueError(f'Invalid JSON constant: {value}')
    return json.loads(text, object_pairs_hook=_unique_object,
                      parse_constant=reject_constant)


def validate_payload(payload):
    if not isinstance(payload, dict) or set(payload) != {'task', 'customer', 'program_evidence'}:
        raise ValueError('The request needs a task, customer, and program_evidence.')
    if not isinstance(payload['task'], str) or not payload['task'].strip():
        raise ValueError('Describe what the assistant should review.')
    if not isinstance(payload['customer'], dict):
        raise ValueError('Customer facts must be a JSON object.')
    programs = payload['program_evidence']
    if not isinstance(programs, list) or not 1 <= len(programs) <= 3:
        raise ValueError('Provide one to three program evidence records.')
    seen = set()
    for program in programs:
        if not isinstance(program, dict):
            raise ValueError('Each evidence record must be a JSON object.')
        source_id = program.get('source_id')
        if not isinstance(source_id, str) or not source_id.strip() or source_id in seen:
            raise ValueError('Each evidence record needs a unique source_id.')
        seen.add(source_id)
        if program.get('program_type') not in {'utility', 'government'}:
            raise ValueError('Program type must be utility or government.')
        if not isinstance(program.get('rule_text'), str) or not program['rule_text'].strip():
            raise ValueError('Each program needs its rule_text.')
    if len(json.dumps(payload, allow_nan=False)) > 14000:
        raise ValueError('This prototype accepts a short project and program description.')
    return payload


def parse_response(text, official=False):
    # Keep malformed answers visible instead of silently repairing the model's JSON.
    obj = strict_json(text)
    if not isinstance(obj, dict) or set(obj) != RESPONSE_KEYS:
        raise ValueError('The model did not return the seven required response fields.')
    if not isinstance(obj['decision'], str) or obj['decision'] not in DECISIONS:
        raise ValueError('The model returned an unsupported decision.')
    if not isinstance(obj['summary'], str) or not obj['summary'].strip():
        raise ValueError('The model did not provide an explanation.')
    for name in ['missing_fields', 'questions', 'caveats', 'source_ids']:
        if not isinstance(obj[name], list) or not all(isinstance(x, str) for x in obj[name]):
            raise ValueError(f'{name} must be a list of text values.')
    inputs = obj['calculation_inputs']
    if inputs is not None:
        if (not isinstance(inputs, dict) or set(inputs) != INPUT_KEYS):
            raise ValueError('The model returned invalid calculation inputs.')
        if official:
            if (not all(valid_number(inputs[k]) for k in ['charging_ports', 'rebate_per_port'])
                    or any(inputs[k] is not None for k in ['eligible_project_cost', 'percent_limit', 'maximum_rebate'])):
                raise ValueError('DTE requires a port count and rate; the three unsupported cost/cap fields must be null.')
        elif not all(valid_number(v) for v in inputs.values()):
            raise ValueError('The model returned invalid calculation inputs.')
    if obj['decision'] != 'ready_for_calculation' and inputs is not None:
        raise ValueError('A response that is not ready cannot include calculation inputs.')
    return obj


def guarded_estimate(payload, response):
    """Use the supplied evidence to recheck every value before doing the math."""
    customer, programs = payload['customer'], payload['program_evidence']
    if response['decision'] != 'ready_for_calculation' or len(programs) != 1:
        raise ValueError('There is no single, ready calculation handoff.')
    if response['missing_fields'] or response['questions']:
        raise ValueError('The model still lists information that needs confirmation.')
    program = programs[0]
    if program.get('program_type') != 'utility':
        raise ValueError('This calculator supports the demonstrated utility formula only.')
    if sorted(response['source_ids']) != [program['source_id']]:
        raise ValueError('The model cited a source that does not match this program.')
    if not (customer.get('utility_confirmed') is True
            and customer.get('utility') == program.get('utility')
            and customer.get('account_class_confirmed') is True
            and customer.get('account_class') == program.get('eligible_account_class')
            and customer.get('ports_confirmed') is True
            and customer.get('eligible_cost_confirmed') is True):
        raise ValueError('The serving utility, account, ports, or eligible costs are unconfirmed or do not match.')
    if not isinstance(program.get('prior_approval_required'), bool):
        raise ValueError('The program must explicitly identify whether prior approval is required.')
    if program['prior_approval_required']:
        if customer.get('prior_approval') is not True:
            raise ValueError('Required approval has not been confirmed.')
        if not isinstance(customer.get('purchased'), bool):
            raise ValueError('Equipment purchase status has not been confirmed.')
        if customer['purchased'] and customer.get('approval_before_purchase_confirmed') is not True:
            raise ValueError('Approval before the purchase has not been confirmed.')
    authoritative = {
        'charging_ports': customer.get('charging_ports'),
        'rebate_per_port': program.get('rebate_per_port'),
        'eligible_project_cost': customer.get('eligible_project_cost'),
        'percent_limit': program.get('percent_limit'),
        'maximum_rebate': program.get('maximum_rebate'),
    }
    if response.get('calculation_inputs') != authoritative:
        raise ValueError('The proposed inputs do not match the customer facts and program evidence.')
    if not all(valid_number(v) and v > 0 for v in authoritative.values()):
        raise ValueError('The calculation requires positive, finite values.')
    if not float(authoritative['charging_ports']).is_integer() or authoritative['percent_limit'] > 1:
        raise ValueError('The port count or percentage limit is invalid.')
    value = {key: Decimal(str(number)) for key, number in authoritative.items()}
    limits = {
        'Per-port limit': value['charging_ports'] * value['rebate_per_port'],
        'Eligible-cost limit': value['eligible_project_cost'] * value['percent_limit'],
        'Program cap': value['maximum_rebate'],
    }
    amount = min(limits.values()).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    return {
        'conditional_estimate': float(amount), 'currency': 'USD',
        'limits': {name: float(number) for name, number in limits.items()},
        'binding_limits': [name for name, number in limits.items() if number == min(limits.values())],
        'guaranteed_award': False,
    }


def official_ceiling(payload, response):
    """Calculate only the published DTE per-port ceiling, without invented caps."""
    from official_program import (PROGRAM_ID, SNAPSHOT_SHA256, evidence_for,
                                  expected_planning_decision)
    customer, records = payload['customer'], payload['program_evidence']
    if len(records) != 1 or records[0] != evidence_for(customer):
        raise ValueError('The supplied DTE record does not match the reviewed program snapshot.')
    if expected_planning_decision(payload) != 'ready_for_calculation':
        raise ValueError('A required planning fact is missing or does not meet the supplied rules. See the independent checklist.')
    expected = {'charging_ports': customer['charging_ports'],
                'rebate_per_port': records[0]['rebate_per_port'],
                'eligible_project_cost': None, 'percent_limit': None, 'maximum_rebate': None}
    if (response['decision'] != 'ready_for_calculation'
            or response['missing_fields'] or response['questions']
            or response['source_ids'] != [PROGRAM_ID]
            or response.get('calculation_inputs') != expected):
        raise ValueError('The model handoff does not match the confirmed DTE planning facts.')
    if not response['caveats']:
        raise ValueError('The model omitted the conditional-award caveat.')
    amount = Decimal(str(expected['charging_ports'])) * Decimal(str(expected['rebate_per_port']))
    return {
        'conditional_estimate': float(amount.quantize(Decimal('.01'))),
        'currency': 'USD', 'kind': 'published_per_port_ceiling',
        'guaranteed_award': False, 'final_eligibility_verified': False,
        'site_and_participant_caps_known': False,
        'charging_ports': expected['charging_ports'],
        'rebate_per_port': expected['rebate_per_port'],
        'electric_choice_customer': customer['electric_choice_customer'],
        'source_id': PROGRAM_ID, 'rules_snapshot_sha256': SNAPSHOT_SHA256,
        'explanation': 'This is the published per-port upper bound only. DTE discretionary site/participant caps, compliance, documents and available funding can reduce it or prevent an award.',
    }


def review_generated_answer(payload, raw_text, hit_token_limit=False):
    """Keep the model's answer separate from the independent calculation check."""
    result = {'raw_response': raw_text, 'response': None, 'estimate': None,
              'validation_error': None, 'calculation_blocked': None}
    from official_program import PROGRAM_ID, official_checklist, expected_planning_decision
    official = any(p.get('source_id') == PROGRAM_ID for p in payload['program_evidence'])
    if official:
        result['planning_checks'] = official_checklist(payload['customer'])
        result['independent_planning_decision'] = expected_planning_decision(payload)
    try:
        if hit_token_limit:
            raise ValueError('The response reached its output limit and may be incomplete.')
        response = parse_response(raw_text, official=official)
        actual_sources = sorted(p['source_id'] for p in payload['program_evidence'])
        if sorted(response['source_ids']) != actual_sources:
            raise ValueError('The model\'s source IDs do not match the supplied evidence.')
        result['response'] = response
        if official:
            result['model_decision_matches_checks'] = response['decision'] == result['independent_planning_decision']
        if response['decision'] == 'ready_for_calculation':
            try:
                result['estimate'] = official_ceiling(payload, response) if official else guarded_estimate(payload, response)
            except (ValueError, TypeError, KeyError) as error:
                result['calculation_blocked'] = str(error)
    except (ValueError, TypeError, KeyError) as error:
        result['validation_error'] = str(error)
    return result
