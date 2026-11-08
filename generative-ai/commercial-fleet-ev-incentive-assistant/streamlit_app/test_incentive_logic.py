"""Check the calculator boundaries and the app's handling of model errors."""

import copy
import json
import unittest

from example_cases import make_example, SCENARIO_TYPES
from incentive_logic import (guarded_estimate, parse_response,
                             review_generated_answer, validate_payload)


class IncentiveChecks(unittest.TestCase):
    def setUp(self):
        self.case = make_example('calc_confirmed', 'test', 2000)

    def test_authored_cases_match_the_original_workflow(self):
        accepted = 0
        for scenario in SCENARIO_TYPES:
            for variant in [2000, 2001]:
                case = make_example(scenario, 'test', variant)
                validate_payload(case['payload'])
                result = review_generated_answer(case['payload'], json.dumps(case['expected']))
                self.assertIsNone(result['validation_error'])
                if case['expected']['decision'] == 'ready_for_calculation':
                    self.assertIsNotNone(result['estimate'])
                    accepted += 1
                else:
                    self.assertIsNone(result['estimate'])
        self.assertEqual(accepted, 8)

    def test_calculation_applies_all_three_limits(self):
        payload = self.case['payload']
        response = self.case['expected']
        payload['customer'].update(charging_ports=4, eligible_project_cost=15000)
        payload['program_evidence'][0].update(rebate_per_port=1500, percent_limit=.4, maximum_rebate=10000)
        response['calculation_inputs'].update(charging_ports=4, rebate_per_port=1500,
            eligible_project_cost=15000, percent_limit=.4, maximum_rebate=10000)
        self.assertEqual(guarded_estimate(payload, response)['conditional_estimate'], 6000)
        response['calculation_inputs']['percent_limit'] = .2
        payload['program_evidence'][0]['percent_limit'] = .2
        self.assertEqual(guarded_estimate(payload, response)['conditional_estimate'], 3000)
        response['calculation_inputs']['maximum_rebate'] = 1200
        payload['program_evidence'][0]['maximum_rebate'] = 1200
        self.assertEqual(guarded_estimate(payload, response)['conditional_estimate'], 1200)

    def test_false_ready_cannot_override_unconfirmed_cost(self):
        self.case['payload']['customer']['eligible_cost_confirmed'] = False
        result = review_generated_answer(self.case['payload'], json.dumps(self.case['expected']))
        self.assertIsNone(result['estimate'])
        self.assertIsNotNone(result['calculation_blocked'])

    def test_changed_input_and_wrong_source_are_rejected(self):
        response = copy.deepcopy(self.case['expected'])
        response['calculation_inputs']['charging_ports'] += 1
        result = review_generated_answer(self.case['payload'], json.dumps(response))
        self.assertIsNotNone(result['calculation_blocked'])
        response = copy.deepcopy(self.case['expected'])
        response['source_ids'] = ['UNSUPPLIED-SOURCE']
        result = review_generated_answer(self.case['payload'], json.dumps(response))
        self.assertIsNotNone(result['validation_error'])
        self.assertIsNone(result['estimate'])

    def test_purchase_timing_cannot_be_bypassed(self):
        customer = self.case['payload']['customer']
        customer['purchased'] = True
        customer['approval_before_purchase_confirmed'] = False
        with self.assertRaises(ValueError):
            guarded_estimate(self.case['payload'], self.case['expected'])
        customer['approval_before_purchase_confirmed'] = True
        self.assertGreater(guarded_estimate(self.case['payload'], self.case['expected'])['conditional_estimate'], 0)

    def test_ambiguous_sources_cannot_be_calculated(self):
        payload = self.case['payload']
        payload['program_evidence'].append(dict(payload['program_evidence'][0], source_id='CONFLICT'))
        result = review_generated_answer(payload, json.dumps(self.case['expected']))
        self.assertIsNone(result['estimate'])

    def test_malformed_or_truncated_answer_does_not_produce_estimate(self):
        for raw in ['```json\n{}\n```', '{}', '{"decision": null}', 'not JSON']:
            result = review_generated_answer(self.case['payload'], raw)
            self.assertIsNotNone(result['validation_error'])
            self.assertIsNone(result['estimate'])
        result = review_generated_answer(self.case['payload'], json.dumps(self.case['expected']), True)
        self.assertIsNotNone(result['validation_error'])

    def test_duplicate_keys_and_boolean_numbers_are_rejected(self):
        with self.assertRaises(ValueError):
            parse_response('{"decision":"potential_match","decision":"ready_for_calculation"}')
        self.case['expected']['calculation_inputs']['charging_ports'] = True
        with self.assertRaises(ValueError):
            parse_response(json.dumps(self.case['expected']))


if __name__ == '__main__':
    unittest.main()
