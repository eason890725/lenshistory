// Server-side only: importing this from a 'use client' file would ship all of products.json to the browser.
import products from '@/data/products.json';
import type { Gear } from './gear';

export const gears = products as Gear[];

// The database grid gets every item, so send only what its cards, filters and sorting read (the full records are ~5 MB).
// The JSON round trip drops empty fields; React would otherwise send each one as "$undefined".
export const listGears: Gear[] = JSON.parse(JSON.stringify(gears.map((g): Gear => ({
  id: g.id, slug: g.slug, brand: g.brand, modelName: g.modelName, aliases: g.aliases, gearType: g.gearType,
  image_url: g.image_url, releaseYear: g.releaseYear, releaseMonth: g.releaseMonth,
  launchPrice: g.launchPrice, retailPrice: g.retailPrice, weightGrams: g.weightGrams,
  mounts: g.mounts?.map(m => ({ mount: { name: m.mount.name } })), lensMount: g.lensMount,
  sensorFormat: g.sensorFormat, megapixels: g.megapixels,
  focalLengthMinMm: g.focalLengthMinMm, focalLengthMaxMm: g.focalLengthMaxMm, apertureMax: g.apertureMax,
  accessoryType: g.accessoryType, magnification: g.magnification, guideNumber: g.guideNumber,
  filterKind: g.filterKind, filterSizes: g.filterSizes, maxHeight: g.maxHeight, maxLoad: g.maxLoad,
}))));

export function findGear(idOrSlug: string) {
  return gears.find(g => g.id === idOrSlug || g.slug === idOrSlug);
}

export function catalogueStats() {
  const years = gears.map(g => g.releaseYear).filter((y): y is number => !!y);
  return {
    count: gears.length,
    brands: new Set(gears.map(g => g.brand)).size,
    from: Math.min(...years),
    to: Math.max(...years),
  };
}

export type CompatLink = { kind: 'LENS' | 'CAMERA_BODY'; mount: string; count: number };

const mountNames = (g: Gear) => g.mounts?.map(m => m.mount.name) ?? [];
const newestFirst = (a: Gear, b: Gear) => (b.releaseYear ?? 0) * 100 + (b.releaseMonth ?? 0) - ((a.releaseYear ?? 0) * 100 + (a.releaseMonth ?? 0));

// What fits this item: counts of bodies / lenses per shared mount (shown as links to the filtered database),
// plus the specific items that name each other in compatibleWith or connect through an adapter.
export function compatibleFor(g: Gear): { links: CompatLink[]; items: Gear[] } {
  const links: CompatLink[] = [];
  const items = new Set<Gear>();
  const count = (kind: CompatLink['kind'], mount: string) =>
    gears.filter(x => x.gearType === kind && x.id !== g.id && mountNames(x).includes(mount)).length;
  const addLinks = (kind: CompatLink['kind'], mounts: string[]) => {
    for (const mount of mounts) {
      const n = count(kind, mount);
      if (n) links.push({ kind, mount, count: n });
    }
  };

  for (const x of gears) {
    if (x.id === g.id) continue;
    if (g.compatibleWith?.includes(x.id) || x.compatibleWith?.includes(g.id)) items.add(x);
  }

  if (g.gearType === 'CAMERA_BODY' && g.mounts?.length) {
    addLinks('LENS', mountNames(g));
    // Adapters whose camera side is this body's mount
    for (const x of gears) if (x.accessoryType === 'MOUNT_ADAPTER' && mountNames(x).some(m => mountNames(g).includes(m))) items.add(x);
  } else if (g.gearType === 'LENS') {
    addLinks('CAMERA_BODY', mountNames(g));
    // Adapters that take this lens's mount onto another system
    for (const x of gears) if (x.accessoryType === 'MOUNT_ADAPTER' && x.lensMount && mountNames(g).includes(x.lensMount)) items.add(x);
  } else if (g.accessoryType === 'MOUNT_ADAPTER') {
    if (g.lensMount) addLinks('LENS', [g.lensMount]);
    addLinks('CAMERA_BODY', mountNames(g));
  } else if (g.accessoryType === 'TELECONVERTER' && !g.compatibleWith?.length) {
    addLinks('CAMERA_BODY', mountNames(g));
  }

  return { links, items: [...items].sort(newestFirst) };
}
