import { useState } from 'react';
import { DownloadLink, ModuleHeader, Notice, Panel, PrimaryButton } from '../components';
import { fileUrl, postForm } from '../api';
import type { Preview } from '../types';

type Result = { count: number; elapsed: number; provider: string; zip_file_id: string; previews: Preview[] };

export default function Docs({ demo }: { demo: boolean }) {
  const [file, setFile] = useState<File | null>(null);
  const [docType, setDocType] = useState('Merit Certificate');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<Result | null>(null);

  async function run(useSample = false) {
    setBusy(true);
    setError('');
    try {
      const form = new FormData();
      form.set('demo', String(demo));
      form.set('use_sample', String(useSample));
      form.set('doc_type', docType);
      if (file && !useSample) form.set('csv', file);
      setResult(await postForm<Result>('/api/docs', form));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not generate documents.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <ModuleHeader kicker="Module 03" title="Bulk Document Generator" text="Generate personalized PDFs from a student or employee CSV." />
      <Panel title="Input">
        <input type="file" accept=".csv" onChange={(event) => setFile(event.target.files?.[0] || null)} />
        <select value={docType} onChange={(event) => setDocType(event.target.value)}>
          <option>Merit Certificate</option>
          <option>Progress Report</option>
        </select>
        <div className="actions">
          <PrimaryButton busy={busy} onClick={() => run(false)}>Generate All</PrimaryButton>
          <button onClick={() => run(true)} disabled={busy}>Use sample CSV</button>
        </div>
      </Panel>
      {error ? <Notice kind="error">{error}</Notice> : null}
      {result ? (
        <Panel title="Generated documents">
          <Notice kind="success">Generated {result.count} PDFs in {result.elapsed.toFixed(1)} seconds via {result.provider}.</Notice>
          <DownloadLink fileId={result.zip_file_id}>Download all PDFs</DownloadLink>
          <div className="previews">
            {result.previews.map((preview) => (
              <figure key={preview.file_id}>
                <img src={fileUrl(preview.file_id)} alt={preview.name} />
                <figcaption>{preview.name}</figcaption>
              </figure>
            ))}
          </div>
        </Panel>
      ) : null}
    </>
  );
}
