import { useEffect, useMemo, useState } from 'react';
import katex from 'katex';
import {
  ArrowUpRight,
  BookOpen,
  Check,
  CheckCircle2,
  ChevronRight,
  Copy,
  FileText,
  FlaskConical,
  GitBranch,
  Menu,
  ShieldCheck,
  Target,
  X,
} from 'lucide-react';
import snapshot from '../../data/records.json';
import campaignSnapshotSeed from '../../research_state/campaign-epsilon-2-10-ultra/snapshot.json';
import contributorInstructions from '../../how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md?raw';

type RecordEntry = (typeof snapshot.records)[number];
type NotebookTab = 'lemmas' | 'directions' | 'proofs' | 'discussion' | 'review';
type CampaignCandidate = {
  id: string;
  title: string;
  status: string;
  submission_class: string;
  dimension: number | null;
  minimum_distance: number | null;
  rate: number | null;
  polynomial_generator?: boolean;
  baseline_beaten: boolean;
  accepted_reviews: number;
  source_path: string;
};
type CampaignSnapshot = {
  updated_at: string;
  researcher_count: number;
  counts: Record<string, number>;
  promising_candidates: CampaignCandidate[];
  doubly_verified_candidates: CampaignCandidate[];
  message_board?: {
    post_count: number;
    recent_posts: Array<{
      job_id: string;
      team: string;
      round: number;
      kind: string;
      subject: string;
      body_markdown: string;
      references: string[];
    }>;
  };
};

const N = snapshot.target.blockLength;
const D = snapshot.target.minimumDistance;
const gvDimension = snapshot.benchmark.equivalentDimension;
const repoUrl = 'https://github.com/kz99/binary-gv-concrete';
const campaignSnapshotUrl = 'https://raw.githubusercontent.com/kz99/binary-gv-concrete/main/research_state/campaign-epsilon-2-10-ultra/snapshot.json';

function useCampaignSnapshot() {
  const [campaign, setCampaign] = useState<CampaignSnapshot>(campaignSnapshotSeed as CampaignSnapshot);
  const [live, setLive] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function refresh() {
      try {
        const response = await fetch(`${campaignSnapshotUrl}?t=${Date.now()}`, { cache: 'no-store' });
        if (!response.ok) throw new Error(`campaign snapshot: ${response.status}`);
        const next = await response.json() as CampaignSnapshot;
        if (!cancelled && Array.isArray(next.promising_candidates)) {
          setCampaign(next);
          setLive(true);
        }
      } catch {
        // Keep the bundled checkpoint when the raw GitHub feed is unavailable.
      }
    }
    refresh();
    const timer = window.setInterval(refresh, 30_000);
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, []);
  return { campaign, live };
}

function formatInteger(value: number) {
  return new Intl.NumberFormat('en-US').format(value);
}

function formatRate(value: number) {
  return value.toFixed(10).replace(/0+$/, '').replace(/\.$/, '');
}

function formatScore(entry: RecordEntry) {
  return `${entry.rateType === 'certified_lower_bound' ? '≥ ' : ''}${formatRate(entry.rate)}`;
}

function formatDimension(value: number) {
  return formatInteger(Math.round(value));
}

function getRoute() {
  const route = window.location.hash.replace(/^#\/?/, '');
  if (!route || route === 'record') return { page: 'record' as const, tab: 'lemmas' as NotebookTab };
  if (route === 'contribute') return { page: 'contribute' as const, tab: 'lemmas' as NotebookTab };
  const [, tab] = route.split('/');
  const allowed: NotebookTab[] = ['lemmas', 'directions', 'proofs', 'discussion', 'review'];
  return {
    page: 'research' as const,
    tab: allowed.includes(tab as NotebookTab) ? (tab as NotebookTab) : 'lemmas',
  };
}

function MathBlock({ children }: { children: string }) {
  const html = katex.renderToString(children, {
    displayMode: true,
    throwOnError: false,
    errorColor: '#9c2e22',
  });
  return <div className="math-block" dangerouslySetInnerHTML={{ __html: html }} />;
}

function MathInline({ children }: { children: string }) {
  const html = katex.renderToString(children, {
    displayMode: false,
    throwOnError: false,
    errorColor: '#9c2e22',
  });
  return <span className="math-inline" dangerouslySetInnerHTML={{ __html: html }} />;
}

function BrandMark() {
  return (
    <div className="brand-mark" aria-hidden="true">
      <span>01</span>
      <i />
      <span>10</span>
    </div>
  );
}

function Header({ page }: { page: 'record' | 'research' | 'contribute' }) {
  const [open, setOpen] = useState(false);
  return (
    <header className="site-header">
      <div className="header-inner">
        <a className="wordmark" href="#/record" aria-label="Binary GV Concrete home">
          <BrandMark />
          <span>
            <strong>Binary GV</strong>
            <small>Concrete Observatory</small>
          </span>
        </a>
        <button className="menu-button" onClick={() => setOpen(!open)} aria-label="Toggle navigation">
          {open ? <X size={19} /> : <Menu size={19} />}
        </button>
        <nav className={open ? 'primary-nav open' : 'primary-nav'}>
          <a className={page === 'record' ? 'active' : ''} href="#/record" onClick={() => setOpen(false)}>
            Record
          </a>
          <a className={page === 'research' ? 'active' : ''} href="#/research/lemmas" onClick={() => setOpen(false)}>
            Research notebook
          </a>
          <a className={page === 'contribute' ? 'active' : ''} href="#/contribute" onClick={() => setOpen(false)}>
            Contribute
          </a>
          <a className="github-link" href={repoUrl} target="_blank" rel="noreferrer">
            GitHub <ArrowUpRight size={13} />
          </a>
        </nav>
      </div>
    </header>
  );
}

function ParameterBar() {
  return (
    <section className="parameter-bar" aria-label="Fixed problem parameters">
      <div>
        <span>Alphabet</span>
        <strong><MathInline>{'\\mathbb{F}_{2}'}</MathInline></strong>
      </div>
      <div>
        <span>Block length</span>
        <strong><MathInline>{'n=2^{30}'}</MathInline></strong>
        <small>{formatInteger(N)}</small>
      </div>
      <div>
        <span>Required distance</span>
        <strong><MathInline>{'d_{\\mathrm{min}}\\geq (1/2-2^{-10})n'}</MathInline></strong>
        <small>{formatInteger(D)}</small>
      </div>
      <div>
        <span>Score</span>
        <strong><MathInline>{'k'}</MathInline></strong>
        <small>maximize dimension</small>
      </div>
      <div>
        <span>Admission</span>
        <strong>1-agent verified</strong>
        <small>proof required</small>
      </div>
    </section>
  );
}

function ProgressScale({ record, proposed }: { record: RecordEntry; proposed?: CampaignCandidate }) {
  const recordShare = record.dimension / gvDimension;
  const proposedShare = proposed?.dimension == null ? null : proposed.dimension / gvDimension;
  return (
    <section className="benchmark-panel">
      <div className="benchmark-copy">
        <span className="eyebrow">Concrete dimension target</span>
        <p>
          The verified record has <strong>k={formatInteger(record.dimension)}</strong>; the GV benchmark is <strong>k≈{formatDimension(gvDimension)}</strong>.
        </p>
      </div>
      <div className="scale-wrap">
        <div className="scale-labels">
          <span>k = 0</span>
          <span>GV bound&nbsp; k ≈ {formatDimension(gvDimension)}</span>
        </div>
        <div className="scale-track">
          <div className="scale-fill" style={{ width: `${recordShare * 100}%` }} />
          {proposedShare != null && proposedShare > recordShare && (
            <div
              className="scale-proposed-segment"
              style={{ left: `${recordShare * 100}%`, width: `${(proposedShare - recordShare) * 100}%` }}
            />
          )}
          <span className="gv-pin" title={`Gilbert–Varshamov benchmark: k≈${formatDimension(gvDimension)}`}><i /></span>
          <span className={`record-pin ${recordShare < 0.1 ? 'near-origin' : ''}`} style={{ left: `${recordShare * 100}%` }}>
            <i />
            <b>record k={formatInteger(record.dimension)}</b>
          </span>
          {proposedShare != null && proposedShare > recordShare && (
            <span className="proposed-pin" style={{ left: `${proposedShare * 100}%` }}>
              <i />
              <b>best proposed k={formatInteger(proposed?.dimension ?? 0)}</b>
            </span>
          )}
        </div>
        <div className="scale-foot">
          <span><i className="baseline-key" /> Verified explicit construction</span>
          {proposedShare != null && proposedShare > recordShare ? (
            <span><i className="proposed-key" /> Best proposed claim</span>
          ) : <span>Dashed line: existential GV target</span>}
        </div>
      </div>
    </section>
  );
}

function VerificationBadge({ entry }: { entry: RecordEntry }) {
  return (
    <span className="verified-badge" title={entry.verification.summary}>
      <ShieldCheck size={15} /> Verified
    </span>
  );
}

function ParameterPill({ label, value }: { label: string; value: string }) {
  return (
    <span className="parameter-pill">
      <small>{label}</small>
      <b>{value}</b>
    </span>
  );
}

function RecordCard({ entry, isLeader }: { entry: RecordEntry; isLeader: boolean }) {
  const proofUrl = `${repoUrl}/blob/main/${entry.proofPath}`;
  const relativeDistance = `${snapshot.target.relativeDistanceNumerator} / ${snapshot.target.relativeDistanceDenominator}`;
  return (
    <article className={isLeader ? 'record-card leader' : 'record-card'}>
      <div className="rank-cell">
        <span>#{entry.rank}</span>
        {isLeader && <small>record</small>}
      </div>
      <div className="record-main">
        <div className="record-title-row">
          <div>
            <p className="construction-family">{entry.tags.slice(0, 3).join(' · ')}</p>
            <h2>{entry.name}</h2>
          </div>
          <VerificationBadge entry={entry} />
        </div>
        <div className="rate-line">
          <span>Dimension</span>
          <strong>k = {formatInteger(entry.dimension)}</strong>
          <small>rate {formatScore(entry)}</small>
        </div>
        <div className="concrete-parameters">
          <ParameterPill label="binary length n" value={formatInteger(entry.blockLength)} />
          <ParameterPill label="dimension k" value={formatInteger(entry.dimension)} />
          <ParameterPill label="proved distance d" value={`≥ ${formatInteger(entry.minimumDistance)}`} />
          <ParameterPill label="relative distance" value={relativeDistance} />
        </div>
        <div className="construction-detail">
          <div>
            <span className="detail-label">Concrete choice</span>
            <p>
              Evaluate all affine Boolean functions on <MathInline>{'\\mathbb F_2^{30}'}</MathInline>.
              This is <MathInline>{'\\operatorname{RM}(1,30)=[2^{30},31,2^{29}]_2'}</MathInline>.
            </p>
          </div>
          <a href={proofUrl} target="_blank" rel="noreferrer">
            Read proof <ArrowUpRight size={14} />
          </a>
        </div>
        <div className="audit-strip">
          <span><Check size={13} /> arithmetic</span>
          <span><Check size={13} /> correctness agent A</span>
          <span><Check size={13} /> correctness agent B</span>
          <span><Check size={13} /> readable proof</span>
        </div>
      </div>
    </article>
  );
}

function ProposedCard({ candidate, rank }: { candidate: CampaignCandidate; rank: number }) {
  const sourceUrl = `${repoUrl}/blob/main/${candidate.source_path}`;
  return (
    <article className="record-card proposed">
      <div className="rank-cell">
        <span>P{String(rank).padStart(2, '0')}</span>
        <small>proposed</small>
      </div>
      <div className="record-main">
        <div className="record-title-row">
          <div>
            <p className="construction-family">{candidate.submission_class.replaceAll('_', ' · ')}</p>
            <h2>{candidate.title}</h2>
          </div>
          <span className="proposed-badge"><FlaskConical size={14} /> Under review</span>
        </div>
        <div className="rate-line">
          <span>Proposed dimension</span>
          <strong>{candidate.dimension == null ? '—' : `k = ${formatInteger(candidate.dimension)}`}</strong>
          {candidate.rate != null && <small>rate {formatRate(candidate.rate)}</small>}
        </div>
        {candidate.dimension != null && candidate.minimum_distance != null && (
          <div className="concrete-parameters">
            <ParameterPill label="binary length n" value={formatInteger(N)} />
            <ParameterPill label="dimension k" value={formatInteger(candidate.dimension)} />
            <ParameterPill label="claimed distance d" value={`≥ ${formatInteger(candidate.minimum_distance)}`} />
            <ParameterPill label="relative distance" value={`${snapshot.target.relativeDistanceNumerator} / ${snapshot.target.relativeDistanceDenominator}`} />
          </div>
        )}
        <div className="construction-detail proposed-detail">
          <p>
            {candidate.baseline_beaten ? 'Claims to improve the current verified baseline. ' : ''}
            This mathematical proof enters one independent verifier review as soon as it is submitted.
          </p>
          <a href={sourceUrl} target="_blank" rel="noreferrer">Read submission <ArrowUpRight size={14} /></a>
        </div>
        <div className="proposed-audit">
          <span><FlaskConical size={12} /> {candidate.status}</span>
          <span>{candidate.accepted_reviews}/1 verifier acceptance</span>
        </div>
      </div>
    </article>
  );
}

function RecordPage() {
  const { campaign, live } = useCampaignSnapshot();
  const verified = useMemo(
    () => snapshot.records.filter((entry) => entry.status === 'verified').sort((a, b) => b.rate - a.rate),
    [],
  );
  const leader = verified[0];
  const proposed = useMemo(
    () => campaign.promising_candidates
      .filter((candidate) => candidate.rate != null && candidate.dimension != null)
      .filter((candidate) => candidate.polynomial_generator === true)
      .filter((candidate) => !snapshot.records.some((entry) => entry.id === candidate.id))
      .sort((a, b) => (b.rate ?? -1) - (a.rate ?? -1)),
    [campaign],
  );
  const succeeded = campaign.counts.succeeded ?? 0;
  const totalResearch = campaign.researcher_count;
  return (
    <main>
      <ParameterBar />
      <div className="page-shell record-page">
        <div className="page-heading">
          <div>
            <span className="eyebrow">Verified explicit constructions</span>
            <h1>Dimension leaderboard</h1>
          </div>
          <div className="record-stat">
            <span>Current record</span>
            <strong>k = {formatInteger(leader.dimension)}</strong>
            <small>rate {formatScore(leader)}</small>
          </div>
        </div>
        <div className="campaign-feed-status" role="status">
          <span className="feed-dot" /> Live research feed {live ? 'connected' : 'using latest checkpoint'} · {succeeded} jobs completed · {totalResearch} researchers · refreshed every 30 seconds
        </div>
        <ProgressScale record={leader} proposed={proposed[0]} />
        <div className="leaderboard-heading">
          <span>Rank</span>
          <span>Construction and certified parameters</span>
          <span>{verified.length} verified results</span>
        </div>
        <section className="records-list" aria-label="Verified dimension leaderboard">
          {verified.map((entry, index) => <RecordCard key={entry.id} entry={entry} isLeader={index === 0} />)}
        </section>
        {proposed.length > 0 && (
          <>
            <div className="leaderboard-heading proposed-heading">
              <span>Status</span>
              <span>Proposed constructions and claimed parameters</span>
              <span>{proposed.length} under review</span>
            </div>
            <section className="records-list" aria-label="Proposed constructions awaiting verification">
              {proposed.map((candidate, index) => <ProposedCard key={candidate.id} candidate={candidate} rank={index + 1} />)}
            </section>
          </>
        )}
        <p className="admission-note">
          Green cards are verified records. Amber cards are proposed research outputs shown for transparency; they are not ranked or certified until one independent verifier accepts their proof. Every displayed construction must include a deterministic polynomial-time algorithm for outputting its full generator matrix. The GV value is displayed solely as a target line.
        </p>
      </div>
    </main>
  );
}

const notebookTabs: { id: NotebookTab; label: string; icon: typeof BookOpen }[] = [
  { id: 'lemmas', label: 'Lemma book', icon: BookOpen },
  { id: 'directions', label: 'Directions', icon: GitBranch },
  { id: 'proofs', label: 'Proof notes', icon: FlaskConical },
  { id: 'discussion', label: 'Message board', icon: FileText },
  { id: 'review', label: 'Review log', icon: ShieldCheck },
];

function LemmaBook() {
  return (
    <section className="notebook-list">
      {snapshot.research.lemmas.map((lemma, index) => (
        <article className="notebook-card lemma-card" key={lemma.id}>
          <div className="notebook-index">L{String(index + 1).padStart(2, '0')}</div>
          <div>
            <div className="notebook-title-line">
              <h2>{lemma.title}</h2>
              <span className="status proved">proved</span>
            </div>
            <MathBlock>{lemma.statement}</MathBlock>
            <p className="used-by">Used by {lemma.usedBy.length} verified construction{lemma.usedBy.length === 1 ? '' : 's'}.</p>
          </div>
        </article>
      ))}
    </section>
  );
}

function Directions() {
  return (
    <section className="directions-grid">
      {snapshot.research.directions.map((direction, index) => (
        <article className="direction-card" key={direction.id}>
          <div className="direction-top">
            <span>D{String(index + 1).padStart(2, '0')}</span>
            <span className={`priority ${direction.priority}`}>{direction.priority} priority</span>
          </div>
          <h2>{direction.title}</h2>
          <p>{direction.summary}</p>
          <div className="direction-state"><i /> {direction.state}</div>
        </article>
      ))}
    </section>
  );
}

function ProofNotes() {
  return (
    <section className="notebook-list">
      {snapshot.records.map((entry) => (
        <article className="notebook-card proof-card" key={entry.id}>
          <div className="proof-icon"><ShieldCheck size={21} /></div>
          <div>
            <div className="notebook-title-line">
              <h2>{entry.name}</h2>
              <VerificationBadge entry={entry} />
            </div>
            <p>{entry.construction}</p>
            <div className="proof-parameter-line">
              <MathInline>{`[2^{30},${entry.dimension.toLocaleString('en-US').replaceAll(',', '{,}')},\\geq ${entry.minimumDistance.toLocaleString('en-US').replaceAll(',', '{,}')}]_2`}</MathInline>
              <span>rate {formatScore(entry)}</span>
            </div>
            <a className="text-link" href={`${repoUrl}/blob/main/${entry.proofPath}`} target="_blank" rel="noreferrer">
              Open complete proof certificate <ChevronRight size={14} />
            </a>
          </div>
        </article>
      ))}
    </section>
  );
}

function DiscussionBoard({ board }: { board?: CampaignSnapshot['message_board'] }) {
  const posts = board?.recent_posts ?? [];
  if (!posts.length) {
    return (
      <section className="notebook-list">
        <article className="notebook-card">
          <div className="notebook-index">—</div>
          <div><h2>Message board is ready</h2><p>Teams will post proved lemmas, precise obstacles, and concrete questions here as their work is written into the repository.</p></div>
        </article>
      </section>
    );
  }
  return (
    <section className="notebook-list">
      {posts.map((post, index) => (
        <article className="notebook-card" key={post.job_id + '-' + index}>
          <div className="notebook-index">{post.team}</div>
          <div>
            <div className="notebook-title-line"><h2>{post.subject}</h2><span className="status proved">{post.kind}</span></div>
            <p>{post.body_markdown}</p>
            <p className="used-by">{post.job_id} · round {post.round}{post.references.length ? ' · ' + post.references.join(', ') : ''}</p>
          </div>
        </article>
      ))}
    </section>
  );
}

function ReviewPolicy() {
  return (
    <div className="review-page">
      <section className="policy-layout">
        <article className="policy-card emphasis">
          <span className="eyebrow">Admission gate</span>
          <h2>One independent correctness vote</h2>
          <MathBlock>{'\\text{Independent verifier accepts}\\;\\Longrightarrow\\;\\text{leaderboard eligible}'}</MathBlock>
          <p>The verifier reads the construction and proof independently. An unresolved mathematical obstruction blocks publication.</p>
        </article>
        <article className="policy-card">
          <span>01</span>
          <h3>Check the mathematics</h3>
          <p>Recompute every concrete parameter and audit the logical steps establishing linearity, dimension, length, and minimum distance.</p>
        </article>
        <article className="policy-card">
          <span>02</span>
          <h3>Check the proof is readable</h3>
          <p>The note must let a mathematical reader reconstruct the argument and locate every invoked result.</p>
        </article>
        <article className="policy-card">
          <span>03</span>
          <h3>Stay pragmatic</h3>
          <p>Do not demand low-level formalization, ceremonial detail, or stylistic perfection. Ask for revision only when exposition hides a genuine gap or makes correctness materially hard to assess.</p>
        </article>
      </section>
      <section className="review-history">
        <div className="section-label">Recorded independent decisions</div>
        {snapshot.records.map((entry) => (
          <article className="review-record" key={entry.id}>
            <div className="review-record-head">
              <div>
                <span>Rate {formatScore(entry)}</span>
                <h2>{entry.name}</h2>
              </div>
              <VerificationBadge entry={entry} />
            </div>
            <div className="review-votes">
              {entry.verification.reviews.map((review) => (
                <div className="review-vote" key={review.agent}>
                  <div><ShieldCheck size={16} /><strong>{review.agent}</strong><span>{review.decision}</span></div>
                  <p>{review.summary}</p>
                  <small><Check size={11} /> correctness &nbsp; <Check size={11} /> writing</small>
                </div>
              ))}
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}

function ResearchPage({ tab }: { tab: NotebookTab }) {
  const { campaign } = useCampaignSnapshot();
  return (
    <main>
      <div className="notebook-header">
        <div className="page-shell">
          <span className="eyebrow">Behind the leaderboard</span>
          <h1>Research notebook</h1>
          <p>Shared lemmas, proof certificates, active directions, and the publication standard live here. None of this working material appears on the main record page.</p>
        </div>
      </div>
      <div className="notebook-tabs-wrap">
        <nav className="page-shell notebook-tabs" aria-label="Research notebook sections">
          {notebookTabs.map(({ id, label, icon: Icon }) => (
            <a key={id} className={tab === id ? 'active' : ''} href={`#/research/${id}`}>
              <Icon size={15} /> {label}
            </a>
          ))}
        </nav>
      </div>
      <div className="page-shell notebook-content">
        {tab === 'lemmas' && <LemmaBook />}
        {tab === 'directions' && <Directions />}
        {tab === 'proofs' && <ProofNotes />}
        {tab === 'discussion' && <DiscussionBoard board={campaign.message_board} />}
        {tab === 'review' && <ReviewPolicy />}
      </div>
    </main>
  );
}

const literature = [
  {
    tag: 'Start here',
    title: 'Binary Codes with Distance Close to Half',
    authors: 'Dean Doron · 2024 survey',
    note: 'A focused map of explicit constructions in the high-distance regime.',
    href: 'https://eccc.weizmann.ac.il/report/2024/159/',
  },
  {
    tag: 'Near-GV',
    title: 'Explicit, Almost Optimal, Epsilon-Balanced Codes',
    authors: 'Amnon Ta-Shma · STOC 2017',
    note: 'The foundational explicit rate Ω(ε^{2+o(1)}) construction.',
    href: 'https://www.cs.tau.ac.il/~amnon/Papers/T.STOC17.pdf',
  },
  {
    tag: 'Amplification',
    title: 'Wide Replacement Products Meet Gray Codes',
    authors: 'Gil Cohen and Itay Cohen · 2025',
    note: 'The latest improvement within the wide-replacement framework.',
    href: 'https://eccc.weizmann.ac.il/report/2025/179/',
  },
  {
    tag: 'Concatenation',
    title: 'When Do Low-Rate Concatenated Codes Approach GV?',
    authors: 'Doron, Mosheiff, and Wootters · 2024',
    note: 'Structural conditions that suggest concrete derandomization targets.',
    href: 'https://arxiv.org/abs/2405.08584',
  },
  {
    tag: 'AG codes',
    title: 'A Tower of Artin–Schreier Extensions',
    authors: 'Garcia and Stichtenoth · 1995',
    note: 'The optimal function-field tower behind the current baseline.',
    href: 'https://doi.org/10.1007/BF01884295',
  },
  {
    tag: 'New direction',
    title: 'Tracing AG Codes: Toward Meeting GV',
    authors: 'Cohen, Doron, Goldgraber, and Manket · 2025',
    note: 'Algebraic field trace as an alternative to ordinary concatenation.',
    href: 'https://arxiv.org/abs/2511.08788',
  },
];

function CopyInstructionsButton() {
  const [copyState, setCopyState] = useState<'idle' | 'copied' | 'error'>('idle');

  async function copyInstructions() {
    try {
      await navigator.clipboard.writeText(contributorInstructions);
      setCopyState('copied');
      window.setTimeout(() => setCopyState('idle'), 2200);
    } catch {
      setCopyState('error');
    }
  }

  return (
    <button className={`copy-button ${copyState}`} onClick={copyInstructions} type="button">
      {copyState === 'copied' ? <CheckCircle2 size={16} /> : <Copy size={16} />}
      {copyState === 'copied' ? 'Copied to clipboard' : copyState === 'error' ? 'Select the text below' : 'Copy complete instructions'}
    </button>
  );
}

function ContributePage() {
  return (
    <main className="contribute-page">
      <section className="contribute-intro">
        <div className="page-shell contribute-intro-grid">
          <div>
            <span className="eyebrow">Open research problem</span>
            <h1>Improve the verified dimension.</h1>
            <p>
              Contribute a deterministic binary code with the largest provable dimension at the exact target. Its full generator matrix must be computable in polynomial time, and every submission is independently audited by one verifier agent before it can enter the record table.
            </p>
          </div>
          <div className="contribute-target">
            <span>Strict improvement target</span>
            <strong><MathInline>{'k\\geq 32'}</MathInline></strong>
            <small>GV benchmark: <MathInline>{`k\\approx ${formatDimension(gvDimension)}`}</MathInline></small>
            <i>with <MathInline>{'n=2^{30}'}</MathInline> and <MathInline>{`d_{\\mathrm{min}}\\geq ${formatInteger(D).replaceAll(',', '{,}')}`}</MathInline></i>
          </div>
        </div>
      </section>

      <div className="page-shell contribute-content">
        <section className="contribution-flow" aria-label="Submission workflow">
          {[
            ['01', 'Construct', 'Specify every field, constituent code, map, and a deterministic polynomial-time algorithm that emits the complete generator matrix.'],
            ['02', 'Prove', 'Write a concise academic note proving binary linearity, length, dimension, distance, and the generator-runtime bound.'],
            ['03', 'Submit', 'Open a pull request with an under-review JSON record and the proof certificate.'],
            ['04', 'Verify', 'One independent AI verifier recomputes and audits the claim before it becomes rankable.'],
          ].map(([number, title, copy]) => (
            <article key={number}>
              <span>{number}</span>
              <h2>{title}</h2>
              <p>{copy}</p>
            </article>
          ))}
        </section>

        <section className="copy-instructions-section">
          <div className="copy-intro">
            <div>
              <span className="eyebrow">One-click research brief</span>
              <h2>Give the complete setup to a person or agent.</h2>
              <p>The copied Markdown is the canonical file in the repository: problem statement, exact record to beat, admissibility, proof requirements, research directions, data schema, pull-request workflow, verifier protocol, literature, and checklist.</p>
            </div>
            <div className="copy-actions">
              <CopyInstructionsButton />
              <a href={`${repoUrl}/blob/main/how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md`} target="_blank" rel="noreferrer">
                <FileText size={15} /> Open file <ArrowUpRight size={12} />
              </a>
            </div>
          </div>
          <div className="instruction-preview">
            <div className="instruction-preview-bar">
              <span>how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md</span>
              <span>{contributorInstructions.split(/\s+/).length.toLocaleString()} words</span>
            </div>
            <pre>{contributorInstructions}</pre>
          </div>
        </section>

        <section className="literature-section">
          <div className="section-heading-row">
            <div>
              <span className="eyebrow">Literature map</span>
              <h2>Where to start</h2>
            </div>
            <a href={`${repoUrl}/blob/main/how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md#8-literature-map`} target="_blank" rel="noreferrer">
              Full reading list <ArrowUpRight size={13} />
            </a>
          </div>
          <div className="literature-grid">
            {literature.map((paper) => (
              <a href={paper.href} target="_blank" rel="noreferrer" className="literature-card" key={paper.title}>
                <span>{paper.tag}</span>
                <h3>{paper.title}</h3>
                <small>{paper.authors}</small>
                <p>{paper.note}</p>
                <ArrowUpRight size={15} />
              </a>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

function Footer() {
  return (
    <footer>
      <div className="page-shell footer-inner">
        <span>Binary GV Concrete</span>
        <span>Exact parameters · symbolic constructions · proof-first verification</span>
        <a href={repoUrl} target="_blank" rel="noreferrer">Source and data <ArrowUpRight size={12} /></a>
      </div>
    </footer>
  );
}

export function App() {
  const [route, setRoute] = useState(getRoute);
  useEffect(() => {
    const update = () => setRoute(getRoute());
    window.addEventListener('hashchange', update);
    if (!window.location.hash) window.history.replaceState(null, '', '#/record');
    return () => window.removeEventListener('hashchange', update);
  }, []);

  return (
    <div className="app-shell">
      <Header page={route.page} />
      {route.page === 'record' ? <RecordPage /> : route.page === 'research' ? <ResearchPage tab={route.tab} /> : <ContributePage />}
      <Footer />
    </div>
  );
}
