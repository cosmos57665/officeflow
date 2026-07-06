import { useState } from 'react';
import { ModuleHeader, Notice, Panel, PrimaryButton } from '../components';
import { postJson } from '../api';
import type { EmailItem } from '../types';

type Result = { emails: EmailItem[]; elapsed: number; provider: string };
const categories: EmailItem['category'][] = ['Urgent', 'Action Needed', 'FYI'];

export default function Inbox({ demo }: { demo: boolean }) {
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<Result | null>(null);

  async function loadSample() {
    const response = await fetch('/samples/emails.txt');
    setText(await response.text());
  }

  async function run() {
    setBusy(true);
    setError('');
    try {
      setResult(await postJson<Result>('/api/inbox', { text, demo }));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not triage inbox.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <ModuleHeader kicker="Module 02" title="Inbox Triage" text="Paste raw emails and get priority buckets with draft replies." />
      <Panel title="Input">
        <textarea value={text} onChange={(event) => setText(event.target.value)} rows={10} placeholder="Paste emails separated with ---" />
        <div className="actions">
          <PrimaryButton busy={busy} onClick={run}>Triage Inbox</PrimaryButton>
          <button onClick={loadSample} disabled={busy}>Load sample emails</button>
        </div>
      </Panel>
      {error ? <Notice kind="error">{error}</Notice> : null}
      {result ? (
        <>
          <Notice kind="success">{result.emails.length} emails triaged in {result.elapsed.toFixed(1)} seconds via {result.provider}.</Notice>
          <div className="columns">
            {categories.map((category) => (
              <Panel key={category} title={`${category} · ${result.emails.filter((e) => e.category === category).length}`}>
                {result.emails.filter((email) => email.category === category).map((email) => (
                  <article className="email" key={`${email.from}-${email.subject}`}>
                    <strong>{email.subject}</strong>
                    <small>From: {email.from}</small>
                    <p>{email.one_line_summary}</p>
                    {email.suggested_reply ? <pre>{email.suggested_reply}</pre> : null}
                  </article>
                ))}
              </Panel>
            ))}
          </div>
        </>
      ) : null}
    </>
  );
}
