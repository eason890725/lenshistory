// Checks src/data/products.json before every build (npm run validate / prebuild).
// Errors fail the build; warnings are printed only.
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, relative } from 'node:path';

const root = new URL('..', import.meta.url).pathname.replace(/^\/(\w:)/, '$1');
const items = JSON.parse(readFileSync(process.argv[2] ?? join(root, 'src/data/products.json'), 'utf8'));

const SHARED = ['id', 'slug', 'brand', 'modelName', 'gearType', 'aliases', 'image_url', 'officialUrl', 'mounts', 'sensorFormat', 'series',
  'category', 'releaseYear', 'launchPrice', 'weightGrams', 'dimensions', 'hasWeatherSeal'];
const LENS = ['lensType', 'focalLengthMinMm', 'focalLengthMaxMm', 'apertureMax', 'minAperture', 'maxMagnification', 'closeFocus',
  'filterSizeMm', 'motorType', 'opticalDesign', 'specialElements', 'coatings', 'hasOIS', 'hasApertureRing', 'hasCustomButton'];
const BODY = ['megapixels', 'sensorType', 'processor', 'isoRange', 'burstSpeed', 'afPoints', 'afTargets', 'afRange', 'hasIBIS',
  'ibisRating', 'videoResolution', 'videoColorDepth', 'logSupport', 'evfResolution', 'evfMagnification', 'lcdSpec', 'cardSlots',
  'batterySpec', 'ports'];
const ALLOWED = { LENS: new Set([...SHARED, ...LENS]), CAMERA_BODY: new Set([...SHARED, ...BODY]) };
const NUMBER = ['releaseYear', 'launchPrice', 'focalLengthMinMm', 'focalLengthMaxMm', 'filterSizeMm'];
const JUNK = new Set(['', '--', 'N/A', 'TBD', 'TBD / Professional Standard']);
const MOUNTS = new Set(['Sony E', 'Canon RF', 'Nikon Z', 'Fujifilm X', 'Fujifilm G', 'L-Mount', 'Leica M', 'Hasselblad X', 'Canon EF', 'Nikon F', 'Micro Four Thirds']);
const FORMATS = new Set(['Full Frame', 'APS-C', 'Medium Format', '1-inch']);
// House style for free-text fields (scripts/normalize_products.py rewrites most variants into these)
const STYLE = {
  closeFocus: /^\d+(\.\d+)?m\b/,
  maxMagnification: /^\d+(\.\d+)?x\b/,
  opticalDesign: /^\d+ elements in \d+ groups$/,
  megapixels: /^\d+(\.\d+)?MP\b/,
  burstSpeed: /^\d+(\.\d+)?fps\b/,
  dimensions: /^(Ø[\d.]+ x [\d.]+ mm|[\d.]+ x [\d.]+ x [\d.]+ mm)/,
  ibisRating: /^[\d.]+(-[\d.]+)? stops/,
};

const errors = [];
const warnings = [];
const seen = { id: new Set(), slug: new Set() };

for (const g of items) {
  const at = `${g.id ?? '(no id)'}`;
  const err = msg => errors.push(`${at}: ${msg}`);

  for (const k of ['id', 'brand', 'modelName']) if (typeof g[k] !== 'string' || !g[k]) err(`missing ${k}`);
  if (!ALLOWED[g.gearType]) { err(`gearType must be LENS or CAMERA_BODY, got ${g.gearType}`); continue; }
  for (const k of ['id', 'slug']) {
    if (g[k] === undefined) continue;
    if (seen[k].has(g[k])) err(`duplicate ${k}`);
    seen[k].add(g[k]);
  }

  for (const [k, v] of Object.entries(g)) {
    if (!ALLOWED[g.gearType].has(k)) err(`unknown field "${k}" for ${g.gearType} (add it to src/lib/gear.ts and this script, or rename it)`);
    if (typeof v === 'string' && JUNK.has(v.trim())) err(`placeholder value in ${k}: "${v}" (leave the field out instead)`);
    if (NUMBER.includes(k) && typeof v !== 'number') err(`${k} must be a number, got ${JSON.stringify(v)}`);
    if (k.startsWith('has') && typeof v !== 'boolean') err(`${k} must be true/false`);
    if (STYLE[k] && !STYLE[k].test(String(v))) err(`${k} not in house style: "${v}" (run scripts/normalize_products.py or fix by hand)`);
  }
  if (g.sensorFormat && !FORMATS.has(g.sensorFormat)) err(`sensorFormat must be one of ${[...FORMATS].join(', ')}`);
  for (const m of g.mounts ?? []) if (!MOUNTS.has(m?.mount?.name)) err(`unknown mount "${m?.mount?.name}"`);

  if (g.launchPrice !== undefined && !(g.launchPrice > 0)) err('launchPrice must be > 0 (leave it out when unknown)');
  if (g.image_url && !existsSync(join(root, 'public', g.image_url))) err(`image not found: ${g.image_url}`);
  if (g.mounts && !(Array.isArray(g.mounts) && g.mounts.every(m => typeof m?.mount?.name === 'string'))) {
    err('mounts must look like [{ "mount": { "name": "Sony E" } }]');
  }
}

// The same price on many items is how the old 39980 / 0 placeholders looked
const prices = {};
for (const g of items) if (g.launchPrice) prices[g.launchPrice] = (prices[g.launchPrice] || 0) + 1;
for (const [p, n] of Object.entries(prices)) if (n > 8) warnings.push(`launchPrice ${p} is used by ${n} items, check it is not a placeholder`);

const used = new Set(items.map(g => g.image_url));
const walk = dir => readdirSync(dir, { withFileTypes: true }).flatMap(e => (e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)]));
for (const f of walk(join(root, 'public/images/products'))) {
  const url = '/' + relative(join(root, 'public'), f).replaceAll('\\', '/');
  if (!used.has(url)) warnings.push(`image not used by any product: ${url}`);
}

for (const w of warnings) console.warn(`warn  ${w}`);
for (const e of errors) console.error(`error ${e}`);
console.log(`products.json: ${items.length} items, ${errors.length} errors, ${warnings.length} warnings`);
process.exit(errors.length ? 1 : 0);
