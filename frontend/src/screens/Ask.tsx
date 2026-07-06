import { useState } from 'react';
import { ModuleHeader, Notice, Panel, PrimaryButton } from '../components';
import { postForm, postJson } from '../api';

type Loaded = { doc_id: string; pages: number; words: number; warning?: string };
type Answer = { answer: string; elapsed: number; provider: string };
type Chat = { question: string; result: Answer };

export default function Ask({ demo }: { demo: boolean }) {
  const [file, setFile] = useState<File | null>(null);
  const [loaded, setLoaded] = useState<Loaded | null>(null);
  const [question, setQuestion] = useState('What is the deadline for reimbursement claims?');
  const [chat, setChat] = useState<Chat[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function loadPdf() {
    if (!file) return setError('Please upload a PDF file.');
    setBusy(true);
    setError('');
    try {
      const form = new FormData();
      form.set('pdf', file);
      setLoaded(await postForm<Loaded>('/api/ask/load', form));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not read PDF.');
    } finally {
      setBusy(false);
    }
  }

  async function ask() {
    setBusy(true);
    setError('');
    try {
      const result = await postJson<Answer>('/api/ask/question', { doc_id: loaded?.doc_id, question, demo });
      setChat((items) => [...items, { question, result }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not answer question.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <ModuleHeader kicker="Module 04" title="Ask PDF" text="Ask cited questions from an office PDF." />
      <Panel title="Document">
        <input type="file" accept=".pdf" onChange={(event) => setFile(event.target.files?.[0] || null)} />
        <div className="actions">
          <PrimaryButton busy={busy} onClick={loadPdf}>Load PDF</PrimaryButton>
        </div>
        {loaded ? <Notice kind="success">Loaded {loaded.pages} pages and about {loaded.words} words.</Notice> : null}
        {loaded?.warning ? <Notice kind="info">{loaded.warning}</Notice> : null}
        {demo ? <p className="hint">Demo Mode can answer cached sample questions without loading a PDF.</p> : null}
      </Panel>
      <Panel title="Question">
        <input value={question} onChange={(event) => setQuestion(event.target.value)} />
        <div className="actions">
          <PrimaryButton busy={busy} onClick={ask}>Ask Question</PrimaryButton>
        </div>
      </Panel>
      {error ? <Notice kind="error">{error}</Notice> : null}
      {chat.map((item, index) => (
        <Panel key={`${item.question}-${index}`}>
          <p className="question">{item.question}</p>
          <p>{item.result.answer}</p>
          <small>Answered in {item.result.elapsed.toFixed(1)} seconds via {item.result.provider}.</small>
        </Panel>
      ))}
    </>
  );
}
