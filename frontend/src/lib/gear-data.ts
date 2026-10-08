// Server-side only: importing this from a 'use client' file would ship all of products.json to the browser.
import products from '@/data/products.json';
import type { Gear } from './gear';

export const gears = products as Gear[];

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
