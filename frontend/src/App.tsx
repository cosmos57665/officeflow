import { useEffect, useState } from 'react';
import type { ElementType } from 'react';
import { Bot, FileQuestion, FileText, Home, Inbox, Mic, WifiOff } from 'lucide-react';
import { getHealth } from './api';
import Ask from './screens/Ask';
import Docs from './screens/Docs';
import InboxScreen from './screens/Inbox';
import Minutes from './screens/Minutes';

type Page = 'Home' | 'Minutes' | 'Inbox' | 'Docs' | 'Ask';

const pages: { name: Page; icon: ElementType; text: string }[] = [
  { name: 'Home', icon: Home, text: 'Operations console' },
  { name: 'Minutes', icon: Mic, text: 'Audio to Word' },
  { name: 'Inbox', icon: Inbox, text: 'Email triage' },
  { name: 'Docs', icon: FileText, text: 'CSV to PDFs' },
  { name: 'Ask', icon: FileQuestion, text: 'PDF Q&A' }
];

function HomePage({ providers }: { providers: string[] }) {
  return (
    <>
      <section className="hero">
        <div>
          <span>Live demo operations console</span>
          <h1>OfficeFlow</h1>
          <p>Four office automation workflows in one reliable full-stack app.</p>
        </div>
        <div className="hero-status">
          <Bot size={28} />
          <strong>{providers.length ? providers.join(' -> ') : 'Demo Mode ready'}</strong>
          <small>AI providers are used only when Demo Mode is off.</small>
        </div>
      </section>
      <section className="workflow-grid">
        {[
          ['Meeting Minutes', 'Turns audio into structured Word minutes.', '~30 minutes saved'],
          ['Inbox Triage', 'Sorts pasted emails and drafts replies.', '~20 minutes saved'],
          ['Bulk Documents', 'Generates student PDFs from CSV rows.', '~5 minutes per document'],
          ['Ask PDF', 'Answers policy questions with page citations.', '~15 minutes saved']
        ].map(([title, text, metric]) => (
          <article className="workflow" key={title}>
            <h3>{title}</h3>
            <p>{text}</p>
            <strong>{metric}</strong>
          </article>
        ))}
      </section>
    </>
  );
}

export default function App() {
  const [page, setPage] = useState<Page>('Home');
  const [demo, setDemo] = useState(true);
  const [providers, setProviders] = useState<string[]>([]);

  useEffect(() => {
    getHealth()
      .then((health) => {
        setDemo(health.demo_default);
        setProviders(health.providers_available);
      })
      .catch(() => {
        setDemo(true);
        setProviders([]);
      });
  }, []);

  return (
    <div className="app">
      <aside>
        <div className="brand">
          <Bot size={24} />
          <div>
            <strong>OfficeFlow</strong>
            <small>AI Office Suite</small>
          </div>
        </div>
        <nav>
          {pages.map((item) => {
            const Icon = item.icon;
            return (
              <button className={page === item.name ? 'active' : ''} key={item.name} onClick={() => setPage(item.name)}>
                <Icon size={18} />
                <span>{item.name}</span>
                <small>{item.text}</small>
              </button>
            );
          })}
        </nav>
        <label className="toggle">
          <input type="checkbox" checked={demo} onChange={(event) => setDemo(event.target.checked)} />
          <span><WifiOff size={16} /> Demo Mode</span>
        </label>
        <p className="sidebar-note">Cached outputs keep the presentation moving without API or Wi-Fi.</p>
      </aside>
      <main>
        {page === 'Home' ? <HomePage providers={providers} /> : null}
        {page === 'Minutes' ? <Minutes demo={demo} /> : null}
        {page === 'Inbox' ? <InboxScreen demo={demo} /> : null}
        {page === 'Docs' ? <Docs demo={demo} /> : null}
        {page === 'Ask' ? <Ask demo={demo} /> : null}
      </main>
    </div>
  );
}
