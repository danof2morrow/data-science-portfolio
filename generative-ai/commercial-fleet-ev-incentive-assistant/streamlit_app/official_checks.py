"""Run repeatable official-program examples with the actual saved model."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import zipfile

from incentive_logic import review_generated_answer, validate_payload
from official_program import (PROGRAM_ID, REVIEW_DATE, SCENARIOS,
                              SNAPSHOT_SHA256, expected_planning_decision,
                              make_official_case)


def evaluate_review(payload, generation):
    validate_payload(payload)
    checked = review_generated_answer(payload, generation['raw_response'], generation['hit_token_limit'])
    return {'payload': payload, 'generation': generation, 'checked': checked}


def summarize_review(review):
    checked, kind, payload = review['checked'], review['case'], review['payload']
    response = checked['response']
    actual = response['decision'] if response else None
    expected = expected_planning_decision(payload)
    amount = checked['estimate']['conditional_estimate'] if checked['estimate'] else None
    expected_amount = 40000 if kind == 'complete' else 14000 if kind == 'electric_choice' else None
    incomplete_field = {'ports_unknown': 'ports_confirmed', 'meter_unknown': 'meter_network_path',
                        'choice_unknown': 'electric_choice_customer'}.get(kind)
    clarification_specific = (bool(response and response['questions'] and
                                   incomplete_field in response['missing_fields'])
                              if incomplete_field else None)
    return {
        'case': kind, 'expected_decision': expected, 'model_decision': actual,
        'decision_correct': actual == expected,
        'handoff_accepted': checked['estimate'] is not None,
        'published_ceiling': amount, 'expected_ceiling': expected_amount,
        'clarification_field_and_question': clarification_specific,
        'structured_workflow_correct': (actual == expected and amount == expected_amount
            and not checked['validation_error'] and clarification_specific is not False),
        'calculation_blocked': checked['calculation_blocked'],
        'validation_error': checked['validation_error'],
        'seconds': review['generation']['seconds'],
    }


def run_live_checks(runtime, progress=None):
    """Targets are evaluated afterward and are never included in model input."""
    reviews, rows = [], []
    for index, (label, kind) in enumerate(SCENARIOS.items()):
        payload = make_official_case(kind)
        generation = runtime.generate(payload)
        review = evaluate_review(payload, generation)
        review['case'] = kind
        review['case_label'] = label
        reviews.append(review)
        rows.append(summarize_review(review))
        if progress:
            progress(index + 1, len(SCENARIOS), label)
    return {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'program_id': PROGRAM_ID, 'source_review_date': REVIEW_DATE,
        'rules_snapshot_sha256': SNAPSHOT_SHA256,
        'evidence_type': 'actual_saved_model_inference',
        'scope': 'Six authored fictional customer cases using reviewed official rules; not independent real-world accuracy.',
        'summary': rows, 'reviews': reviews,
    }


def bundle_bytes(report):
    import io
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('official_program_live_checks.json', json.dumps(report, indent=2))
        for review in report['reviews']:
            archive.writestr(review['case'] + '_review.json', json.dumps(review, indent=2))
    return data.getvalue()


def verify_live_report(report):
    """Check provenance and recalculate checks when importing a downloaded report."""
    from training_contract import EXPECTED_RUN_ID, EXPECTED_MANIFEST_PREFIX
    from official_program import OFFICIAL_SYSTEM_PROMPT, OFFICIAL_PROMPT_VERSION
    if (report.get('rules_snapshot_sha256') != SNAPSHOT_SHA256
            or report.get('evidence_type') != 'actual_saved_model_inference'):
        raise ValueError('This report belongs to another rules snapshot or test type.')
    reviews = report.get('reviews')
    if not isinstance(reviews, list) or len(reviews) != len(SCENARIOS):
        raise ValueError('The report must contain the six official-program cases.')
    seen = set()
    for review in reviews:
        kind = review.get('case')
        if kind not in SCENARIOS.values() or kind in seen:
            raise ValueError('The case list is incomplete or repeated.')
        seen.add(kind)
        generation = review['generation']
        if (generation.get('model_run') != EXPECTED_RUN_ID
                or not generation.get('model_manifest_sha256', '').startswith(EXPECTED_MANIFEST_PREFIX)
                or generation.get('rules_snapshot_sha256') != SNAPSHOT_SHA256
                or generation.get('inference_prompt_version') != OFFICIAL_PROMPT_VERSION
                or generation.get('inference_prompt_sha256') != hashlib.sha256(OFFICIAL_SYSTEM_PROMPT.encode()).hexdigest()):
            raise ValueError('The model, rules, or inference-prompt identity does not match.')
        if review['payload'] != make_official_case(kind):
            raise ValueError('A recorded scenario differs from the defined check.')
        calculated = evaluate_review(review['payload'], generation)
        if calculated['checked'] != review['checked']:
            raise ValueError('Saved calculation checks do not reproduce from the raw response.')
    if report.get('summary') != [summarize_review(r) for r in reviews]:
        raise ValueError('The summary does not reproduce from the recorded reviews.')
    return report


def main():
    from model_runtime import load_saved_model
    parser = argparse.ArgumentParser(description='Run six live checks with the saved Milestone 3 model.')
    parser.add_argument('--model-dir', required=True)
    parser.add_argument('--device', choices=['auto', 'cpu', 'mps', 'cuda'], default='auto')
    parser.add_argument('--output', default='official_program_live_checks.json')
    args = parser.parse_args()
    runtime = load_saved_model(args.model_dir, args.device)
    report = run_live_checks(runtime, lambda n, total, label: print(f'{n}/{total}: {label}', flush=True))
    verify_live_report(report)
    path = Path(args.output)
    path.write_text(json.dumps(report, indent=2))
    print(f'Saved {path.resolve()}')


if __name__ == '__main__':
    main()
