'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Camera, Check, ArrowRightLeft } from 'lucide-react';
import { Link } from '@/i18n/routing';
import CameraCard from './CameraCard';
import { useRouter, useSearchParams, usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';

import FilterPanel, { FilterState } from './FilterPanel';

export default function GearGrid({ gears, locale }: { gears: any[], locale: string }) {
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterState>({
    q: '',
    sortBy: 'newest',
    minPrice: 0,
    maxPrice: 200000,
    minYear: 2010,
    maxYear: 2026,
    sensorFormats: [],
    gearTypes: [],
    brands: [],
    mounts: []
  });
  const [mounted, setMounted] = useState(false);

  const router = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const t = useTranslations('GearSpecs');
  const tc = useTranslations('Common');

  // Calculate counts for each brand from all available gears
  const brandCounts = gears.reduce((acc: Record<string, number>, g) => {
    const brandName = g.brand?.nameI18n?.enUs || g.brand;
    acc[brandName] = (acc[brandName] || 0) + 1;
    return acc;
  }, {});

  // Filtering and Sorting logic
  const filteredGears = gears
    .filter(g => {
      // Search
      if (filters.q) {
        const query = filters.q.toLowerCase();
        const nameEn = (g.modelNameI18n?.enUs || g.modelName || '').toLowerCase();
        const brandEn = (typeof g.brand === 'string' ? g.brand : (g.brand?.nameI18n?.enUs || g.brand?.name || '')).toLowerCase();
        if (!nameEn.includes(query) && !brandEn.includes(query)) return false;
      }
      // Gear Type
      if (filters.gearTypes.length > 0 && !filters.gearTypes.includes(g.gearType)) return false;
      // Brands
      if (filters.brands.length > 0) {
        const itemBrandName = typeof g.brand === 'string' ? g.brand : (g.brand?.nameI18n?.enUs || g.brand?.name);
        if (!filters.brands.includes(itemBrandName)) return false;
      }
      // Price
      if (g.launchPrice && (g.launchPrice < filters.minPrice || g.launchPrice > filters.maxPrice)) return false;
      // Year
      if (g.releaseYear && (g.releaseYear < filters.minYear || g.releaseYear > filters.maxYear)) return false;
      // Format
      if (filters.sensorFormats.length > 0 && !filters.sensorFormats.includes(g.sensorFormat)) return false;
      // Mounts
      if (filters.mounts.length > 0) {
        const gearMountNames = g.mounts?.map((gm: any) => gm.mount?.name) || [];
        if (!filters.mounts.some(m => gearMountNames.includes(m))) return false;
      }
      
      return true;
    })
    .sort((a, b) => {
      switch (filters.sortBy) {
        case 'newest': return b.releaseYear - a.releaseYear;
        case 'oldest': return a.releaseYear - b.releaseYear;
        case 'priceDesc': return (b.launchPrice || 0) - (a.launchPrice || 0);
        case 'priceAsc': return (a.launchPrice || 1000000) - (b.launchPrice || 1000000);
        case 'weightAsc': return (a.weightGrams || 10000) - (b.weightGrams || 10000);
        case 'mpDesc': return (b.megapixels || 0) - (a.megapixels || 0);
        default: return 0;
      }
    });

  // Initialize filters from URL on mount
  useEffect(() => {
    setMounted(true);
    
    const urlFilters: Partial<FilterState> = {};
    const q = searchParams.get('q');
    if (q) urlFilters.q = q;
    
    const brands = searchParams.get('brands');
    if (brands) urlFilters.brands = brands.split(',');
    
    const gearTypes = searchParams.get('gearTypes');
    if (gearTypes) urlFilters.gearTypes = gearTypes.split(',');
    
    const formats = searchParams.get('formats');
    if (formats) urlFilters.sensorFormats = formats.split(',');
    
    const mounts = searchParams.get('mounts');
    if (mounts) urlFilters.mounts = mounts.split(',');
    
    const sortBy = searchParams.get('sortBy');
    if (sortBy) urlFilters.sortBy = sortBy;

    if (Object.keys(urlFilters).length > 0) {
      setFilters(prev => ({ ...prev, ...urlFilters }));
    }

    const stored = localStorage.getItem('compare_ids');
    if (stored) {
      try {
        const ids = JSON.parse(stored);
        setSelectedIds(ids);
        if (ids.length > 0) {
          const firstItem = gears.find(g => g.id === ids[0]);
          if (firstItem) setSelectedType(firstItem.gearType);
        }
      } catch (e) {
        setSelectedIds([]);
      }
    }
  }, [gears]);

  // Sync filters to URL
  useEffect(() => {
    if (!mounted) return;

    const params = new URLSearchParams();
    if (filters.q) params.set('q', filters.q);
    if (filters.brands.length > 0) params.set('brands', filters.brands.join(','));
    if (filters.gearTypes.length > 0) params.set('gearTypes', filters.gearTypes.join(','));
    if (filters.sensorFormats.length > 0) params.set('formats', filters.sensorFormats.join(','));
    if (filters.mounts.length > 0) params.set('mounts', filters.mounts.join(','));
    if (filters.sortBy !== 'newest') params.set('sortBy', filters.sortBy);

    const query = params.toString();
    const url = query ? `${pathname}?${query}` : pathname;
    
    // Use replace to avoid polluting history with every filter click, 
    // but the state is now in the URL for navigation.
    window.history.replaceState(null, '', url);
  }, [filters, pathname, mounted]);

  const toggleSelect = (e: React.MouseEvent, gear: any) => {
    e.preventDefault();
    e.stopPropagation();
    
    const isSelected = selectedIds.includes(gear.id);
    
    if (!isSelected && selectedIds.length > 0 && selectedType !== gear.gearType) {
      alert(tc('cannotMixComparison'));
      return;
    }

    const newIds = isSelected 
      ? selectedIds.filter(i => i !== gear.id)
      : [...selectedIds, gear.id];
    
    setSelectedIds(newIds);
    setSelectedType(newIds.length > 0 ? gear.gearType : null);
    localStorage.setItem('compare_ids', JSON.stringify(newIds));
  };

  const handleCompare = () => {
    if (selectedIds.length > 0) {
      router.push(`/${locale}/compare?ids=${selectedIds.join(',')}`);
    }
  };

  if (!mounted) {
    return (
      <div className="flex flex-col md:flex-row gap-8 items-start opacity-0">
        <aside className="w-full md:w-64 shrink-0" />
        <div className="flex-1" />
      </div>
    );
  }

  return (
    <div className="flex flex-col md:flex-row gap-8 items-start">
      {/* Sidebar Filters */}
      <aside className="w-full md:w-64 shrink-0 sticky top-24">
        <FilterPanel filters={filters} setFilters={setFilters} brandCounts={brandCounts} />
      </aside>

      <div className="flex-1 relative w-full">
        {filteredGears.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredGears.map((gear: any) => (
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
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 bg-[#111] border border-red-600/50 p-4 shadow-2xl flex items-center gap-6 z-50 animate-in fade-in slide-in-from-bottom-4">
          <div className="text-white text-sm font-medium tracking-wide">
            {selectedIds.length} {tc('itemsSelected')} ({selectedType === 'LENS' ? t('lens') : t('body')})
          </div>
          <div className="flex gap-2">
            <button 
              onClick={() => {
                setSelectedIds([]);
                setSelectedType(null);
                localStorage.setItem('compare_ids', '[]');
              }}
              className="text-gray-400 hover:text-white text-xs uppercase tracking-widest px-4 py-2 border border-white/10 hover:border-white transition-colors"
            >
              {tc('clear')}
            </button>
            <button 
              onClick={handleCompare}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 text-sm font-semibold uppercase tracking-widest transition-colors flex items-center gap-2"
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


