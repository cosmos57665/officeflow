import { AlertCircle, CheckCircle2, Download, Loader2 } from 'lucide-react';
import type { ButtonHTMLAttributes, ReactNode } from 'react';
import { fileUrl } from './api';

export function Panel({ children, title }: { children: ReactNode; title?: string }) {
  return (
    <section className="panel">
      {title ? <h2>{title}</h2> : null}
      {children}
    </section>
  );
}

export function ModuleHeader({ kicker, title, text }: { kicker: string; title: string; text: string }) {
  return (
    <header className="module-head">
      <span>{kicker}</span>
      <h1>{title}</h1>
      <p>{text}</p>
    </header>
  );
}

export function Notice({ kind, children }: { kind: 'error' | 'success' | 'info'; children: ReactNode }) {
  const Icon = kind === 'error' ? AlertCircle : CheckCircle2;
  return (
    <div className={`notice ${kind}`}>
      <Icon size={18} />
      <span>{children}</span>
    </div>
  );
}

export function PrimaryButton({ busy, children, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { busy?: boolean }) {
  return (
    <button className="primary" disabled={busy || props.disabled} {...props}>
      {busy ? <Loader2 className="spin" size={18} /> : null}
      {children}
    </button>
  );
}

export function DownloadLink({ fileId, children }: { fileId: string; children: ReactNode }) {
  return (
    <a className="download" href={fileUrl(fileId)}>
      <Download size={17} />
      {children}
    </a>
  );
}
