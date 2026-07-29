import { copyFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
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

const workerSource = `const assets = new Map(${JSON.stringify(assets)});
import { createWorker } from './runtime.js';
export default createWorker(assets);
`;
await rm(join(root, 'dist'), { recursive: true, force: true });
await mkdir(outputDirectory, { recursive: true });
await writeFile(join(outputDirectory, 'index.js'), workerSource, 'utf8');
await copyFile(join(root, 'server', 'runtime.js'), join(outputDirectory, 'runtime.js'));

console.log('Built Anschlusslabor worker.');
