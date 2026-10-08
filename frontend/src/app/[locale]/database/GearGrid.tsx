'use client';

import { useState, useEffect } from 'react';
import { ArrowRightLeft, Filter, X } from 'lucide-react';
import CameraCard from './CameraCard';
import { useRouter, useSearchParams, usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { weightValue, type Gear } from '@/lib/gear';
import { useCompareIds } from '@/lib/compare';

import FilterPanel, { FilterState } from './FilterPanel';

function filtersFromParams(p: Pick<URLSearchParams, 'get'>): FilterState {
  const list = (k: string) => p.get(k)?.split(',') ?? [];
  const int = (k: string, fallback: number) => (p.get(k) ? parseInt(p.get(k)!) : fallback);
  return {
    q: p.get('q') ?? '',
    sortBy: p.get('sortBy') ?? 'newest',
    minPrice: int('minP', 0),
    maxPrice: int('maxP', 200000),
    minYear: int('minY', 2010),
    maxYear: int('maxY', 2026),
    sensorFormats: list('formats'),
    gearTypes: list('gearTypes'),
    brands: list('brands'),
    mounts: list('mounts')
  };
}

export default function GearGrid({ gears, locale }: { gears: Gear[], locale: string }) {
  const searchParams = useSearchParams();
  const [filters, setFilters] = useState<FilterState>(() => filtersFromParams(searchParams));
  const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false);
  const [storedIds, setSelectedIds] = useCompareIds();
  // Drop ids that no longer exist (e.g. merged duplicates) so they can't lock the type filter
  const selectedIds = storedIds.filter(id => gears.some(g => g.id === id));
  const selectedType = gears.find(g => g.id === selectedIds[0])?.gearType ?? null;

  const router = useRouter();
  const pathname = usePathname();
  const t = useTranslations('GearSpecs');
  const tc = useTranslations('Common');

  // Calculate counts for each brand from all available gears
  const brandCounts = gears.reduce((acc: Record<string, number>, g) => {
    acc[g.brand] = (acc[g.brand] || 0) + 1;
    return acc;
  }, {});

  // Filtering and Sorting logic
  const filteredGears = gears
    .filter(g => {
      // Search (Model, Brand, and Aliases)
      if (filters.q) {
        const query = filters.q.toLowerCase();
        const matchesName = g.modelName.toLowerCase().includes(query);
        const matchesBrand = g.brand.toLowerCase().includes(query);
        const matchesAlias = (g.aliases || []).some(a => a.toLowerCase().includes(query));

        if (!matchesName && !matchesBrand && !matchesAlias) return false;
      }
      // Gear Type
      if (filters.gearTypes.length > 0 && !filters.gearTypes.includes(g.gearType)) return false;
      // Brands
      if (filters.brands.length > 0 && !filters.brands.includes(g.brand)) return false;
      // Price
      // The slider's top position means "MAX", i.e. no upper limit
      const price = g.launchPrice;
      if (price && (price < filters.minPrice || (filters.maxPrice < 200000 && price > filters.maxPrice))) return false;
      // Year
      const year = Number(g.releaseYear);
      if (year && (year < filters.minYear || year > filters.maxYear)) return false;
      // Format
      if (filters.sensorFormats.length > 0 && !filters.sensorFormats.includes(g.sensorFormat ?? '')) return false;
      // Mounts
      if (filters.mounts.length > 0) {
        const gearMountNames = g.mounts?.map(gm => gm.mount.name) || [];
        if (!filters.mounts.some(m => gearMountNames.includes(m))) return false;
      }
      
      return true;
    })
    .sort((a, b) => {
      switch (filters.sortBy) {
        case 'newest': return (Number(b.releaseYear) || 0) - (Number(a.releaseYear) || 0);
        case 'oldest': return (Number(a.releaseYear) || 0) - (Number(b.releaseYear) || 0);
        case 'priceDesc': return (Number(b.launchPrice) || 0) - (Number(a.launchPrice) || 0);
        case 'priceAsc': return (Number(a.launchPrice) || 1000000) - (Number(b.launchPrice) || 1000000);
        case 'weightAsc': return (weightValue(a) || 10000) - (weightValue(b) || 10000);
        case 'mpDesc': return (Number(b.megapixels) || 0) - (Number(a.megapixels) || 0);
        default: return 0;
      }
    });

  // Restore scroll position when coming back from a detail page
  useEffect(() => {
    window.history.scrollRestoration = 'manual';
    const savedScroll = sessionStorage.getItem('database_scroll');

    if (savedScroll) {
      let attempts = 0;
      const targetScroll = parseInt(savedScroll);

      const performScroll = () => {
        window.scrollTo({ top: targetScroll, behavior: 'instant' });
        attempts++;
        // Try multiple times over ~500ms to handle layout shifts
        if (attempts < 10) {
          requestAnimationFrame(performScroll);
        }
      };
      requestAnimationFrame(performScroll);
    }

    let saveTimeout: ReturnType<typeof setTimeout> | undefined;
    const handleScroll = () => {
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => {
        sessionStorage.setItem('database_scroll', window.scrollY.toString());
      }, 100);
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      clearTimeout(saveTimeout);
    };
  }, []);

  // Sync filters to URL
  useEffect(() => {
    const params = new URLSearchParams();
    if (filters.q) params.set('q', filters.q);
    if (filters.brands.length > 0) params.set('brands', filters.brands.join(','));
    if (filters.gearTypes.length > 0) params.set('gearTypes', filters.gearTypes.join(','));
    if (filters.sensorFormats.length > 0) params.set('formats', filters.sensorFormats.join(','));
    if (filters.mounts.length > 0) params.set('mounts', filters.mounts.join(','));
    if (filters.sortBy !== 'newest') params.set('sortBy', filters.sortBy);
    
    // Sync Numerical Filters to URL
    if (filters.minPrice > 0) params.set('minP', filters.minPrice.toString());
    if (filters.maxPrice < 200000) params.set('maxP', filters.maxPrice.toString());
    if (filters.minYear > 2010) params.set('minY', filters.minYear.toString());
    if (filters.maxYear < 2026) params.set('maxY', filters.maxYear.toString());

    const query = params.toString();
    const url = query ? `${pathname}?${query}` : pathname;
    
    window.history.replaceState(null, '', url);
  }, [filters, pathname]);

  const toggleSelect = (e: React.MouseEvent, gear: Gear) => {
    e.preventDefault();
    e.stopPropagation();

    const isSelected = selectedIds.includes(gear.id);

    if (!isSelected && selectedIds.length > 0 && selectedType !== gear.gearType) {
      alert(tc('cannotMixComparison'));
      return;
    }

    setSelectedIds(isSelected
      ? selectedIds.filter(i => i !== gear.id)
      : [...selectedIds, gear.id]);
  };

  const handleCompare = () => {
    if (selectedIds.length > 0) {
      router.push(`/${locale}/compare?ids=${selectedIds.join(',')}`);
    }
  };

  return (
    <div className="flex flex-col md:flex-row gap-8 items-start">
      {/* Mobile Filter Toggle Button */}
      <div className="md:hidden w-full sticky top-20 z-20 bg-black/80 backdrop-blur-md py-4">
        <button 
          onClick={() => setIsMobileFilterOpen(true)}
          className="w-full flex items-center justify-center gap-2 bg-[#1A1A1A] hover:bg-[#222] border border-white/10 text-white py-3 rounded-none uppercase tracking-widest text-sm font-semibold transition-colors"
        >
          <Filter className="w-4 h-4" />
          {tc('filters')}
        </button>
      </div>

      {/* Sidebar Filters (Desktop & Mobile Modal) */}
      <aside className={`
        fixed inset-0 z-50 bg-black/95 p-6 overflow-y-auto transition-transform duration-300
        ${isMobileFilterOpen ? 'translate-x-0' : '-translate-x-full'}
        md:static md:translate-x-0 md:w-64 md:shrink-0 md:bg-transparent md:p-0 md:block md:sticky md:top-24 md:z-10 md:overflow-visible
      `}>
        <div className="flex md:hidden justify-between items-center mb-8 border-b border-white/10 pb-4">
          <h2 className="text-xl font-bold uppercase tracking-widest">{tc('filters')}</h2>
          <button onClick={() => setIsMobileFilterOpen(false)} className="p-2 border border-white/10 hover:bg-white/5 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <FilterPanel filters={filters} setFilters={setFilters} brandCounts={brandCounts} />
        
        {/* Mobile Apply Button */}
        <div className="mt-8 md:hidden pb-12">
          <button 
            onClick={() => setIsMobileFilterOpen(false)}
            className="w-full bg-red-600 hover:bg-red-700 transition-colors text-white py-4 font-bold uppercase tracking-widest text-sm"
          >
            Apply & Close
          </button>
        </div>
      </aside>

      <div className="flex-1 relative w-full">
        {filteredGears.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredGears.map(gear => (
              <CameraCard
                key={gear.id}
                gear={gear}
                isSelected={selectedIds.includes(gear.id)}
                isDisabled={selectedIds.length > 0 && selectedType !== gear.gearType}
                onToggle={toggleSelect}
                t={t}
                tc={tc}
              />
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-48 border border-dashed border-white/5 bg-white/5 w-full">
             <div className="text-gray-600 uppercase tracking-[0.5em] text-sm mb-2 font-bold">NO RESULTS FOUND</div>
             <div className="text-[10px] text-gray-700 uppercase tracking-widest">TRY ADJUSTING YOUR FILTERS</div>
          </div>
        )}
      </div>

      {/* Floating Compare Button */}
      {selectedIds.length > 0 && (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 bg-[#111] border border-red-600/50 p-4 shadow-2xl flex items-center gap-3 md:gap-6 z-50 whitespace-nowrap animate-in fade-in slide-in-from-bottom-4">
          <div className="text-white text-xs md:text-sm font-medium tracking-wide">
            {selectedIds.length} {tc('itemsSelected')} ({selectedType === 'LENS' ? t('lens') : t('body')})
          </div>
          <div className="flex gap-2">
            <button 
              onClick={() => setSelectedIds([])}
              className="text-gray-400 hover:text-white text-xs uppercase tracking-widest px-3 md:px-4 py-2 border border-white/10 hover:border-white transition-colors"
            >
              {tc('clear')}
            </button>
            <button 
              onClick={handleCompare}
              className="bg-red-600 hover:bg-red-700 text-white px-4 md:px-6 py-2 text-sm font-semibold uppercase tracking-widest transition-colors flex items-center gap-2"
            >
              <ArrowRightLeft className="w-4 h-4" />
              {tc('compare')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}


