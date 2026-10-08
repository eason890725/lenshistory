'use client';

import { useTranslations } from 'next-intl';

export interface FilterState {
  q: string;
  sortBy: string;
  minPrice: number;
  maxPrice: number;
  minYear: number;
  maxYear: number;
  sensorFormats: string[];
  gearTypes: string[];
  brands: string[];
  mounts: string[];
}

export const PRICE_MAX = 200000;
export const YEAR_MIN = 2010;
export const YEAR_MAX = 2026;

export const EMPTY_FILTERS: FilterState = {
  q: '',
  sortBy: 'newest',
  minPrice: 0,
  maxPrice: PRICE_MAX,
  minYear: YEAR_MIN,
  maxYear: YEAR_MAX,
  sensorFormats: [],
  gearTypes: [],
  brands: [],
  mounts: [],
};

const FORMATS = ['Full Frame', 'APS-C', 'Medium Format'];
const YEARS = [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026];

function toggle(list: string[], value: string) {
  return list.includes(value) ? list.filter(v => v !== value) : [...list, value];
}

function Chip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={`min-h-9 whitespace-nowrap border px-[var(--space-sm)] text-sm transition-colors duration-[var(--dur-short)] ease-out ${
        active ? 'border-ink bg-ink text-paper' : 'border-rule-2 text-ink-2 hover:border-ink hover:text-ink'
      }`}
    >
      {children}
    </button>
  );
}

function Group({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <fieldset className="border-t border-rule py-[var(--space-md)]">
      <legend className="label float-left mb-[var(--space-sm)] w-full">{label}</legend>
      <div className="clear-both">{children}</div>
    </fieldset>
  );
}

export default function FilterPanel({
  filters,
  setFilters,
  brandCounts,
  mountOptions,
}: {
  filters: FilterState;
  setFilters: (f: FilterState) => void;
  brandCounts: [string, number][];
  mountOptions: string[];
}) {
  const t = useTranslations('GearSpecs');
  const tc = useTranslations('Common');
  const set = (patch: Partial<FilterState>) => setFilters({ ...filters, ...patch });

  return (
    <div className="text-sm">
      <label className="block pb-[var(--space-md)]">
        <span className="label mb-[var(--space-xs)] block">{tc('search')}</span>
        <input
          type="search"
          value={filters.q}
          onChange={e => set({ q: e.target.value })}
          placeholder="α7 IV · 24-70 · Z8"
          className="h-11 w-full border border-rule-2 bg-paper px-[var(--space-sm)] text-base text-ink placeholder:text-muted focus-visible:border-ink"
        />
      </label>

      <label className="block border-t border-rule py-[var(--space-md)]">
        <span className="label mb-[var(--space-xs)] block">{tc('sortBy')}</span>
        <select
          value={filters.sortBy}
          onChange={e => set({ sortBy: e.target.value })}
          className="h-11 w-full border border-rule-2 bg-paper px-[var(--space-sm)] text-ink"
        >
          <option value="newest">{tc('newest')}</option>
          <option value="oldest">{tc('oldest')}</option>
          <option value="priceDesc">{tc('priceHighToLow')}</option>
          <option value="priceAsc">{tc('priceLowToHigh')}</option>
          <option value="weightAsc">{tc('weightLightest')}</option>
          <option value="mpDesc">{tc('megapixelsHighest')}</option>
        </select>
      </label>

      <Group label={t('gearType')}>
        <div className="flex flex-wrap gap-[var(--space-xs)]">
          {(['CAMERA_BODY', 'LENS'] as const).map(type => (
            <Chip key={type} active={filters.gearTypes.includes(type)} onClick={() => set({ gearTypes: toggle(filters.gearTypes, type) })}>
              {type === 'LENS' ? t('lens') : t('body')}
            </Chip>
          ))}
        </div>
      </Group>

      <Group label={tc('brands')}>
        <div className="flex flex-wrap gap-[var(--space-xs)]">
          {brandCounts.map(([brand, count]) => (
            <Chip key={brand} active={filters.brands.includes(brand)} onClick={() => set({ brands: toggle(filters.brands, brand) })}>
              {brand} <span className="ml-1 font-mono text-xs opacity-70 tnum">{count}</span>
            </Chip>
          ))}
        </div>
      </Group>

      <Group label={t('mount')}>
        <div className="flex flex-wrap gap-[var(--space-xs)]">
          {mountOptions.map(m => (
            <Chip key={m} active={filters.mounts.includes(m)} onClick={() => set({ mounts: toggle(filters.mounts, m) })}>
              {m}
            </Chip>
          ))}
        </div>
      </Group>

      <Group label={tc('sensorFormat')}>
        <div className="flex flex-wrap gap-[var(--space-xs)]">
          {FORMATS.map(f => (
            <Chip key={f} active={filters.sensorFormats.includes(f)} onClick={() => set({ sensorFormats: toggle(filters.sensorFormats, f) })}>
              {f}
            </Chip>
          ))}
        </div>
      </Group>

      <Group label={t('launchPrice')}>
        <p className="mb-[var(--space-xs)] font-mono text-xs text-ink-2 tnum">
          NT${filters.minPrice.toLocaleString()} – {filters.maxPrice >= PRICE_MAX ? 'MAX' : `NT$${filters.maxPrice.toLocaleString()}`}
        </p>
        <input
          type="range"
          min={0}
          max={PRICE_MAX}
          step={5000}
          value={filters.maxPrice}
          onChange={e => set({ maxPrice: parseInt(e.target.value) })}
          aria-label={t('launchPrice')}
          className="w-full accent-[var(--color-accent)]"
        />
      </Group>

      <Group label={t('releaseYear')}>
        <div className="flex items-center gap-[var(--space-xs)]">
          {(['minYear', 'maxYear'] as const).map((key, i) => (
            <select
              key={key}
              value={filters[key]}
              onChange={e => set({ [key]: parseInt(e.target.value) })}
              aria-label={`${t('releaseYear')} ${i === 0 ? 'from' : 'to'}`}
              className="h-11 min-w-0 flex-1 border border-rule-2 bg-paper px-[var(--space-xs)] font-mono text-sm text-ink tnum"
            >
              {YEARS.map(y => <option key={y} value={y}>{y}</option>)}
            </select>
          ))}
        </div>
      </Group>

      <div className="border-t border-rule pt-[var(--space-md)]">
        <button type="button" onClick={() => setFilters(EMPTY_FILTERS)} className="link-type min-h-11 text-sm text-ink-2">
          {tc('resetFilters')}
        </button>
      </div>
    </div>
  );
}
