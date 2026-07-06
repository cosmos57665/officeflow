import { useState } from 'react';
import { DownloadLink, ModuleHeader, Notice, Panel, PrimaryButton } from '../components';
import { postForm } from '../api';
import type { MinutesData } from '../types';

type Result = { data: MinutesData; elapsed: number; provider: string; docx_file_id: string };

function textList(value: unknown, fallback: string) {
  if (Array.isArray(value)) {
    const items = value.map((item) => String(item).trim()).filter(Boolean);
    return items.length ? items : [fallback];
  }
  return value ? [String(value)] : [fallback];
}

function actionItems(value: unknown) {
  return Array.isArray(value) ? value.filter((item) => item && typeof item === 'object') as NonNullable<MinutesData['action_items']> : [];
}

export default function Minutes({ demo }: { demo: boolean }) {
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<Result | null>(null);

  async function run(useSample: boolean) {
    setBusy(true);
    setError('');
    try {
      const form = new FormData();
      form.set('demo', String(demo));
      form.set('use_sample', String(useSample));
      if (file && !useSample) form.set('audio', file);
      setResult(await postForm<Result>('/api/minutes', form));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not generate minutes.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <ModuleHeader kicker="Module 01" title="Meeting Minutes" text="Upload audio and generate structured Word minutes." />
      <Panel title="Input">
        <input type="file" accept=".mp3,.wav,.m4a" onChange={(event) => setFile(event.target.files?.[0] || null)} />
        <div className="actions">
          <PrimaryButton busy={busy} onClick={() => run(false)}>Generate Minutes</PrimaryButton>
          <button onClick={() => run(true)} disabled={busy}>Use sample audio</button>
        </div>
        {demo ? <p className="hint">Demo Mode uses cached minutes output and still creates a Word document.</p> : null}
      </Panel>
      {error ? <Notice kind="error">{error}</Notice> : null}
      {result ? (
        <Panel title="Generated minutes">
          <h3>{result.data.title || 'Meeting Minutes'}</h3>
          <p className="muted">
            Date: {result.data.date || 'Not specified'} · Attendees: {(result.data.attendees || []).join(', ') || 'Not specified'}
          </p>
          <h4>Summary</h4>
          <ul>{textList(result.data.summary, 'No summary available.').map((item) => <li key={item}>{item}</li>)}</ul>
          <h4>Decisions</h4>
          <ul>{textList(result.data.decisions, 'No decisions recorded.').map((item) => <li key={item}>{item}</li>)}</ul>
          <h4>Action Items</h4>
          <div className="table">
            {actionItems(result.data.action_items).map((item, index) => (
              <div className="row" key={`${item.task}-${index}`}>
                <span>{item.task || 'Task'}</span><span>{item.owner || 'Owner'}</span><span>{item.deadline || 'Deadline'}</span>
              </div>
            ))}
          </div>
          <Notice kind="success">Done in {result.elapsed.toFixed(1)} seconds via {result.provider}.</Notice>
          <DownloadLink fileId={result.docx_file_id}>Download Word document</DownloadLink>
        </Panel>
      ) : null}
    </>
  );
}
