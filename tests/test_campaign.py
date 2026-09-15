import tempfile
import unittest
from pathlib import Path

from binary_gv_research.agents import CommandAgentProvider
from binary_gv_research.campaign import D, GV_RATE, load_config


ROOT = Path(__file__).resolve().parents[1]


class CampaignTests(unittest.TestCase):
    def test_campaign_is_ultra_and_fixed_target(self):
        config, _ = load_config(ROOT / "configs" / "campaign-epsilon-2-10-ultra.yaml")
        self.assertEqual(config["campaign"]["reasoning_effort"], "ultra")
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


if __name__ == "__main__":
    unittest.main()
