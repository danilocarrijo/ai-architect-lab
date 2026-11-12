import fs from 'node:fs/promises';
import path from 'node:path';

function parseFrontmatter(raw) {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) return { meta: {}, body: raw };
  const meta = Object.fromEntries(
    m[1].split('\n').map((l) => l.split(/:\s*/, 2)).filter((p) => p[0]),
  );
  return { meta, body: m[2] };
}

export async function loadDocuments(dir) {
  const files = (await fs.readdir(dir)).filter((f) => f.endsWith('.md'));
  return Promise.all(
    files.map(async (f) => {
      const raw = (await fs.readFile(path.join(dir, f), 'utf8')).replace(/\r\n/g, '\n');
      const { meta, body } = parseFrontmatter(raw);
      return { id: f.replace(/\.md$/, ''), source: f, meta, body };
    }),
  );
}
