import {createServer} from "node:http";
import {readFile, mkdir} from "node:fs/promises";
import {extname, join, resolve} from "node:path";
import {fileURLToPath} from "node:url";
import {chromium} from "playwright";

const here = fileURLToPath(new URL(".", import.meta.url));
const repo = resolve(here, "..", "..");
const dist = join(repo, "frontend", "dist");
const output = join(repo, "video", "public", "screens");
const previewDir = join(repo, "outputs", "previews");

const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".png": "image/png",
};

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url ?? "/", "http://127.0.0.1:4173");
    const relative = url.pathname === "/" ? "index.html" : url.pathname.slice(1);
    const path = join(dist, relative);
    const body = await readFile(path);
    response.writeHead(200, {"Content-Type": mime[extname(path)] ?? "application/octet-stream"});
    response.end(body);
  } catch {
    response.writeHead(404);
    response.end("Not found");
  }
});

const json = async (name) =>
  JSON.parse(await readFile(join(repo, "cache", name), "utf8"));

const fixtures = {
  health: {demo_default: true, providers_available: ["gemini", "groq", "openrouter"]},
  minutes: {
    data: await json("minutes_sample.json"),
    elapsed: 1.8,
    provider: "demo-cache",
    docx_file_id: "minutes.docx",
  },
  inbox: {
    emails: await json("inbox_sample.json"),
    elapsed: 1.4,
    provider: "demo-cache",
  },
  documents: {
    count: 20,
    elapsed: 2.6,
    provider: "demo-cache",
    zip_file_id: "certificates.zip",
    previews: [
      {file_id: "preview-1.png", name: "01_Aarav_Sharma.png"},
      {file_id: "preview-2.png", name: "02_Diya_Patel.png"},
      {file_id: "preview-3.png", name: "03_Rohan_Verma.png"},
    ],
  },
  ask: {
    answer: (await json("ask_sample.json"))["What is the deadline for reimbursement claims?"],
    elapsed: 0.9,
    provider: "demo-cache",
  },
};

const apiFixture = (url) => {
  const path = new URL(url).pathname;
  if (path === "/api/health") return fixtures.health;
  if (path === "/api/minutes") return fixtures.minutes;
  if (path === "/api/inbox") return fixtures.inbox;
  if (path === "/api/docs") return fixtures.documents;
  if (path === "/api/ask/load") return {doc_id: "demo-policy", pages: 6, words: 882};
  if (path === "/api/ask/question") return fixtures.ask;
  return null;
};

await mkdir(output, {recursive: true});
await new Promise((resolveReady) => server.listen(4173, "127.0.0.1", resolveReady));

const browser = await chromium.launch({
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  headless: true,
});
const page = await browser.newPage({viewport: {width: 1440, height: 900}, deviceScaleFactor: 1});

await page.route("http://localhost:8000/api/**", async (route) => {
  const path = new URL(route.request().url()).pathname;
  if (path.startsWith("/api/files/preview-")) {
    const index = Number(path.match(/preview-(\d)/)?.[1] ?? 1);
    const names = ["01_Aarav_Sharma.png", "02_Diya_Patel.png", "03_Rohan_Verma.png"];
    await route.fulfill({
      status: 200,
      contentType: "image/png",
      body: await readFile(join(previewDir, names[index - 1])),
    });
    return;
  }
  const body = apiFixture(route.request().url());
  await route.fulfill({
    status: body ? 200 : 404,
    contentType: "application/json",
    body: JSON.stringify(body ?? {error: "Not found"}),
  });
});

const snap = async (name) => {
  await page.screenshot({path: join(output, `${name}.png`), animations: "disabled"});
};

try {
  await page.goto("http://127.0.0.1:4173", {waitUntil: "networkidle"});
  await page.getByRole("heading", {name: "OfficeFlow"}).waitFor();
  await snap("home");

  await page.getByRole("button", {name: /^Minutes/}).click();
  await page.getByRole("button", {name: "Use sample audio"}).click();
  await page.getByRole("heading", {name: "Generated minutes"}).waitFor();
  await page.getByRole("heading", {name: "Generated minutes"}).scrollIntoViewIfNeeded();
  await snap("minutes");

  await page.getByRole("button", {name: /^Inbox/}).click();
  await page.getByRole("button", {name: "Load sample emails"}).click();
  await page.getByRole("button", {name: "Triage Inbox"}).click();
  await page.getByText(/8 emails triaged/).waitFor();
  await page.getByText(/8 emails triaged/).scrollIntoViewIfNeeded();
  await snap("inbox");

  await page.getByRole("button", {name: /^Docs/}).click();
  await page.getByRole("button", {name: "Use sample CSV"}).click();
  await page.getByText(/Generated 20 PDFs/).waitFor();
  await page.getByRole("heading", {name: "Generated documents"}).scrollIntoViewIfNeeded();
  await snap("documents");

  await page.getByRole("button", {name: /^Ask/}).click();
  await page.getByRole("button", {name: "Ask Question"}).click();
  await page.getByText(/15 calendar days/).waitFor();
  await page.getByText(/15 calendar days/).scrollIntoViewIfNeeded();
  await snap("ask");
} finally {
  await browser.close();
  await new Promise((resolveDone) => server.close(resolveDone));
}
