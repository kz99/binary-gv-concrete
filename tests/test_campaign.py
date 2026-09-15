import tempfile
import unittest
from pathlib import Path

from binary_gv_research.agents import CommandAgentProvider
from binary_gv_research.campaign import Campaign, D, GV_RATE, RESEARCHER_EFFORTS, load_config


ROOT = Path(__file__).resolve().parents[1]


class CampaignTests(unittest.TestCase):
    def test_campaign_is_ultra_and_fixed_target(self):
        config, _ = load_config(ROOT / "configs" / "campaign-epsilon-2-10-ultra.yaml")
        self.assertEqual(config["campaign"]["reasoning_effort"], "ultra")
        self.assertEqual(config["campaign"]["verifier_reasoning_effort"], "xhigh")
        self.assertEqual(tuple(config["campaign"]["researcher_reasoning_efforts"]), RESEARCHER_EFFORTS)
        self.assertEqual(config["campaign"]["synthesis_reasoning_effort"], "xhigh")
        self.assertFalse(config["campaign"]["genius_enabled"])
        self.assertTrue(config["campaign"]["require_polynomial_generator_matrix"])
        self.assertEqual(config["campaign"]["researcher_count"], 40)
        self.assertEqual(config["campaign"]["block_length"], 2**30)
        self.assertEqual(config["campaign"]["minimum_distance"], 2**29 - 2**20)
        self.assertEqual(D, 2**29 - 2**20)
        self.assertEqual(config["campaign"]["epsilon_denominator"], 1024)
        self.assertEqual(config["campaign"]["verifier_count"], 1)
        self.assertTrue(config["campaign"]["auto_sync_git"])
        self.assertGreater(GV_RATE, 0)

    def test_agent_command_hard_codes_ultra(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            provider = CommandAgentProvider(
                ROOT, root, "codex", "gpt-5.6-sol", "ultra", 10)
            command = provider.command(root / "schema.json", root / "response.json")
            self.assertIn('model_reasoning_effort="ultra"', command)
            self.assertIn("multi_agent", command)

    def test_verifier_command_can_use_extra_high(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            provider = CommandAgentProvider(
                ROOT, root, "codex", "gpt-5.6-sol", "ultra", 10)
            command = provider.command(root / "schema.json", root / "response.json", "xhigh")
            self.assertIn('model_reasoning_effort="xhigh"', command)

    def test_only_polynomial_generator_certificates_are_eligible(self):
        valid = {
            "generator_matrix": {
                "outputs_full_matrix_in_polynomial_time": True,
                "algorithm": "Emit entries in lexicographic order.",
                "runtime_bound": "O(n^2)",
                "runtime_proof": "There are O(n^2) entries.",
            },
        }
        self.assertTrue(Campaign._has_polynomial_generator(valid))
        self.assertFalse(Campaign._has_polynomial_generator({}))

    def test_research_team_mixes_three_reasoning_levels(self):
        campaign = Campaign(ROOT / "configs" / "campaign-epsilon-2-10-ultra.yaml")
        efforts = [campaign._job_effort(f"team-{index:02d}", "researcher") for index in range(1, 11)]
        self.assertEqual(efforts, list(RESEARCHER_EFFORTS))
        self.assertEqual(campaign._job_effort("GENIUS", "genius"), "ultra")
        self.assertEqual(campaign._job_effort("roadmap-expander", "roadmap"), "xhigh")

    def test_researcher_prompt_has_explicitness_mandate(self):
        campaign = Campaign(ROOT / "configs" / "campaign-epsilon-2-10-ultra.yaml")
        job = campaign._job("algebraic-01", "researcher", "test direction", team="algebraic")
        prompt, _ = campaign._prompt(job)
        self.assertIn("polynomial-time", prompt)


if __name__ == "__main__":
    unittest.main()
