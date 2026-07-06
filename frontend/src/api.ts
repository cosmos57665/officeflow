export const API_BASE = 'http://localhost:8000';

export type Health = {
  ok: boolean;
  demo_default: boolean;
  providers_available: string[];
  app_name: string;
};

const BACKEND_DOWN = 'Backend is not reachable. Restart OfficeFlow or use the Streamlit fallback.';

async function parse<T>(response: Response): Promise<T> {
  let data: Record<string, unknown> = {};
  try {
    const text = await response.text();
    data = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(BACKEND_DOWN);
  }
  if (!response.ok) {
    throw new Error(typeof data.error === 'string' ? data.error : 'Request failed. Please try again.');
  }
  return data as T;
}

async function request<T>(input: RequestInfo | URL, init?: RequestInit) {
  try {
    return await parse<T>(await fetch(input, init));
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(BACKEND_DOWN);
    }
    throw error;
  }
}

export async function getHealth() {
  return request<Health>(`${API_BASE}/api/health`);
}

export async function postJson<T>(path: string, body: unknown) {
  return request<T>(
    `${API_BASE}${path}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }
  );
}

export async function postForm<T>(path: string, form: FormData) {
  return request<T>(`${API_BASE}${path}`, { method: 'POST', body: form });
}

export function fileUrl(fileId: string) {
  return `${API_BASE}/api/files/${fileId}`;
}
