"""Check official-program boundaries without pretending to run the model."""

import copy
import json
import unittest

from incentive_logic import review_generated_answer
from official_program import (PROGRAM_ID, REQUIRED_TRUE, build_payload,
                              make_official_case, expected_planning_decision)


def authored_ready(payload):
    """A test fixture, not a model response or a measured result."""
    return {
        'decision': 'ready_for_calculation', 'missing_fields': [], 'questions': [],
        'summary': 'The supplied planning facts support a published per-port ceiling.',
        'calculation_inputs': {
            'charging_ports': payload['customer']['charging_ports'],
            'rebate_per_port': payload['program_evidence'][0]['rebate_per_port'] or 2500,
            'eligible_project_cost': None, 'percent_limit': None, 'maximum_rebate': None,
        },
        'caveats': ['DTE reviews compliance and determines site/participant caps; funding and an award are not guaranteed.'],
        'source_ids': [PROGRAM_ID],
    }


class OfficialProgramChecks(unittest.TestCase):
    def checked(self, payload, response=None):
        return review_generated_answer(payload, json.dumps(response or authored_ready(payload)))

    def test_actual_rate_and_electric_choice_reduction(self):
        for kind, rate, ceiling in [('complete', 2500, 40000), ('electric_choice', 875, 14000)]:
            with self.subTest(kind=kind):
                result = self.checked(make_official_case(kind))
                self.assertEqual(result['estimate']['rebate_per_port'], rate)
                self.assertEqual(result['estimate']['conditional_estimate'], ceiling)
                self.assertFalse(result['estimate']['site_and_participant_caps_known'])
                self.assertFalse(result['estimate']['final_eligibility_verified'])
                self.assertNotIn('limits', result['estimate'])

    def test_each_required_unknown_blocks_even_a_ready_model(self):
        for field in REQUIRED_TRUE:
            payload = make_official_case()
            payload['customer'][field] = None
            result = self.checked(payload)
            self.assertIsNone(result['estimate'], field)
            self.assertTrue(result['calculation_blocked'], field)
            self.assertEqual(result['independent_planning_decision'], 'clarification_needed')

    def test_unknown_choice_does_not_default_to_standard_rate(self):
        payload = make_official_case('choice_unknown')
        self.assertIsNone(payload['program_evidence'][0]['rebate_per_port'])
        self.assertIsNone(self.checked(payload)['estimate'])

    def test_meter_and_network_are_alternatives(self):
        for path in ['dedicated_meter', 'qualified_network']:
            payload = make_official_case()
            payload['customer']['meter_network_path'] = path
            self.assertIsNotNone(self.checked(payload)['estimate'])
        for path in ['unknown', 'neither']:
            payload = make_official_case()
            payload['customer']['meter_network_path'] = path
            self.assertIsNone(self.checked(payload)['estimate'])

    def test_inapplicable_utility_and_grid_requirements(self):
        payload = make_official_case('wrong_utility')
        self.assertEqual(expected_planning_decision(payload), 'not_applicable')
        self.assertIsNone(self.checked(payload)['estimate'])
        for state in ['unknown', 'declined']:
            payload = make_official_case()
            payload['customer']['grid_commitment_status'] = state
            self.assertIsNone(self.checked(payload)['estimate'])

    def test_no_invented_percentage_or_cap(self):
        payload = make_official_case()
        for field, value in [('percent_limit', .4), ('maximum_rebate', 26000), ('eligible_project_cost', 27000)]:
            response = authored_ready(payload)
            response['calculation_inputs'][field] = value
            result = self.checked(payload, response)
            self.assertIsNone(result['estimate'])
            self.assertTrue(result['validation_error'])

    def test_changed_evidence_rate_and_port_count_are_rejected(self):
        payload = make_official_case()
        payload['program_evidence'][0]['rebate_per_port'] = 9999
        self.assertIsNone(self.checked(payload)['estimate'])
        payload = make_official_case()
        response = authored_ready(payload)
        response['calculation_inputs']['charging_ports'] = 17
        self.assertIsNone(self.checked(payload, response)['estimate'])

    def test_missing_or_false_model_decision_is_not_replaced(self):
        payload = make_official_case()
        response = authored_ready(payload)
        response.update(decision='clarification_needed', calculation_inputs=None,
                        missing_fields=['already_confirmed_fact'], questions=['Confirm it?'])
        result = self.checked(payload, response)
        self.assertEqual(result['response']['decision'], 'clarification_needed')
        self.assertFalse(result['model_decision_matches_checks'])
        self.assertIsNone(result['estimate'])

    def test_invalid_ports_and_wrong_source_cannot_pass(self):
        for value in [0, -1, 2.5, True]:
            payload = make_official_case()
            payload['customer']['charging_ports'] = value
            self.assertIsNone(self.checked(payload)['estimate'])
        payload = make_official_case()
        response = authored_ready(payload)
        response['source_ids'] = ['UNSUPPLIED']
        self.assertTrue(self.checked(payload, response)['validation_error'])

    def test_no_universal_purchase_approval_rule_added(self):
        payload = make_official_case()
        self.assertNotIn('prior_approval_required', payload['program_evidence'][0])
        self.assertNotIn('prior_approval', payload['customer'])
        self.assertIsNotNone(self.checked(payload)['estimate'])

    def test_no_cost_input_required_for_published_ceiling(self):
        payload = make_official_case()
        self.assertNotIn('eligible_project_cost', payload['customer'])
        self.assertIsNotNone(self.checked(payload)['estimate'])

    def test_non_boolean_confirmation_is_not_accepted(self):
        payload = make_official_case()
        payload['customer']['site_rights'] = 'yes'
        self.assertIsNone(self.checked(payload)['estimate'])

    def test_live_report_round_trip_with_an_explicit_test_double(self):
        from official_checks import run_live_checks, verify_live_report
        from official_program import (OFFICIAL_SYSTEM_PROMPT, OFFICIAL_PROMPT_VERSION,
                                      SNAPSHOT_SHA256, official_checklist)
        from training_contract import EXPECTED_RUN_ID, EXPECTED_MANIFEST_PREFIX
        import hashlib

        class TestDouble:
            def generate(self, payload):
                # Exercise report plumbing only; no weights or model calls occur here.
                response = authored_ready(payload)
                decision = expected_planning_decision(payload)
                if decision != 'ready_for_calculation':
                    missing = [r['field'] for r in official_checklist(payload['customer']) if r['status'] == 'unknown']
                    response.update(decision=decision, calculation_inputs=None,
                                    missing_fields=missing,
                                    questions=['Can you confirm ' + f + '?' for f in missing])
                return {
                    'raw_response': json.dumps(response), 'hit_token_limit': False,
                    'model_run': EXPECTED_RUN_ID,
                    'model_manifest_sha256': EXPECTED_MANIFEST_PREFIX,
                    'inference_prompt_version': OFFICIAL_PROMPT_VERSION,
                    'inference_prompt_sha256': hashlib.sha256(OFFICIAL_SYSTEM_PROMPT.encode()).hexdigest(),
                    'rules_snapshot_sha256': SNAPSHOT_SHA256,
                    'seconds': 0, 'device': 'explicit_test_double',
                }
        report = run_live_checks(TestDouble())
        self.assertEqual(len(verify_live_report(report)['reviews']), 6)
        self.assertTrue(all(row['structured_workflow_correct'] for row in report['summary']))
        report['summary'][0]['published_ceiling'] = 1
        with self.assertRaises(ValueError):
            verify_live_report(report)


if __name__ == '__main__':
    unittest.main()
