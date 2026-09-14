import { useEffect, useMemo, useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import {
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronRight,
  FlaskConical,
  GitBranch,
  Menu,
  ShieldCheck,
  Target,
  X,
} from 'lucide-react';
import snapshot from '../../data/records.json';

type RecordEntry = (typeof snapshot.records)[number];
type NotebookTab = 'lemmas' | 'directions' | 'proofs' | 'review';

const N = snapshot.target.blockLength;
const D = snapshot.target.minimumDistance;
const gvRate = snapshot.benchmark.rate;
const literatureRate = snapshot.literatureBaseline.rate;
const repoUrl = 'https://github.com/kz99/binary-gv-concrete';

function formatInteger(value: number) {
  return new Intl.NumberFormat('en-US').format(value);
}

function formatRate(value: number) {
  return value.toFixed(10).replace(/0+$/, '').replace(/\.$/, '');
}

function formatScore(entry: RecordEntry) {
  return `${entry.rateType === 'certified_lower_bound' ? '≥ ' : ''}${formatRate(entry.rate)}`;
}

function getRoute() {
  const route = window.location.hash.replace(/^#\/?/, '');
  if (!route || route === 'record') return { page: 'record' as const, tab: 'lemmas' as NotebookTab };
  const [, tab] = route.split('/');
  const allowed: NotebookTab[] = ['lemmas', 'directions', 'proofs', 'review'];
  return {
    page: 'research' as const,
    tab: allowed.includes(tab as NotebookTab) ? (tab as NotebookTab) : 'lemmas',
  };
}

function MathBlock({ children }: { children: string }) {
  return <BlockMath math={children} errorColor="#9c2e22" renderError={() => <code>{children}</code>} />;
}

function MathInline({ children }: { children: string }) {
  return <InlineMath math={children} errorColor="#9c2e22" renderError={() => <code>{children}</code>} />;
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

function Header({ page }: { page: 'record' | 'research' }) {
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
        <strong><MathInline>{'\\mathbb F_2'}</MathInline></strong>
      </div>
      <div>
        <span>Block length</span>
        <strong><MathInline>{'n=2^{30}'}</MathInline></strong>
        <small>{formatInteger(N)}</small>
      </div>
      <div>
        <span>Required distance</span>
        <strong><MathInline>{'d_{\\min}\\ge 7n/16'}</MathInline></strong>
        <small>{formatInteger(D)}</small>
      </div>
      <div>
        <span>Score</span>
        <strong><MathInline>{'R=k/n'}</MathInline></strong>
        <small>maximize rate</small>
      </div>
      <div>
        <span>Admission</span>
        <strong>2-agent verified</strong>
        <small>proof required</small>
      </div>
    </section>
  );
}

function ProgressScale({ record }: { record: RecordEntry }) {
  const share = record.rate / gvRate;
  const literatureShare = literatureRate / gvRate;
  return (
    <section className="benchmark-panel">
      <div className="benchmark-copy">
        <span className="eyebrow">Distance to benchmark</span>
        <p>
          The verified record reaches <strong>{(share * 100).toFixed(2)}%</strong> of the binary GV rate.
        </p>
      </div>
      <div className="scale-wrap">
        <div className="scale-labels">
          <span>0</span>
          <span>GV&nbsp; {formatRate(gvRate)}</span>
        </div>
        <div className="scale-track">
          <div className="scale-fill" style={{ width: `${share * 100}%` }} />
          <span
            className="literature-pin"
            style={{ left: `${literatureShare * 100}%` }}
            title={`${snapshot.literatureBaseline.name}: ${formatRate(literatureRate)}`}
          >
            <i />
          </span>
          <span className="record-pin" style={{ left: `${share * 100}%` }}>
            <i />
            <b>record {formatScore(record)}</b>
          </span>
        </div>
        <div className="scale-foot">
          <span><i className="baseline-key" /> Fixed explicit literature baseline</span>
          <span>Existential reference only</span>
        </div>
      </div>
    </section>
  );
}

function VerificationBadge({ entry }: { entry: RecordEntry }) {
  return (
    <span className="verified-badge" title={entry.verification.summary}>
      <ShieldCheck size={15} /> Verified 2/2
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
  const isGs = entry.id === 'gs-densified-rm-1-7';
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
          <span>Rate</span>
          <strong>{formatScore(entry)}</strong>
          <small>{(entry.rate / gvRate * 100).toFixed(2)}% of GV</small>
        </div>
        <div className="concrete-parameters">
          <ParameterPill label="binary length n" value={formatInteger(entry.blockLength)} />
          <ParameterPill label="dimension k" value={formatInteger(entry.dimension)} />
          <ParameterPill label="proved distance d" value={`≥ ${formatInteger(entry.minimumDistance)}`} />
          <ParameterPill label="relative distance" value="7 / 16" />
        </div>
        <div className="construction-detail">
          <div>
            <span className="detail-label">Concrete choice</span>
            {isGs ? (
              <p>
                Outer: densified GS level <MathInline>{'(q,k,s)=(16,4,3)'}</MathInline> over <MathInline>{'\\mathbb F_{256}'}</MathInline>,
                <MathInline>{'[8{,}355{,}840,\\ge461{,}056,\\ge7{,}340{,}032]_{256}'}</MathInline>.
                Inner: <MathInline>{'\\operatorname{RM}(1,7)=[128,8,64]_2'}</MathInline>. Append 4,194,304 zero coordinates.
              </p>
            ) : (
              <p>
                Outer: <MathInline>{'[32{,}768,4{,}097,28{,}672]_{2^{16}}'}</MathInline> Reed–Solomon.
                Inner: <MathInline>{'\\operatorname{RM}(1,15)=[32{,}768,16,16{,}384]_2'}</MathInline>. No padding.
              </p>
            )}
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

function RecordPage() {
  const verified = useMemo(
    () => snapshot.records.filter((entry) => entry.status === 'verified').sort((a, b) => b.rate - a.rate),
    [],
  );
  const leader = verified[0];
  return (
    <main>
      <ParameterBar />
      <div className="page-shell record-page">
        <div className="page-heading">
          <div>
            <span className="eyebrow">Verified explicit constructions</span>
            <h1>Rate leaderboard</h1>
          </div>
          <div className="record-stat">
            <span>Current record</span>
            <strong>{formatScore(leader)}</strong>
            <small><MathInline>{'R=k/2^{30}'}</MathInline></small>
          </div>
        </div>
        <ProgressScale record={leader} />
        <div className="leaderboard-heading">
          <span>Rank</span>
          <span>Construction and certified parameters</span>
          <span>{verified.length} verified results</span>
        </div>
        <section className="records-list" aria-label="Verified rate leaderboard">
          {verified.map((entry, index) => <RecordCard key={entry.id} entry={entry} isLeader={index === 0} />)}
        </section>
        <p className="admission-note">
          Only results independently accepted by two AI verifier agents appear here. The GV value is displayed solely as a target line and is not a ranked construction.
        </p>
      </div>
    </main>
  );
}

const notebookTabs: { id: NotebookTab; label: string; icon: typeof BookOpen }[] = [
  { id: 'lemmas', label: 'Lemma book', icon: BookOpen },
  { id: 'directions', label: 'Directions', icon: GitBranch },
  { id: 'proofs', label: 'Proof notes', icon: FlaskConical },
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
              <MathInline>{`[2^{30},${entry.dimension.toLocaleString('en-US').replaceAll(',', '{,}')},\\ge ${entry.minimumDistance.toLocaleString('en-US').replaceAll(',', '{,}')}]_2`}</MathInline>
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

function ReviewPolicy() {
  return (
    <div className="review-page">
      <section className="policy-layout">
        <article className="policy-card emphasis">
          <span className="eyebrow">Admission gate</span>
          <h2>Two independent correctness votes</h2>
          <MathBlock>{'\\text{Agent A accepts}\\;\\land\\;\\text{Agent B accepts}\\;\\Longrightarrow\\;\\text{leaderboard eligible}'}</MathBlock>
          <p>Each verifier reads the construction and proof independently. An unresolved mathematical obstruction blocks publication.</p>
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
        {tab === 'review' && <ReviewPolicy />}
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
      {route.page === 'record' ? <RecordPage /> : <ResearchPage tab={route.tab} />}
      <Footer />
    </div>
  );
}
