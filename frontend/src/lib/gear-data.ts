// Server-side only: importing this from a 'use client' file would ship all of products.json to the browser.
import products from '@/data/products.json';
import type { Gear } from './gear';

export const gears = products as Gear[];

export function findGear(idOrSlug: string) {
  return gears.find(g => g.id === idOrSlug || g.slug === idOrSlug);
}
