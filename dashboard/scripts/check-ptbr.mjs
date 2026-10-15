#!/usr/bin/env node
// Validate the untranslated bundle, before the English fallback can mask gaps.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src/i18n/locales');
const sharedTerms = new Set([
  'Backup', 'Status', 'JSON', 'watchtower', 'Tag', 'Chat', 'Bot', 'Plugins',
  'Console', 'GitHub', 'Plugin', 'Local', 'Online', 'Offline', 'WebUI', 'AstrBot',
  'Normal', 'SSE', 'WebSocket', 'Tokens', 'Dify', 'Coze', 'DeerFlow', 'Persona',
  'string', 'int', 'Regex', 'TOTP', 'Top-p', 'Volume', 'Alibaba Cloud Model Studio',
  'UMO', 'Experimental', 'Cron', 'local', 'Total', 'MCP', 'Downloads',
  'Plugin: {plugin}', 'logo', 'Personas', 'Bots', 'Token', 'Feishu China',
  'Lark Global', 'SSYCloud', 'Proxy', 'OpenAPI', 'Cache', 'cache', 'CPU', 'TPM',
  'transfer_to_{name}', 'Persona: {id}', 'ModelScope', 'Beta',
  '{used} / {limit} tokens ({percent}%)'
]);

function flatten(value, prefix = '', result = new Map()) {
  if (value && typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) {
      flatten(child, prefix ? `${prefix}.${key}` : key, result);
    }
  } else result.set(prefix, value);
  return result;
}

function* files(dir, prefix = '') {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const name = path.join(prefix, entry.name);
    if (entry.isDirectory()) yield* files(path.join(dir, entry.name), name);
    else if (entry.name.endsWith('.json')) yield name;
  }
}

const read = file => JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const markers = value => [...value.matchAll(/\{[A-Za-z_][A-Za-z0-9_]*\}/g)]
  .map(match => match[0]).sort().join('|');
const problems = [];
let checked = 0;
for (const file of files(path.join(root, 'en-US'))) {
  const target = path.join(root, 'pt-BR', file);
  if (!fs.existsSync(target)) { problems.push(`${file}: missing file`); continue; }
  const english = flatten(read(path.join(root, 'en-US', file)));
  const portuguese = flatten(read(target));
  for (const [key, original] of english) {
    const translated = portuguese.get(key);
    const label = `${file}:${key}`;
    if (!portuguese.has(key)) { problems.push(`${label}: missing translation`); continue; }
    if (typeof original !== typeof translated) { problems.push(`${label}: changed value type`); continue; }
    if (typeof original !== 'string') continue;
    checked++;
    if (original.trim() && !translated.trim()) problems.push(`${label}: empty translation`);
    if (markers(original) !== markers(translated)) problems.push(`${label}: interpolation mismatch`);
    if (/[\u4e00-\u9fff]/.test(translated)) problems.push(`${label}: unexpected Chinese text`);
    if (original === translated && /[A-Za-z]{3}/.test(original) &&
        !sharedTerms.has(original) &&
        /[A-Za-z]{3}/.test(original.replace(/\{[^{}]*\}/g, ''))) {
      problems.push(`${label}: untranslated English text (${original})`);
    }
  }
}
if (problems.length) {
  console.error(problems.join('\n'));
  process.exit(1);
}
console.log(`pt-BR: ${checked} text entries checked; no missing translations, leaked English or broken placeholders.`);
