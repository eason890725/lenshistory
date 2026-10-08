'use client';

import { useSyncExternalStore } from 'react';

const KEY = 'compare_ids';
const listeners = new Set<() => void>();

function subscribe(onChange: () => void) {
  listeners.add(onChange);
  window.addEventListener('storage', onChange);
  return () => {
    listeners.delete(onChange);
    window.removeEventListener('storage', onChange);
  };
}

function parse(raw: string): string[] {
  try {
    const ids = JSON.parse(raw);
    return Array.isArray(ids) ? ids.map(String) : [];
  } catch {
    return [];
  }
}

// Gear ids picked for comparison, kept in localStorage and shared by every component that uses this hook.
export function useCompareIds() {
  const raw = useSyncExternalStore(subscribe, () => localStorage.getItem(KEY) ?? '[]', () => '[]');
  const setIds = (ids: string[]) => {
    localStorage.setItem(KEY, JSON.stringify(ids));
    listeners.forEach(l => l());
  };
  return [parse(raw), setIds] as const;
}
