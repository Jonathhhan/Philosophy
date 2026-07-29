import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const outputDirectory = join(root, 'dist', 'server');

const [html, css, javascript] = await Promise.all([
  readFile(join(root, 'index.html'), 'utf8'),
  readFile(join(root, 'css', 'main.css'), 'utf8'),
  readFile(join(root, 'js', 'main.js'), 'utf8')
]);

const assets = [
  ['/', { body: html, contentType: 'text/html; charset=utf-8' }],
  ['/index.html', { body: html, contentType: 'text/html; charset=utf-8' }],
  ['/css/main.css', { body: css, contentType: 'text/css; charset=utf-8' }],
  ['/js/main.js', { body: javascript, contentType: 'text/javascript; charset=utf-8' }]
];

const contentSecurityPolicy = `default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'`;

const workerSource = `const assets = new Map(${JSON.stringify(assets)});

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const asset = assets.get(url.pathname);

    if (!asset) {
      return new Response('Nicht gefunden', { status: 404 });
    }

    return new Response(asset.body, {
      headers: {
        'Content-Type': asset.contentType,
        'Cache-Control': url.pathname === '/' || url.pathname === '/index.html' ? 'no-cache' : 'public, max-age=3600',
        'Content-Security-Policy': ${JSON.stringify(contentSecurityPolicy)},
        'Referrer-Policy': 'no-referrer',
        'X-Content-Type-Options': 'nosniff'
      }
    });
  }
};
`;

await rm(join(root, 'dist'), { recursive: true, force: true });
await mkdir(outputDirectory, { recursive: true });
await writeFile(join(outputDirectory, 'index.js'), workerSource, 'utf8');

console.log('Built Anschlusslabor worker.');
