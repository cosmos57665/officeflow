export const API_BASE = 'http://localhost:8000';

export type Health = {
  ok: boolean;
  demo_default: boolean;
  providers_available: string[];
  app_name: string;
};

async function parse<T>(response: Response): Promise<T> {
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(data.error || 'Request failed. Please try again.');
  }
  return data as T;
}

export async function getHealth() {
  return parse<Health>(await fetch(`${API_BASE}/api/health`));
}

export async function postJson<T>(path: string, body: unknown) {
  return parse<T>(
    await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
  );
}

export async function postForm<T>(path: string, form: FormData) {
  return parse<T>(await fetch(`${API_BASE}${path}`, { method: 'POST', body: form }));
}

export function fileUrl(fileId: string) {
  return `${API_BASE}/api/files/${fileId}`;
}
