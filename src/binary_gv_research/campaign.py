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
D = 469_762_048
CURRENT_K = 3_688_448
CEILING_RATE = 7 / 1920


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
        "leaderboard_submission", "ceiling_beaten", "block_length", "dimension",
        "minimum_distance", "rate", "construction_markdown", "theorem_statement",
        "proof_markdown", "proof_steps", "literature_dependencies", "parameter_ledger",
        "explicitness_audit", "distance_audit", "obstructions", "next_tasks",
        "source_paths_read", "confidence",
    ],
    "properties": {
        "title": {"type": "string"},
        "research_direction": {"type": "string"},
        "result_status": {"type": "string", "enum": ["proved", "conditional", "conjectural", "refuted"]},
        "submission_class": {"type": "string", "enum": [
            "ceiling_optimization", "beyond_ceiling", "obstruction", "literature", "proof_tool"
        ]},
        "leaderboard_submission": {"type": "boolean"},
        "ceiling_beaten": {"type": "boolean"},
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
        "ceiling_classification_passed", "verified_block_length", "verified_dimension",
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
        "ceiling_classification_passed": {"type": "boolean"},
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
        "best_promising_candidate", "ceiling_analysis", "selected_architecture",
        "asymptotic_family", "integrated_theorem", "proof_steps", "fatal_gaps",
        "research_directives", "note_markdown",
    ],
    "properties": {
        "title": {"type": "string"}, "coverage_complete": {"type": "boolean"},
        "examined_paths": {"type": "array", "items": {"type": "string"}},
        "best_verified_candidate": {"type": ["string", "null"]},
        "best_promising_candidate": {"type": ["string", "null"]},
        "ceiling_analysis": {"type": "string"}, "selected_architecture": {"type": ["string", "null"]},
        "asymptotic_family": {"type": "string"}, "integrated_theorem": {"type": "string"},
        "proof_steps": {"type": "array", "items": PROOF_STEP},
        "fatal_gaps": {"type": "array", "items": {"type": "string"}},
        "research_directives": {"type": "array", "items": {"type": "string"}},
        "note_markdown": {"type": "string"},
    },
}


DIRECTIONS = [
    "Optimize the exact finite n=2^30 GS(F_256)+RM(1,7) construction up to its vanilla 7/1920 asymptotic envelope; prove every tower, divisor, floor, and padding choice and quantify the remaining finite-size loss.",
    "Prove and audit the GS+Hadamard template ceiling over every even extension degree m, then identify the weakest hypothesis whose replacement could permit rate greater than 7/1920.",
    "Find an explicit binary inner code or structured family that changes the one-level concatenation optimization enough to beat 7/1920, and instantiate it exactly at n=2^30.",
    "Develop a multilevel or generalized concatenation construction that provably crosses 7/1920 while keeping a human-readable minimum-distance proof.",
    "Use trace codes, subfield subcodes, or algebraic alphabet reduction to retain more of a GS outer code's dimension than Hadamard concatenation and prove the exact binary parameters.",
    "Instantiate an epsilon-balanced or expander-amplified explicit construction at epsilon=1/8 and n=2^30, exposing all constants and exact shortening or padding losses.",
    "Investigate deterministic replacements for random inner codes in low-rate concatenation theorems; produce a symbolic constituent and a proof, not a sampling argument.",
    "Search alternative explicit AG towers, divisors, or algebraic code operations whose binary reduction escapes the vanilla GS+Hadamard rate formula.",
    "Combine explicit base codes with expander distance amplification or direct-sum/product operations to cross 7/1920 at exact length, proving the weight propagation lemma.",
    "Synthesize reusable proved lemmas from the repository into a genuinely beyond-ceiling architecture; attack the strongest missing lemma rather than merely proposing it.",
]


ROADMAPS = {
    "roadmap-alphabet-reduction": "Trace, subfield-subcode, algebraic concatenation, and multilevel routes beyond one-level Hadamard.",
    "roadmap-expander": "Finite epsilon-balanced and expander-amplification routes with explicit constants at epsilon=1/8.",
    "roadmap-inner-code": "Structured inner-code improvements and deterministic derandomization of low-rate concatenation.",
}


BASE_SPEC = r"""
The immutable target is an explicit binary linear code C subset F_2^n with
n=2^30=1,073,741,824 and d_min(C)>=469,762,048=(7/16)n.  Maximize the
rigorously proved rate R=dim(C)/n.  The current verified dimension is 3,688,448,
so a new record needs dimension at least 3,688,449.  Random sampling is not an
admissible construction.  Every field, code, tower level, divisor, graph,
ordering, shortening, puncturing, and padding choice must be deterministic and
symbolically recoverable.  Distance must be proved for every nonzero codeword.

The vanilla one-level Garcia--Stichtenoth plus RM(1,m-1) Hadamard calculation
has rate envelope
  (m/2^(m-1)) (1/8 - 1/(2^(m/2)-1))_+
for even m.  Its unique optimum is m=8 with rate 7/1920 =
0.0036458333333333333.  This is a ceiling of that standard TVZ/designed-distance
parameter template, not a universal upper bound on GS-derived codes or explicit
binary codes.  It is acceptable to improve the finite instantiation up to the
ceiling, but the primary objective is to cross 7/1920 through a mechanism that
actually leaves the template.  Never label parameter tuning inside the same
formula as a beyond-ceiling result.
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
    if int(cfg.get("researcher_count", 0)) < 10:
        raise ValueError("the campaign must have at least 10 researchers")
    if int(cfg.get("verifier_count", 0)) != 2:
        raise ValueError("every submission must receive exactly two independent reviews")
    if int(cfg.get("roadmap_count", 0)) < 3:
        raise ValueError("at least three proof roadmaps are required")
    if int(cfg.get("block_length", 0)) != N or int(cfg.get("minimum_distance", 0)) != D:
        raise ValueError("fixed target parameters changed")
    base = path.parent
    workspace = (base / str(value.get("workspace", ".."))).resolve()
    campaign_dir = (base / str(value.get("campaign_dir", "../research_state/campaign-10-ultra"))).resolve()
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
        for name in ("submissions", "reviews", "lemma_book", "roadmaps", "genius", "metadata"):
            (self.root / name).mkdir(parents=True, exist_ok=True)
        if self.jobs_path.exists():
            return self.status()
        jobs: list[dict[str, Any]] = []
        for index in range(10):
            jobs.append(self._job(f"researcher-{index + 1:04d}", "researcher", DIRECTIONS[index]))
        if self.cfg.get("literature_agent_enabled", True):
            jobs.append(self._job(
                "literature-sota-0001", "literature",
                "Audit the exact explicit-code literature baseline and extract finite, citable constants relevant to crossing 7/1920."))
        for job_id, focus in ROADMAPS.items():
            jobs.append(self._job(job_id, "roadmap", focus, phase="synthesis"))
        if self.cfg.get("lemma_writer_enabled", True):
            jobs.append(self._job("lemma-writer-0001", "lemma_writer", "Edit all reusable proof steps into the shared lemma book.", phase="synthesis"))
        if self.cfg.get("genius_enabled", True):
            jobs.append(self._job("GENIUS", "genius", "Construct the strongest integrated exact and asymptotic family from all campaign evidence.", phase="genius"))
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
            jobs.append(self._job(job_id, "researcher", DIRECTIONS[(ordinal - 1) % len(DIRECTIONS)]))
            existing.add(job_id)
            ordinal += 1
        self._write_jobs(jobs)
        return self.status()

    def _job(self, job_id: str, role: str, direction: str, phase: str = "research",
             dependency: str | None = None) -> dict[str, Any]:
        return {
            "id": job_id, "role": role, "direction": direction, "phase": phase,
            "dependency": dependency, "status": "queued", "attempts": 0,
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
You run at ultra reasoning.  Read AGENTS.md, TARGET.md, the contribution guide,
both baseline proofs, and data/records.json before reasoning.

{BASE_SPEC}

YOUR FOCUSED DIRECTION:
{job['direction']}

Produce genuine mathematical work.  A leaderboard_submission=true response must
contain a complete deterministic construction and an academic proof that checks
binary linearity, exact length, integer dimension, minimum distance, and every
finite parameter.  Do not use random existence, sampled codewords, hidden
O-constants, or an unavailable theorem.  Set leaderboard_submission=false when
any essential step is conditional.  State concise lemmas; put explanations in
their proofs.  You may report a rigorous obstruction or ceiling lemma when no
candidate survives.  Rate must equal dimension/1,073,741,824 exactly up to JSON
number precision.  ceiling_beaten is true only if the proved rate is strictly
greater than 7/1920 and the proof identifies the mechanism escaping the template.
"""
            return prompt, RESEARCH_SCHEMA
        if role == "verifier":
            source_id = str(job["dependency"])
            source_path = self.root / "submissions" / f"{source_id}.json"
            source = json.loads(source_path.read_text())
            prompt = f"""You are {job['id']}, one of two independent mathematical reviewers.
Do not rely on the other reviewer.  Read and audit {source_path.relative_to(self.paths.workspace)} line by line.

{BASE_SPEC}

The immutable source SHA-256 is {canonical_hash(source)}.  Recompute every
integer and verify every cited theorem's hypotheses, exact-length operation,
dimension claim, and minimum-distance implication.  Try to break the construction
with edge cases and low-weight words.  Check whether its ceiling classification
is honest.  Reject an unfixable false or inadmissible claim; request revision for
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
ending in an exact code at n=2^30 with rate greater than 7/1920.  Mark what is
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

Attempt to construct the strongest asymptotic explicit family and its exact
n=2^30 instantiation by combining only compatible proved components.  Treat
7/1920 as the vanilla GS+Hadamard template ceiling and make crossing it the main
architectural goal.  Do not fill gaps by optimism.  Distinguish verified facts,
conditional components, refutations, and new conjectures.  If a complete
beyond-ceiling proof is unavailable, identify the narrowest decisive missing
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
            if any(job["status"] == "failed" and int(job["attempts"]) < max_attempts for job in self._read_jobs() if job["role"] in roles):
                time.sleep(min(int(self.cfg.get("retry_seconds", 120)), 30))

    def _queue_verifiers(self) -> None:
        jobs = self._read_jobs()
        existing = {job["id"] for job in jobs}
        for source_path in sorted((self.root / "submissions").glob("researcher-*.json")):
            source = json.loads(source_path.read_text())
            if not source.get("leaderboard_submission"):
                continue
            source_id = source_path.stem
            for index in range(1, 3):
                job_id = f"verifier-{index}-{source_id}"
                if job_id not in existing:
                    jobs.append(self._job(job_id, "verifier", "Independent line-by-line proof audit.", phase="verification", dependency=source_id))
                    existing.add(job_id)
        self._write_jobs(jobs)

    def export_snapshot(self) -> dict[str, Any]:
        if not self.jobs_path.exists():
            return self.initialize()
        jobs = self._read_jobs()
        candidates = []
        verified = []
        for source_path in sorted((self.root / "submissions").glob("researcher-*.json")):
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
                "ceiling_beaten": source.get("ceiling_beaten"),
                "accepted_reviews": sum(review.get("verdict") == "accept" for review in reviews),
                "source_path": str(source_path.relative_to(self.paths.workspace)),
            }
            candidates.append(item)
            if (
                source.get("leaderboard_submission") and item["accepted_reviews"] >= 2
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
            "target": {"block_length": N, "minimum_distance": D, "current_dimension": CURRENT_K},
            "gs_hadamard_template_ceiling": CEILING_RATE,
            "promising_candidates": candidates, "doubly_verified_candidates": verified,
        }
        (self.root / "snapshot.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        (self.root / "status.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return payload

    def status(self) -> dict[str, Any]:
        if not self.jobs_path.exists():
            return self.initialize()
        return self.export_snapshot()

    def run(self) -> dict[str, Any]:
        self.initialize()
        self._run_phase({"researcher", "literature"})
        self._queue_verifiers()
        self._run_phase({"verifier"})
        self._run_phase({"lemma_writer", "roadmap"})
        self._run_phase({"genius"})
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
