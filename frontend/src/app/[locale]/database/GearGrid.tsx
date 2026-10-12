'use client';

import { useState, useEffect } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/routing';
import ProductCard from '@/components/gear/ProductCard';
import { weightValue, type Gear } from '@/lib/gear';
import { useCompareIds } from '@/lib/compare';
import FilterPanel, { EMPTY_FILTERS, PRICE_MAX, YEAR_MAX, YEAR_MIN, type FilterState } from './FilterPanel';

function filtersFromParams(p: Pick<URLSearchParams, 'get'>): FilterState {
  const list = (k: string) => p.get(k)?.split(',') ?? [];
  const int = (k: string, fallback: number) => (p.get(k) ? parseInt(p.get(k)!) : fallback);
  return {
    q: p.get('q') ?? '',
    sortBy: p.get('sortBy') ?? 'newest',
    minPrice: int('minP', 0),
    maxPrice: int('maxP', PRICE_MAX),
    minYear: int('minY', YEAR_MIN),
    maxYear: int('maxY', YEAR_MAX),
    sensorFormats: list('formats'),
    gearTypes: list('gearTypes'),
    brands: list('brands'),
    mounts: list('mounts'),
  };
}

function matches(g: Gear, f: FilterState) {
  if (f.q) {
    const q = f.q.toLowerCase();
    const hit = g.modelName.toLowerCase().includes(q) || g.brand.toLowerCase().includes(q) || (g.aliases || []).some(a => a.toLowerCase().includes(q));
    if (!hit) return false;
  }
  if (f.gearTypes.length && !f.gearTypes.includes(g.gearType)) return false;
  if (f.brands.length && !f.brands.includes(g.brand)) return false;
  // The slider's top position means "MAX", i.e. no upper limit
  const price = g.launchPrice;
  if (price && (price < f.minPrice || (f.maxPrice < PRICE_MAX && price > f.maxPrice))) return false;
  const year = g.releaseYear;
  if (year && (year < f.minYear || year > f.maxYear)) return false;
  if (f.sensorFormats.length && !f.sensorFormats.includes(g.sensorFormat ?? '')) return false;
  if (f.mounts.length && !f.mounts.some(m => g.mounts?.some(gm => gm.mount.name === m))) return false;
  return true;
}

function compareGears(sortBy: string) {
  return (a: Gear, b: Gear) => {
    switch (sortBy) {
      case 'newest': return (b.releaseYear || 0) - (a.releaseYear || 0);
      case 'oldest': return (a.releaseYear || 0) - (b.releaseYear || 0);
      case 'priceDesc': return (b.launchPrice || 0) - (a.launchPrice || 0);
      case 'priceAsc': return (a.launchPrice || 1e9) - (b.launchPrice || 1e9);
      case 'weightAsc': return (weightValue(a) || 1e5) - (weightValue(b) || 1e5);
      case 'mpDesc': return (parseFloat(String(b.megapixels)) || 0) - (parseFloat(String(a.megapixels)) || 0);
      // Lenses by widest focal length, then longest; bodies (no focal length) go last either way
      case 'focalAsc':
      case 'focalDesc': {
        const dir = sortBy === 'focalAsc' ? 1 : -1;
        const fa = a.focalLengthMinMm, fb = b.focalLengthMinMm;
        if (!fa || !fb) return (fa ? -1 : 0) - (fb ? -1 : 0);
        return dir * (fa - fb || (a.focalLengthMaxMm || fa) - (b.focalLengthMaxMm || fb));
      }
      default: return 0;
    }
  };
}

export default function GearGrid({ gears }: { gears: Gear[] }) {
  const searchParams = useSearchParams();
  const [filters, setFilters] = useState<FilterState>(() => filtersFromParams(searchParams));
  const [sheetOpen, setSheetOpen] = useState(false);
  const [storedIds, setSelectedIds] = useCompareIds();
  // Drop ids that no longer exist (e.g. merged duplicates) so they can't lock the type filter
  const selectedIds = storedIds.filter(id => gears.some(g => g.id === id));
  const selectedType = gears.find(g => g.id === selectedIds[0])?.gearType ?? null;

  const router = useRouter();
  const pathname = usePathname();
  const t = useTranslations('GearSpecs');
  const tc = useTranslations('Common');

  const brandCounts = Object.entries(
    gears.reduce<Record<string, number>>((acc, g) => ({ ...acc, [g.brand]: (acc[g.brand] || 0) + 1 }), {})
  ).sort((a, b) => b[1] - a[1]);
  const mountOptions = [...new Set(gears.flatMap(g => g.mounts?.map(m => m.mount.name) ?? []))].sort();

  const results = gears.filter(g => matches(g, filters)).sort(compareGears(filters.sortBy));

  // Restore scroll position when coming back from a detail page
  useEffect(() => {
    window.history.scrollRestoration = 'manual';
    const saved = sessionStorage.getItem('database_scroll');
    if (saved) {
      let attempts = 0;
      const target = parseInt(saved);
      const restore = () => {
        window.scrollTo({ top: target, behavior: 'instant' });
        if (++attempts < 10) requestAnimationFrame(restore);
      };
      requestAnimationFrame(restore);
    }

    let saveTimeout: ReturnType<typeof setTimeout> | undefined;
    const onScroll = () => {
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => sessionStorage.setItem('database_scroll', String(window.scrollY)), 100);
    };
    window.addEventListener('scroll', onScroll);
    return () => {
      window.removeEventListener('scroll', onScroll);
      clearTimeout(saveTimeout);
    };
  }, []);

  // Keep the filters in the URL so back/forward and shared links restore them
  useEffect(() => {
    const p = new URLSearchParams();
    if (filters.q) p.set('q', filters.q);
    if (filters.brands.length) p.set('brands', filters.brands.join(','));
    if (filters.gearTypes.length) p.set('gearTypes', filters.gearTypes.join(','));
    if (filters.sensorFormats.length) p.set('formats', filters.sensorFormats.join(','));
    if (filters.mounts.length) p.set('mounts', filters.mounts.join(','));
    if (filters.sortBy !== 'newest') p.set('sortBy', filters.sortBy);
    if (filters.minPrice > 0) p.set('minP', String(filters.minPrice));
    if (filters.maxPrice < PRICE_MAX) p.set('maxP', String(filters.maxPrice));
    if (filters.minYear > YEAR_MIN) p.set('minY', String(filters.minYear));
    if (filters.maxYear < YEAR_MAX) p.set('maxY', String(filters.maxYear));
    const query = p.toString();
    window.history.replaceState(null, '', query ? `${pathname}?${query}` : pathname);
  }, [filters, pathname]);

  const toggleCompare = (gear: Gear) => {
    const isSelected = selectedIds.includes(gear.id);
    if (!isSelected && selectedType && selectedType !== gear.gearType) return;
    setSelectedIds(isSelected ? selectedIds.filter(i => i !== gear.id) : [...selectedIds, gear.id]);
  };

  const activeCount =
    filters.brands.length + filters.gearTypes.length + filters.mounts.length + filters.sensorFormats.length +
    (filters.q ? 1 : 0) + (filters.maxPrice < PRICE_MAX ? 1 : 0) + (filters.minYear > YEAR_MIN || filters.maxYear < YEAR_MAX ? 1 : 0);

  return (
    <div className="grid gap-[var(--space-xl)] lg:grid-cols-[16rem_minmax(0,1fr)]">
      {/* Filters: sidebar on desktop, a sheet on small screens */}
      <div className="lg:hidden">
        <button
          type="button"
          onClick={() => setSheetOpen(true)}
          className="flex h-11 w-full items-center justify-between border border-rule-2 px-[var(--space-md)] text-sm text-ink"
        >
          <span>{tc('filters')}</span>
          {activeCount > 0 && <span className="font-mono text-xs text-accent tnum">{activeCount}</span>}
        </button>
      </div>

      <aside
        className={`${sheetOpen ? 'fixed inset-0 z-40 overflow-y-auto bg-paper px-[var(--page-gutter)] py-[var(--space-lg)]' : 'hidden'} lg:sticky lg:top-[var(--space-lg)] lg:block lg:max-h-[calc(100dvh-var(--space-xl))] lg:self-start lg:overflow-y-auto lg:p-0`}
      >
        <div className="mb-[var(--space-md)] flex items-center justify-between lg:hidden">
          <h2 className="text-lg font-bold">{tc('filters')}</h2>
          <button type="button" onClick={() => setSheetOpen(false)} className="link-type min-h-11 text-sm">
            {tc('applyFilters')}
          </button>
        </div>
        <FilterPanel filters={filters} setFilters={setFilters} brandCounts={brandCounts} mountOptions={mountOptions} />
      </aside>

      <section aria-live="polite" className="min-w-0">
        <p className="label mb-[var(--space-md)] tnum">{tc('resultsCount', { count: results.length })}</p>
        {results.length > 0 ? (
          <div className="grid grid-cols-[repeat(2,minmax(0,1fr))] gap-x-[var(--space-lg)] gap-y-[var(--space-xl)] md:grid-cols-[repeat(3,minmax(0,1fr))] xl:grid-cols-[repeat(4,minmax(0,1fr))]">
            {results.map((gear, i) => (
              <ProductCard
                key={gear.id}
                gear={gear}
                priority={i < 4}
                noImageLabel={t('noImage')}
                compare={{
                  selected: selectedIds.includes(gear.id),
                  disabled: !!selectedType && selectedType !== gear.gearType && !selectedIds.includes(gear.id),
                  onToggle: toggleCompare,
                  labels: { add: tc('addCompare'), remove: tc('inCompare'), mixed: tc('cannotMixComparison') },
                }}
              />
            ))}
          </div>
        ) : (
          <div className="border-t border-rule py-[var(--space-2xl)]">
            <p className="font-display text-lg font-bold">{tc('noResults')}</p>
            <p className="mt-[var(--space-xs)] text-sm text-muted">{tc('noResultsHint')}</p>
            <button type="button" onClick={() => setFilters(EMPTY_FILTERS)} className="link-type mt-[var(--space-md)] min-h-11 text-sm">
              {tc('resetFilters')}
            </button>
          </div>
        )}
      </section>

      {/* C4 sticky bottom bar for the compare selection */}
      {selectedIds.length > 0 && (
        <div className="fixed inset-x-0 bottom-0 z-30 border-t border-rule-2 bg-paper px-[var(--page-gutter)] py-[var(--space-sm)]">
          <div className="mx-auto flex max-w-[var(--page-max)] items-center justify-between gap-[var(--space-md)]">
            <p className="truncate text-sm text-ink-2 tnum">
              {selectedIds.length} {tc('itemsSelected')} · {selectedType === 'LENS' ? t('lens') : t('body')}
            </p>
            <div className="flex shrink-0 items-center gap-[var(--space-md)]">
              <button type="button" onClick={() => setSelectedIds([])} className="link-type min-h-11 text-sm text-ink-2">
                {tc('clear')}
              </button>
              <button
                type="button"
                onClick={() => router.push(`/compare?ids=${selectedIds.join(',')}`)}
                className="h-11 whitespace-nowrap bg-accent px-[var(--space-lg)] text-sm font-bold text-accent-ink transition-colors duration-[var(--dur-short)] ease-out hover:bg-ink"
              >
                {tc('compareNow', { count: selectedIds.length })}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
