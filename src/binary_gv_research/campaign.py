from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .agents import AgentError, CommandAgentProvider


N = 1_073_741_824
D = 535_822_336
CURRENT_K = 31
EPSILON_DENOMINATOR = 1_024
GV_RATE = 0.0000027517241633056023


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


PROOF_STEP = {
    "type": "object", "additionalProperties": False,
    "required": ["id", "statement", "status", "proof", "dependencies"],
    "properties": {
        "id": {"type": "string"},
        "statement": {"type": "string"},
        "status": {"type": "string", "enum": ["proved", "conditional", "conjectural", "refuted"]},
        "proof": {"type": "string"},
        "dependencies": {"type": "array", "items": {"type": "string"}},
    },
}


RESEARCH_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": [
        "title", "research_direction", "result_status", "submission_class",
        "leaderboard_submission", "baseline_beaten", "block_length", "dimension",
        "minimum_distance", "rate", "construction_markdown", "theorem_statement",
        "proof_markdown", "proof_steps", "literature_dependencies", "parameter_ledger",
        "explicitness_audit", "distance_audit", "obstructions", "next_tasks",
        "source_paths_read", "discussion_posts", "confidence",
    ],
    "properties": {
        "title": {"type": "string"},
        "research_direction": {"type": "string"},
        "result_status": {"type": "string", "enum": ["proved", "conditional", "conjectural", "refuted"]},
        "submission_class": {"type": "string", "enum": [
            "leaderboard_candidate", "baseline_improvement", "obstruction", "literature", "proof_tool"
        ]},
        "leaderboard_submission": {"type": "boolean"},
        "baseline_beaten": {"type": "boolean"},
        "block_length": {"type": ["integer", "null"]},
        "dimension": {"type": ["integer", "null"], "minimum": 0},
        "minimum_distance": {"type": ["integer", "null"], "minimum": 0},
        "rate": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
        "construction_markdown": {"type": "string"},
        "theorem_statement": {"type": "string"},
        "proof_markdown": {"type": "string"},
        "proof_steps": {"type": "array", "items": PROOF_STEP},
        "literature_dependencies": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["source", "result", "hypotheses", "used_for"],
            "properties": {
                "source": {"type": "string"}, "result": {"type": "string"},
                "hypotheses": {"type": "string"}, "used_for": {"type": "string"},
            },
        }},
        "parameter_ledger": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["quantity", "value", "derivation"],
            "properties": {
                "quantity": {"type": "string"}, "value": {"type": "string"},
                "derivation": {"type": "string"},
            },
        }},
        "explicitness_audit": {"type": "array", "items": {"type": "string"}},
        "distance_audit": {"type": "array", "items": {"type": "string"}},
        "obstructions": {"type": "array", "items": {"type": "string"}},
        "next_tasks": {"type": "array", "items": {"type": "string"}},
        "source_paths_read": {"type": "array", "items": {"type": "string"}},
        "discussion_posts": {"type": "array", "maxItems": 3, "items": {
            "type": "object", "additionalProperties": False,
            "required": ["kind", "subject", "body_markdown", "references"],
            "properties": {
                "kind": {"type": "string", "enum": ["idea", "question", "objection", "request", "reply"]},
                "subject": {"type": "string"}, "body_markdown": {"type": "string"},
                "references": {"type": "array", "items": {"type": "string"}},
            },
        }},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
    },
}


AUDIT_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["reference", "claim", "verdict", "justification"],
    "properties": {
        "reference": {"type": "string"}, "claim": {"type": "string"},
        "verdict": {"type": "string", "enum": ["valid", "gap", "false", "unclear"]},
        "justification": {"type": "string"},
    },
}


VERIFIER_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": [
        "source_job_id", "source_sha256", "verdict", "independent_review",
        "arithmetic_passed", "exact_length_passed", "distance_passed",
        "dimension_passed", "explicitness_passed", "readability_passed",
        "baseline_classification_passed", "verified_block_length", "verified_dimension",
        "verified_minimum_distance", "verified_rate", "line_audit",
        "counterexample_attempts", "fatal_obstruction", "required_changes", "summary",
    ],
    "properties": {
        "source_job_id": {"type": "string"}, "source_sha256": {"type": "string"},
        "verdict": {"type": "string", "enum": ["accept", "revise", "reject"]},
        "independent_review": {"type": "boolean"},
        "arithmetic_passed": {"type": "boolean"},
        "exact_length_passed": {"type": "boolean"},
        "distance_passed": {"type": "boolean"},
        "dimension_passed": {"type": "boolean"},
        "explicitness_passed": {"type": "boolean"},
        "readability_passed": {"type": "boolean"},
        "baseline_classification_passed": {"type": "boolean"},
        "verified_block_length": {"type": ["integer", "null"]},
        "verified_dimension": {"type": ["integer", "null"]},
        "verified_minimum_distance": {"type": ["integer", "null"]},
        "verified_rate": {"type": ["number", "null"]},
        "line_audit": {"type": "array", "items": AUDIT_ITEM},
        "counterexample_attempts": {"type": "array", "items": {"type": "string"}},
        "fatal_obstruction": {"type": ["string", "null"]},
        "required_changes": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
}


LEMMA_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["coverage_complete", "source_jobs", "lemmas"],
    "properties": {
        "coverage_complete": {"type": "boolean"},
        "source_jobs": {"type": "array", "items": {"type": "string"}},
        "lemmas": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "title", "statement_markdown", "proof_markdown", "status", "dependencies", "source_refs"],
            "properties": {
                "id": {"type": "string"}, "title": {"type": "string"},
                "statement_markdown": {"type": "string"}, "proof_markdown": {"type": "string"},
                "status": {"type": "string", "enum": ["proved", "conditional", "conjectural", "refuted"]},
                "dependencies": {"type": "array", "items": {"type": "string"}},
                "source_refs": {"type": "array", "items": {"type": "string"}},
            },
        }},
    },
}


ROADMAP_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["roadmap_id", "title", "target_statement", "summary", "progress", "nodes", "critical_path", "messages"],
    "properties": {
        "roadmap_id": {"type": "string"}, "title": {"type": "string"},
        "target_statement": {"type": "string"}, "summary": {"type": "string"},
        "progress": {"type": "number", "minimum": 0, "maximum": 1},
        "nodes": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "statement_markdown", "status", "dependencies", "evidence_refs", "notes"],
            "properties": {
                "id": {"type": "string"}, "statement_markdown": {"type": "string"},
                "status": {"type": "string", "enum": ["proved", "conditional", "conjectural", "refuted", "open"]},
                "dependencies": {"type": "array", "items": {"type": "string"}},
                "evidence_refs": {"type": "array", "items": {"type": "string"}},
                "notes": {"type": "string"},
            },
        }},
        "critical_path": {"type": "array", "items": {"type": "string"}},
        "messages": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["kind", "subject", "body_markdown", "references"],
            "properties": {
                "kind": {"type": "string", "enum": ["idea", "question", "objection", "request", "reply"]},
                "subject": {"type": "string"}, "body_markdown": {"type": "string"},
                "references": {"type": "array", "items": {"type": "string"}},
            },
        }},
    },
}


GENIUS_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": [
        "title", "coverage_complete", "examined_paths", "best_verified_candidate",
        "best_promising_candidate", "baseline_analysis", "selected_architecture",
        "leaderboard_plan", "integrated_theorem", "proof_steps", "fatal_gaps",
        "research_directives", "note_markdown",
    ],
    "properties": {
        "title": {"type": "string"}, "coverage_complete": {"type": "boolean"},
        "examined_paths": {"type": "array", "items": {"type": "string"}},
        "best_verified_candidate": {"type": ["string", "null"]},
        "best_promising_candidate": {"type": ["string", "null"]},
        "baseline_analysis": {"type": "string"}, "selected_architecture": {"type": ["string", "null"]},
        "leaderboard_plan": {"type": "string"}, "integrated_theorem": {"type": "string"},
        "proof_steps": {"type": "array", "items": PROOF_STEP},
        "fatal_gaps": {"type": "array", "items": {"type": "string"}},
        "research_directives": {"type": "array", "items": {"type": "string"}},
        "note_markdown": {"type": "string"},
    },
}


TEAM_DIRECTIONS = {
    "algebraic": [
        "Trace and character-sum codes.", "Subfield subcodes and concatenation.",
        "Algebraic-geometric evaluation codes.", "BCH and cyclic-code bias bounds.",
        "Reed--Muller extensions.", "Tensor and product constructions.",
        "Boolean polynomial constructions.", "Explicit Fourier-bias calculations.",
        "Finite-field lifting and descent.", "Exact parameter optimization of algebraic routes.",
    ],
    "combinatorial": [
        "Explicit small-bias generators.", "Epsilon-balanced code instantiations.",
        "Expander-walk codes.", "Replacement-product constructions.",
        "Extractor-based linear codes.", "Derandomized sampler constructions.",
        "Cayley graph and character constructions.", "Spectral amplification.",
        "Limited-independence constructions.", "Finite constant optimization of combinatorial routes.",
    ],
    "combinatorial-expander": [
        "Ta-Shma-style epsilon-balanced codes and their exact finite instantiation.",
        "Ta-Shma bias amplification with every constant exposed.",
        "Wide replacement products and Gray-code constructions.",
        "Expander-walk and free-walk balanced codes.",
        "Replacement-product parameter optimization at epsilon=2^-10.",
        "Lossless-expander and sampler-based constructions.",
        "Spectral graph products and explicit bias reduction.",
        "Extractor-based balanced codes with concrete length accounting.",
        "Derandomized low-bias code constructions and finite losses.",
        "Synthesize the strongest combinatorial-expander record candidate.",
    ],
    "composition": [
        "Multilevel concatenation.", "Structured inner-code search with proofs.",
        "Outer-code and alphabet-reduction tradeoffs.", "Direct sums and interleavings.",
        "Puncturing, shortening, and padding arithmetic.", "Code product transformations.",
        "Hybrid algebraic-combinatorial constructions.", "Exact finite-length rounding optimization.",
        "Audit of known explicit constructions at the checkpoint.", "Synthesis of reusable lemmas into a higher-k candidate.",
    ],
}


ROADMAPS = {
    "roadmap-algebraic": "Trace, character-sum, subfield-subcode, and algebraic routes maximizing concrete dimension at bias 2^-10.",
    "roadmap-expander": "Explicit epsilon-balanced and expander-walk routes with finite constants optimized at epsilon=2^-10.",
    "roadmap-composition": "Structured concatenation, multilevel, and finite parameter-search routes maximizing the certified dimension at the exact target.",
}


BASE_SPEC = r"""
The immutable target is an explicit binary linear code C subset F_2^n with
n=2^30=1,073,741,824 and epsilon=2^-10.  It must satisfy
d_min(C)>=535,822,336=(1/2-2^-10)n.  The sole operating objective is to
maximize the rigorously proved dimension k=dim(C), equivalently rate R=k/n,
at this exact target. The current verified dimension is 31, so a new record needs
dimension at least 32; the concrete GV-rate reference corresponds to dimension
2,955. Every decision, roadmap, and synthesis must be judged first by whether
it can yield a larger verified k. Random sampling is not an
admissible construction.  Every field, code, tower level, divisor, graph,
ordering, shortening, puncturing, and padding choice must be deterministic and
symbolically recoverable.  Distance must be proved for every nonzero codeword.

Asymptotic insights are useful only when they supply a concrete symbolic code
or a finite lemma that can improve this leaderboard. Do not spend a campaign
turn proving a general family unless its exact n=2^30 specialization improves
the best available certified dimension.
"""


@dataclass(frozen=True)
class Paths:
    config: Path
    workspace: Path
    campaign_dir: Path


def load_config(config_path: Path | str) -> tuple[dict[str, Any], Paths]:
    path = Path(config_path).resolve()
    value = yaml.safe_load(path.read_text())
    if not isinstance(value, dict) or not isinstance(value.get("campaign"), dict):
        raise ValueError("config must contain a campaign mapping")
    cfg = value["campaign"]
    if cfg.get("reasoning_effort") != "ultra":
        raise ValueError("campaign.reasoning_effort must be ultra")
    if int(cfg.get("researcher_count", 0)) != 40:
        raise ValueError("the campaign must have four groups of ten researchers")
    if int(cfg.get("verifier_count", 0)) != 1:
        raise ValueError("every submission must receive exactly one independent review")
    if int(cfg.get("roadmap_count", 0)) < 3:
        raise ValueError("at least three proof roadmaps are required")
    if int(cfg.get("block_length", 0)) != N or int(cfg.get("minimum_distance", 0)) != D:
        raise ValueError("fixed target parameters changed")
    base = path.parent
    workspace = (base / str(value.get("workspace", ".."))).resolve()
    campaign_dir = (base / str(value.get("campaign_dir", "../research_state/campaign-epsilon-2-10-ultra"))).resolve()
    return value, Paths(path, workspace, campaign_dir)


class Campaign:
    def __init__(self, config_path: Path | str):
        self.config, self.paths = load_config(config_path)
        self.cfg = self.config["campaign"]
        self.root = self.paths.campaign_dir
        self.jobs_path = self.root / "jobs.json"
        self.provider = CommandAgentProvider(
            self.paths.workspace, self.root / "agent_logs",
            str(self.cfg.get("executable", "codex")),
            str(self.cfg.get("model", "gpt-5.6-sol")), "ultra",
            int(self.cfg.get("timeout_seconds", 5400)),
            bool(self.cfg.get("disable_nested_agents", True)),
        )

    def _read_jobs(self) -> list[dict[str, Any]]:
        return json.loads(self.jobs_path.read_text()) if self.jobs_path.exists() else []

    def _write_jobs(self, jobs: list[dict[str, Any]]) -> None:
        temp = self.jobs_path.with_suffix(".tmp")
        temp.write_text(json.dumps(jobs, indent=2, sort_keys=True) + "\n")
        temp.replace(self.jobs_path)

    def initialize(self) -> dict[str, Any]:
        for name in ("submissions", "reviews", "lemma_book", "roadmaps", "genius", "metadata", "message_board"):
            (self.root / name).mkdir(parents=True, exist_ok=True)
        if self.jobs_path.exists():
            return self.status()
        jobs: list[dict[str, Any]] = []
        for team, directions in TEAM_DIRECTIONS.items():
            for index, direction in enumerate(directions, start=1):
                jobs.append(self._job(
                    f"{team}-{index:02d}", "researcher", direction, team=team, round_number=1))
        if self.cfg.get("literature_agent_enabled", True):
            jobs.append(self._job(
                "literature-sota-0001", "literature",
                "Audit explicit epsilon-balanced-code literature and extract the strongest finite constants and parameter choices for a larger dimension at epsilon=2^-10.",
                team="shared", round_number=1))
        for job_id, focus in ROADMAPS.items():
            jobs.append(self._job(job_id, "roadmap", focus, phase="synthesis", team="shared", round_number=1))
        if self.cfg.get("lemma_writer_enabled", True):
            jobs.append(self._job("lemma-writer-0001", "lemma_writer", "Edit all reusable proof steps into the shared lemma book.", phase="synthesis", team="shared", round_number=1))
        if self.cfg.get("genius_enabled", True):
            jobs.append(self._job("GENIUS", "genius", "Construct the highest-dimension exact leaderboard candidate from all campaign evidence.", phase="genius", team="shared", round_number=1))
        self._write_jobs(jobs)
        return self.status()

    def add_researchers(self, count: int) -> dict[str, Any]:
        """Append ultra-reasoning researcher seats to a live durable queue."""
        if count < 1:
            raise ValueError("count must be positive")
        self.initialize()
        jobs = self._read_jobs()
        existing = {job["id"] for job in jobs}
        ordinal = 1
        while f"researcher-{ordinal:04d}" in existing:
            ordinal += 1
        for _ in range(count):
            while f"researcher-{ordinal:04d}" in existing:
                ordinal += 1
            job_id = f"researcher-{ordinal:04d}"
            team_names = tuple(TEAM_DIRECTIONS)
            team = team_names[(ordinal - 1) % len(team_names)]
            direction = TEAM_DIRECTIONS[team][(ordinal - 1) % len(TEAM_DIRECTIONS[team])]
            jobs.append(self._job(job_id, "researcher", direction, team=team, round_number=2))
            existing.add(job_id)
            ordinal += 1
        self._write_jobs(jobs)
        return self.status()

    def add_team(self, team: str) -> dict[str, Any]:
        """Append one named ten-agent research team without restarting the campaign."""
        if team not in TEAM_DIRECTIONS:
            raise ValueError(f"unknown team: {team}")
        self.initialize()
        jobs = self._read_jobs()
        prefix = f"{team}-"
        if any(job["id"].startswith(prefix) for job in jobs):
            raise ValueError(f"team already exists: {team}")
        round_number = max((int(job.get("round", 1)) for job in jobs), default=1)
        for index, direction in enumerate(TEAM_DIRECTIONS[team], start=1):
            jobs.append(self._job(
                f"{team}-{index:02d}", "researcher", direction,
                team=team, round_number=round_number))
        self._write_jobs(jobs)
        return self.status()

    def _job(self, job_id: str, role: str, direction: str, phase: str = "research",
             dependency: str | None = None, team: str = "shared", round_number: int = 1) -> dict[str, Any]:
        return {
            "id": job_id, "role": role, "direction": direction, "phase": phase,
            "dependency": dependency, "status": "queued", "attempts": 0,
            "team": team, "round": round_number,
            "model": self.cfg.get("model", "gpt-5.6-sol"),
            "reasoning_effort": "ultra", "error": None,
            "created_at": utc_timestamp(), "updated_at": utc_timestamp(),
        }

    def _submission_paths(self) -> list[str]:
        return [str(path.relative_to(self.paths.workspace)) for path in sorted((self.root / "submissions").glob("*.json"))]

    def _review_paths(self) -> list[str]:
        return [str(path.relative_to(self.paths.workspace)) for path in sorted((self.root / "reviews").glob("**/*.json"))]

    def _prompt(self, job: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        role = job["role"]
        if role in {"researcher", "literature"}:
            seat = "state-of-the-art literature analyst" if role == "literature" else "independent construction researcher"
            prompt = f"""You are {job['id']}, an {seat} in the Binary-GV Concrete campaign.
You run at ultra reasoning. Read AGENTS.md, TARGET.md, the contribution guide,
the RM baseline proof, and data/records.json before reasoning.

{BASE_SPEC}

YOUR FOCUSED DIRECTION:
{job['direction']}

TEAM: {job.get('team', 'shared')}; ROUND: {job.get('round', 1)}.
Before reasoning, read the durable submissions, lemma book, roadmaps, and every
file in the shared message_board directory. Use another team's proved lemma
when it helps. At the end, put up to three concise, substantive posts in
discussion_posts: a reusable lemma, a precise obstacle, or a concrete question
for other teams. Do not post social updates or unsupported claims.

Produce genuine mathematical work.  A leaderboard_submission=true response must
contain a complete deterministic construction and an academic proof that checks
binary linearity, exact length, integer dimension, minimum distance, and every
finite parameter.  Do not use random existence, sampled codewords, hidden
O-constants, or an unavailable theorem.  Set leaderboard_submission=false when
any essential step is conditional.  State concise lemmas; put explanations in
their proofs.  You may report a rigorous obstruction lemma when no
candidate survives.  Rate must equal dimension/1,073,741,824 exactly up to JSON
number precision. baseline_beaten is true only if the proved dimension is
strictly greater than 31 at the immutable near-half-distance target.
"""
            return prompt, RESEARCH_SCHEMA
        if role == "verifier":
            source_id = str(job["dependency"])
            source_path = self.root / "submissions" / f"{source_id}.json"
            source = json.loads(source_path.read_text())
            prompt = f"""You are {job['id']}, the independent mathematical reviewer.
Read and audit {source_path.relative_to(self.paths.workspace)} line by line.

{BASE_SPEC}

The immutable source SHA-256 is {canonical_hash(source)}.  Recompute every
integer and verify every cited theorem's hypotheses, exact-length operation,
dimension claim, and minimum-distance implication.  Try to break the construction
with edge cases and low-weight words. Check whether its baseline-improvement
classification is honest. Reject an unfixable false or inadmissible claim; request revision for
a local gap; accept a correct proof written clearly enough for an ordinary
mathematical reader.  Do not reject for ceremonial or proof-assistant-level
formalism.  Set source_job_id and source_sha256 exactly.
"""
            return prompt, VERIFIER_SCHEMA
        if role == "lemma_writer":
            paths = self._submission_paths()
            prompt = f"""You are the dedicated Lemma Writer for Binary-GV Concrete.
Read every source listed below and post-edit all reusable proof steps.

{BASE_SPEC}

RULE: A lemma statement contains only quantified objects, hypotheses, and its
conclusion.  It contains no motivation, derivation, commentary, proof sketch,
interpretation, history, or explanation; put all such material in the proof.
Preserve mathematical status and content.  You may split a lemma into ordered
pieces when that materially improves comprehension.  Use KaTeX-compatible LaTeX
inside math delimiters and omit no substantive proved step.  Source paths:
{json.dumps(paths, indent=2)}
"""
            return prompt, LEMMA_SCHEMA
        if role == "roadmap":
            prompt = f"""You are {job['id']}, one of three parallel proof-roadmap mathematicians.
All campaign work is shared, but prefer the assigned focus below.

{BASE_SPEC}

ASSIGNED FOCUS: {job['direction']}
Read all JSON submissions in {self.root.relative_to(self.paths.workspace)}/submissions
and all available reviews in {self.root.relative_to(self.paths.workspace)}/reviews.
Build a concise but complete dependency chain, similar to a Lean theorem graph,
ending in an exact code at n=2^30 with distance at least 535,822,336 and an
improved certified rate. Mark what is
proved, conditional, refuted, or open; never promote a conjecture.  Cite source
paths for reused lemmas.  Post useful informal questions, objections, and ideas
in messages so the other roadmaps and GENIUS can use them.  Set roadmap_id to
{job['id']}.
"""
            return prompt, ROADMAP_SCHEMA
        if role == "genius":
            prompt = f"""You are GENIUS, the final global synthesis mathematician.
Read every durable file under {self.root.relative_to(self.paths.workspace)},
including all submissions, both independent reviews, the lemma book, and all
three roadmaps.  Read the repository baselines and literature map too.

{BASE_SPEC}

Attempt to construct the highest-dimension exact code at n=2^30 and
epsilon=2^-10 by combining only compatible proved components. Maximizing the
leaderboard dimension is the main architectural goal.
Do not fill gaps by optimism. Distinguish verified facts,
conditional components, refutations, and new conjectures.  If a complete
complete target proof is unavailable, identify the narrowest decisive missing
lemma and give concrete research directives.  coverage_complete=true only after
you have examined every durable response and review path.
"""
            return prompt, GENIUS_SCHEMA
        raise ValueError(f"unknown role: {role}")

    def _output_path(self, job: dict[str, Any]) -> Path:
        if job["role"] in {"researcher", "literature"}:
            return self.root / "submissions" / f"{job['id']}.json"
        if job["role"] == "verifier":
            target = self.root / "reviews" / str(job["dependency"])
            target.mkdir(parents=True, exist_ok=True)
            return target / f"{job['id']}.json"
        if job["role"] == "lemma_writer":
            return self.root / "lemma_book" / "lemma-book.json"
        if job["role"] == "roadmap":
            return self.root / "roadmaps" / f"{job['id']}.json"
        return self.root / "genius" / "GENIUS.json"

    def _run_job(self, job: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        prompt, schema = self._prompt(job)
        response, metadata = self.provider.run(job["id"], prompt, schema)
        output = self._output_path(job)
        output.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n")
        posts = response.get("discussion_posts")
        if not isinstance(posts, list) and job["role"] == "roadmap":
            posts = response.get("messages")
        if isinstance(posts, list) and posts:
            payload = {
                "job_id": job["id"], "team": job.get("team", "shared"),
                "round": job.get("round", 1), "created_at": utc_timestamp(), "posts": posts,
            }
            board_path = self.root / "message_board" / f"{job['id']}.json"
            board_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        metadata["durable_output"] = str(output)
        (self.root / "metadata" / f"{job['id']}.json").write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n")
        return response, metadata

    def _run_phase(self, roles: set[str]) -> None:
        max_attempts = int(self.cfg.get("max_attempts", 3))
        while True:
            jobs = self._read_jobs()
            selected = [job for job in jobs if job["role"] in roles and job["status"] in {"queued", "failed"} and int(job["attempts"]) < max_attempts]
            if not selected:
                return
            selected_ids = {job["id"] for job in selected}
            for job in jobs:
                if job["id"] in selected_ids:
                    job["status"] = "running"
                    job["attempts"] = int(job["attempts"]) + 1
                    job["updated_at"] = utc_timestamp()
            self._write_jobs(jobs)
            with ThreadPoolExecutor(max_workers=int(self.cfg.get("max_workers", 3))) as pool:
                futures = {pool.submit(self._run_job, job): job["id"] for job in selected}
                for future in as_completed(futures):
                    job_id = futures[future]
                    jobs = self._read_jobs()
                    target = next(job for job in jobs if job["id"] == job_id)
                    try:
                        future.result()
                        target["status"] = "succeeded"
                        target["error"] = None
                    except Exception as exc:  # retain errors for durable retry
                        target["status"] = "failed"
                        target["error"] = str(exc)
                    target["updated_at"] = utc_timestamp()
                    self._write_jobs(jobs)
                    self.export_snapshot()
                    # Make every durable result visible to collaborators as soon
                    # as the job finishes. This is best-effort and never turns a
                    # successful mathematical job into a failed one if GitHub
                    # authentication or connectivity is temporarily unavailable.
                    self._sync_git(f"{job_id} completed")
                    if target["role"] == "researcher":
                        # A complete candidate enters its one-review gate as soon
                        # as its durable submission is available; it never waits
                        # for the rest of the research round.
                        self._queue_verifiers()
                        self._run_phase({"verifier"})
            if any(job["status"] == "failed" and int(job["attempts"]) < max_attempts for job in self._read_jobs() if job["role"] in roles):
                time.sleep(min(int(self.cfg.get("retry_seconds", 120)), 30))

    def _sync_git(self, reason: str) -> None:
        """Commit and push durable campaign state without touching user files.

        Agent traces, caches, and the runner PID are intentionally ignored. Only
        machine-readable submissions, metadata, reviews, synthesis artifacts,
        and progress snapshots are synchronized. A pre-existing staged change
        causes a skip, so an in-progress collaborator commit is never folded into
        an automated campaign commit.
        """
        if not self.cfg.get("auto_sync_git", False):
            return
        try:
            # Do not interfere with a human's staged work.
            staged = subprocess.run(
                ["git", "diff", "--cached", "--quiet"], cwd=self.paths.workspace,
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False,
            )
            if staged.returncode != 0:
                return
            durable = [
                self.root / "jobs.json", self.root / "snapshot.json", self.root / "status.json",
                *sorted((self.root / "metadata").glob("*.json")),
                *sorted((self.root / "submissions").glob("*.json")),
                *sorted((self.root / "reviews").glob("**/*.json")),
                *sorted((self.root / "lemma_book").glob("*.json")),
                *sorted((self.root / "roadmaps").glob("*.json")),
                *sorted((self.root / "genius").glob("*.json")),
                *sorted((self.root / "message_board").glob("*.json")),
            ]
            existing = [path for path in durable if path.exists()]
            if not existing:
                return
            relative = [str(path.relative_to(self.paths.workspace)) for path in existing]
            add = subprocess.run(
                ["git", "add", "--", *relative], cwd=self.paths.workspace,
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=False,
            )
            if add.returncode != 0:
                return
            staged_paths = subprocess.run(
                ["git", "diff", "--cached", "--name-only"], cwd=self.paths.workspace,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
            ).stdout.splitlines()
            allowed = set(relative)
            if not set(staged_paths).issubset(allowed):
                # This should only be reachable if another process staged files
                # between the checks; leave the index untouched for the author.
                return
            if not staged_paths:
                return
            message = "Sync Binary GV campaign: " + reason
            commit = subprocess.run(
                ["git", "commit", "-m", message], cwd=self.paths.workspace,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
            )
            if commit.returncode != 0:
                return
            remote = str(self.cfg.get("git_remote", "origin"))
            branch = str(self.cfg.get("git_branch", "main"))
            subprocess.run(
                ["git", "push", remote, branch], cwd=self.paths.workspace,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
            )
        except OSError:
            # Synchronization is auxiliary; the local campaign remains durable.
            return

    def _queue_verifiers(self) -> None:
        jobs = self._read_jobs()
        existing = {job["id"] for job in jobs}
        for source_path in sorted((self.root / "submissions").glob("*.json")):
            source = json.loads(source_path.read_text())
            if not source.get("leaderboard_submission"):
                continue
            source_id = source_path.stem
            for index in range(1, int(self.cfg["verifier_count"]) + 1):
                job_id = f"verifier-{index}-{source_id}"
                if job_id not in existing:
                    jobs.append(self._job(job_id, "verifier", "Independent line-by-line proof audit.", phase="verification", dependency=source_id))
                    existing.add(job_id)
        self._write_jobs(jobs)

    def _has_verified_improvement(self) -> bool:
        for source_path in (self.root / "submissions").glob("*.json"):
            source = json.loads(source_path.read_text())
            if (
                not source.get("leaderboard_submission")
                or not isinstance(source.get("dimension"), int)
                or source["dimension"] <= CURRENT_K
                or source.get("block_length") != N
                or source.get("minimum_distance", 0) < D
            ):
                continue
            reviews = self.root / "reviews" / source_path.stem
            accepted = 0 if not reviews.exists() else sum(
                json.loads(path.read_text()).get("verdict") == "accept"
                for path in reviews.glob("*.json")
            )
            if accepted >= int(self.cfg["verifier_count"]):
                return True
        return False

    def _queue_next_research_round(self) -> None:
        jobs = self._read_jobs()
        next_round = max((int(job.get("round", 1)) for job in jobs), default=0) + 1
        for team, directions in TEAM_DIRECTIONS.items():
            for index, direction in enumerate(directions, start=1):
                jobs.append(self._job(
                    f"{team}-r{next_round:03d}-{index:02d}", "researcher", direction,
                    team=team, round_number=next_round))
        for roadmap_id, focus in ROADMAPS.items():
            jobs.append(self._job(
                f"{roadmap_id}-r{next_round:03d}", "roadmap", focus, phase="synthesis",
                team="shared", round_number=next_round))
        jobs.append(self._job(
            f"lemma-writer-r{next_round:03d}", "lemma_writer",
            "Merge the newest reusable proof steps into the shared lemma book.", phase="synthesis",
            team="shared", round_number=next_round))
        jobs.append(self._job(
            f"GENIUS-r{next_round:03d}", "genius",
            "Synthesize the highest-dimension exact candidate from all shared evidence.", phase="genius",
            team="shared", round_number=next_round))
        self._write_jobs(jobs)

    def export_snapshot(self) -> dict[str, Any]:
        if not self.jobs_path.exists():
            return self.initialize()
        jobs = self._read_jobs()
        candidates = []
        verified = []
        for source_path in sorted((self.root / "submissions").glob("*.json")):
            source = json.loads(source_path.read_text())
            source_id = source_path.stem
            if not source.get("leaderboard_submission") and source.get("result_status") not in {"proved", "conditional"}:
                continue
            reviews = []
            review_dir = self.root / "reviews" / source_id
            if review_dir.exists():
                reviews = [json.loads(path.read_text()) for path in sorted(review_dir.glob("*.json"))]
            item = {
                "id": source_id, "title": source.get("title"), "status": source.get("result_status"),
                "submission_class": source.get("submission_class"), "dimension": source.get("dimension"),
                "minimum_distance": source.get("minimum_distance"), "rate": source.get("rate"),
                "baseline_beaten": source.get("baseline_beaten"),
                "accepted_reviews": sum(review.get("verdict") == "accept" for review in reviews),
                "source_path": str(source_path.relative_to(self.paths.workspace)),
            }
            candidates.append(item)
            if (
                source.get("leaderboard_submission") and item["accepted_reviews"] >= int(self.cfg["verifier_count"])
                and source.get("block_length") == N
                and isinstance(source.get("dimension"), int)
                and source.get("minimum_distance", 0) >= D
            ):
                verified.append(item)
        candidates.sort(key=lambda item: item.get("rate") or -1, reverse=True)
        verified.sort(key=lambda item: item.get("rate") or -1, reverse=True)
        counts: dict[str, int] = {}
        for job in jobs:
            counts[job["status"]] = counts.get(job["status"], 0) + 1
        payload = {
            "schema": "binary-gv-campaign-snapshot-v1", "updated_at": utc_timestamp(),
            "model": self.cfg.get("model"), "reasoning_effort": "ultra",
            "researcher_count": sum(job["role"] == "researcher" for job in jobs), "counts": counts,
            "target": {
                "block_length": N,
                "minimum_distance": D,
                "current_dimension": CURRENT_K,
                "epsilon": "2^-10",
                "relative_distance": "511/1024",
                "gv_rate": GV_RATE,
                "gv_dimension_threshold": 2_955,
            },
            "leaderboard_objective": {
                "maximize": "certified_dimension",
                "current_verified_dimension": CURRENT_K,
                "gv_dimension_reference": 2_955,
                "minimum_distance": D,
            },
            "message_board": self._message_board_snapshot(),
            "promising_candidates": candidates, "doubly_verified_candidates": verified,
        }
        (self.root / "snapshot.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        (self.root / "status.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return payload

    def _message_board_snapshot(self) -> dict[str, Any]:
        posts: list[dict[str, Any]] = []
        for path in sorted((self.root / "message_board").glob("*.json")):
            try:
                entry = json.loads(path.read_text())
            except json.JSONDecodeError:
                continue
            for post in entry.get("posts", []):
                if isinstance(post, dict):
                    posts.append({
                        "job_id": entry.get("job_id"), "team": entry.get("team"),
                        "round": entry.get("round"), **post,
                    })
        return {"post_count": len(posts), "recent_posts": posts[-12:]}

    def status(self) -> dict[str, Any]:
        if not self.jobs_path.exists():
            return self.initialize()
        return self.export_snapshot()

    def run(self) -> dict[str, Any]:
        self.initialize()
        completed_rounds = 0
        round_limit = int(self.cfg.get("max_improvement_rounds", 0))
        while not self._has_verified_improvement():
            self._run_phase({"researcher", "literature"})
            self._queue_verifiers()
            self._run_phase({"verifier"})
            self._run_phase({"lemma_writer", "roadmap"})
            self._run_phase({"genius"})
            if self._has_verified_improvement():
                break
            completed_rounds += 1
            if round_limit and completed_rounds >= round_limit:
                break
            self._queue_next_research_round()
        return self.export_snapshot()


def launch_campaign(config_path: Path | str) -> dict[str, Any]:
    _, paths = load_config(config_path)
    paths.campaign_dir.mkdir(parents=True, exist_ok=True)
    runner_path = paths.campaign_dir / "runner.json"
    if runner_path.exists():
        try:
            old = json.loads(runner_path.read_text())
            os.kill(int(old["pid"]), 0)
            return {"status": "already_running", **old}
        except (OSError, KeyError, ValueError, json.JSONDecodeError):
            pass
    log_path = paths.campaign_dir / "campaign.log"
    log_handle = log_path.open("a")
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(paths.workspace / "src")
    environment["PYTHONPYCACHEPREFIX"] = str(paths.campaign_dir / "python-cache")
    process = subprocess.Popen(
        [sys.executable, "-m", "binary_gv_research", "run", str(Path(config_path).resolve())],
        cwd=paths.workspace, stdout=log_handle, stderr=subprocess.STDOUT,
        text=True, start_new_session=True, env=environment,
    )
    log_handle.close()
    payload = {
        "status": "launched", "pid": process.pid, "started_at": utc_timestamp(),
        "config": str(Path(config_path).resolve()), "log": str(log_path),
        "model": "gpt-5.6-sol", "reasoning_effort": "ultra",
    }
    runner_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload
