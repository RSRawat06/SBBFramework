import unittest
import os
import subprocess
from collections import deque
from ...config import Config
from ...sbb import SBB

TEST_CONFIG = {
    'task': 'reinforcement',
    'reinforcement_parameters': { 
        'environment': 'tictactoe', 
        'validation_population': 20,
        'champion_population': 30,
        'hall_of_fame': {
            'size': 6,
            'enabled': False,
            'diversity': None,
            'opponents': 0,
        },
    },
    'training_parameters': {
        'runs_total': 2,
        'generations_total': 30,
        'validate_after_each_generation': 30,
        'populations': {
            'teams': 12,
            'points': 12,
        },
        'replacement_rate': {
            'teams': 0.5,
            'points': 0.2,
        },
        'mutation': {
            'team': {
                'remove_program': 0.7,
                'add_program': 0.8,
                'mutate_program': 0.2,
            },
            'program': {
                'remove_instruction': 0.7,
                'add_instruction': 0.8,
                'change_instruction': 0.8,
                'swap_instructions': 0.8,
                'change_action': 0.1,
            },
        },
        'team_size': { 
            'min': 2,
            'max': 12,
        },
        'program_size': {
            'min': 2,
            'max': 12,
        },
    },

    'advanced_training_parameters': {
        'seed': 1,
        'use_pareto_for_point_population_selection': False,
        'use_operations': ['+', '-', '*', '/', 'if_lesser_than', 'if_equal_or_higher_than'],
        'extra_registers': 4,
        'diversity': {
            'use_and_show': [],
            'only_show': [],
            'k': 8,
        },
        "novelty": {
            "enabled": False,
            "dont_use_fitness": False,
        },
        'run_initialization_step2': False,
        'use_weighted_probability_selection': False,
        'use_agressive_mutations': False,
        'second_layer': {
            'enabled': False,
            'path': 'SBB/tests/system_tests/actions_reference/run[run_id]/second_layer_files/hall_of_fame/actions.json',
        },
    },

    "debug": {
        "enabled": False,
        "output_path": "logs/",
    },
}

class TictactoeWithSocketsTests(unittest.TestCase):
    def setUp(self):
        Config.RESTRICTIONS['write_output_files'] = False
        Config.RESTRICTIONS['novelty_archive']['samples'] = deque(maxlen=int(TEST_CONFIG['training_parameters']['populations']['teams']*1.0))

        config = dict(TEST_CONFIG)
        config['advanced_training_parameters']['diversity']['use_and_show'] = []
        config['advanced_training_parameters']['diversity']['only_show'] = []
        config['reinforcement_parameters']['hall_of_fame']['enabled'] = False
        config['reinforcement_parameters']['hall_of_fame']['opponents'] = 0
        config['reinforcement_parameters']['hall_of_fame']['diversity'] = None
        config['training_parameters']['runs_total'] = 1
        config['advanced_training_parameters']['use_operations'] = ['+', '-', '*', '/', 'if_lesser_than', 'if_equal_or_higher_than']
        config['advanced_training_parameters']['use_weighted_probability_selection'] = False
        config['advanced_training_parameters']['use_agressive_mutations'] = False
        config['advanced_training_parameters']['second_layer']['enabled'] = False
        Config.USER = config

    def test_reinforcement_for_ttt_without_pareto_and_without_diversity_maintenance_for_only_coded_opponents_for_two_runs(self):
        Config.USER['training_parameters']['runs_total'] = 2
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 2
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_without_diversity_maintenance_for_only_coded_opponents(self):
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_with_weighted_selection(self):
        Config.USER['advanced_training_parameters']['use_weighted_probability_selection'] = True
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_with_use_agressive_mutations(self):
        Config.USER['advanced_training_parameters']['use_agressive_mutations'] = True
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_with_second_layer(self):
        Config.USER['advanced_training_parameters']['second_layer']['enabled'] = True
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_without_diversity_maintenance_for_only_sbb_opponents_showing_diversity(self):
        Config.USER['advanced_training_parameters']['diversity']['only_show'] = ['genotype', 'fitness_sharing']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_genotype_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['genotype']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_sharing_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['fitness_sharing']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_entropy_c2_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['entropy_c2']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_hamming_c3_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['hamming_c3']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_ncd_c3_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['ncd_c3']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_entropy_c3_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['entropy_c3']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_ncd_c4_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['ncd_c4']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_euclidean_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['euclidean']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_with_two_diversity_maintenance(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['genotype', 'fitness_sharing']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_with_complex_instructions(self):
        Config.USER['advanced_training_parameters']['diversity']['use_and_show'] = ['ncd_c4']
        Config.USER['advanced_training_parameters']['use_operations'] = ['+', '-', '*', '/', 'ln', 'exp', 'cos', 'if_lesser_than_for_signal', 'if_equal_or_higher_than_for_signal', 'if_lesser_than', 'if_equal_or_higher_than']
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_without_diversity_maintenance_for_only_coded_opponents_with_hall_of_fame(self):
        Config.USER['reinforcement_parameters']['hall_of_fame']['enabled'] = True
        Config.USER['reinforcement_parameters']['hall_of_fame']['opponents'] = 2
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_without_diversity_maintenance_for_only_coded_opponents_with_hall_of_fame_not_used_as_opponents(self):
        Config.USER['reinforcement_parameters']['hall_of_fame']['enabled'] = True
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

    def test_reinforcement_for_ttt_without_pareto_and_without_diversity_maintenance_for_only_coded_opponents_with_hall_of_fame_with_diversity(self):
        Config.USER['reinforcement_parameters']['hall_of_fame']['enabled'] = True
        Config.USER['reinforcement_parameters']['hall_of_fame']['opponents'] = 2
        Config.USER['reinforcement_parameters']['hall_of_fame']['diversity'] = 'ncd_c4'
        sbb = SBB()
        sbb.run()
        result = len(sbb.best_scores_per_runs_)
        expected = 1
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()