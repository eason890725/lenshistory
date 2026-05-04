'use client';

import { useTranslations } from 'next-intl';
import { Search, SortDesc, SlidersHorizontal } from 'lucide-react';

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

export default function FilterPanel({ 
  filters, 
  setFilters,
  maxPriceData = 200000,
  minYearData = 2010,
  maxYearData = 2026
}: { 
  filters: FilterState; 
  setFilters: (f: FilterState) => void;
  maxPriceData?: number;
  minYearData?: number;
  maxYearData?: number;
}) {
  const t = useTranslations('GearSpecs');
  const tc = useTranslations('Common');

  const formats = ["Full Frame", "APS-C"];

  const handleFormatToggle = (fmt: string) => {
    if (filters.sensorFormats.includes(fmt)) {
      setFilters({ ...filters, sensorFormats: filters.sensorFormats.filter(f => f !== fmt) });
    } else {
      setFilters({ ...filters, sensorFormats: [...filters.sensorFormats, fmt] });
    }
  };

  return (
    <div className="bg-[#111] border border-white/10 p-6 space-y-8 max-h-[calc(100vh-120px)] overflow-y-auto custom-scrollbar">
      {/* Search */}
      <div className="space-y-3">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500 flex items-center gap-2">
          <Search className="w-3 h-3" /> {tc('search')}
        </label>
        <input 
          type="text" 
          value={filters.q}
          onChange={(e) => setFilters({ ...filters, q: e.target.value })}
          placeholder="MODEL NAME..."
          className="w-full bg-black border border-white/10 px-4 py-2 text-sm text-white focus:outline-none focus:border-red-600 transition-colors"
        />
      </div>

      {/* Sort */}
      <div className="space-y-3">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500 flex items-center gap-2">
          <SortDesc className="w-3 h-3" /> {tc('sortBy')}
        </label>
        <select 
          value={filters.sortBy}
          onChange={(e) => setFilters({ ...filters, sortBy: e.target.value })}
          className="w-full bg-black border border-white/10 px-4 py-2 text-sm text-white focus:outline-none focus:border-red-600 appearance-none"
        >
          <option value="newest">{tc('newest')}</option>
          <option value="oldest">{tc('oldest')}</option>
          <option value="priceDesc">{tc('priceHighToLow')}</option>
          <option value="priceAsc">{tc('priceLowToHigh')}</option>
          <option value="weightAsc">{tc('weightLightest')}</option>
          <option value="mpDesc">{tc('megapixelsHighest')}</option>
        </select>
      </div>

      {/* Price Range */}
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500">{t('launchPrice')}</label>
          <span className="text-[10px] text-red-500 font-mono">NT${filters.minPrice.toLocaleString()} - {filters.maxPrice >= maxPriceData ? 'MAX' : 'NT$' + filters.maxPrice.toLocaleString()}</span>
        </div>
        <input 
          type="range" 
          min={0} 
          max={maxPriceData} 
          step={5000}
          value={filters.maxPrice}
          onChange={(e) => setFilters({ ...filters, maxPrice: parseInt(e.target.value) })}
          className="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-red-600"
        />
      </div>

      {/* Year Range */}
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500">{t('releaseYear')}</label>
          <span className="text-[10px] text-red-500 font-mono">{filters.minYear} - {filters.maxYear}</span>
        </div>
        <div className="flex gap-2">
           <select 
            value={filters.minYear}
            onChange={(e) => setFilters({ ...filters, minYear: parseInt(e.target.value) })}
            className="flex-1 bg-black border border-white/10 px-2 py-1 text-xs text-white"
           >
             {[2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026].map(y => <option key={y} value={y}>{y}</option>)}
           </select>
           <select 
            value={filters.maxYear}
            onChange={(e) => setFilters({ ...filters, maxYear: parseInt(e.target.value) })}
            className="flex-1 bg-black border border-white/10 px-2 py-1 text-xs text-white"
           >
             {[2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026].map(y => <option key={y} value={y}>{y}</option>)}
           </select>
        </div>
      </div>

      {/* Brands */}
      <div className="space-y-3">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500">{tc('brands')}</label>
        <div className="flex flex-wrap gap-2">
          {["Sony", "Canon", "Nikon", "Fujifilm", "Sigma", "Tamron", "Samyang", "Viltrox"].map(brand => (
            <button
              key={brand}
              onClick={() => {
                const next = filters.brands.includes(brand) 
                  ? filters.brands.filter(b => b !== brand)
                  : [...filters.brands, brand];
                setFilters({ ...filters, brands: next });
              }}
              className={`px-3 py-1.5 text-[10px] font-bold border transition-colors ${filters.brands.includes(brand) ? 'bg-red-600/20 border-red-600 text-white' : 'bg-black border-white/10 text-gray-500 hover:border-white/30'}`}
            >
              {brand}
            </button>
          ))}
        </div>
      </div>

      {/* Mounts */}
      <div className="space-y-3">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500">{t('mount')}</label>
        <div className="flex flex-wrap gap-2">
          {["Sony E", "Canon RF", "Nikon Z", "Fujifilm X", "Fujifilm G"].map(m => (
            <button
              key={m}
              onClick={() => {
                const next = filters.mounts.includes(m) 
                  ? filters.mounts.filter(x => x !== m)
                  : [...filters.mounts, m];
                setFilters({ ...filters, mounts: next });
              }}
              className={`px-2 py-1 text-[9px] font-bold border transition-colors ${filters.mounts.includes(m) ? 'bg-red-600/20 border-red-600 text-white' : 'bg-black border-white/10 text-gray-500 hover:border-white/30'}`}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      {/* Gear Type */}
      <div className="space-y-3">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500">{t('gearType')}</label>
        <div className="flex gap-2">
          {["LENS", "CAMERA_BODY"].map(type => (
            <button
              key={type}
              onClick={() => {
                const next = filters.gearTypes.includes(type) 
                  ? filters.gearTypes.filter(t => t !== type)
                  : [...filters.gearTypes, type];
                setFilters({ ...filters, gearTypes: next });
              }}
              className={`flex-1 py-2 text-[10px] font-bold border transition-colors ${filters.gearTypes.includes(type) ? 'bg-red-600 border-red-600 text-white' : 'bg-black border-white/10 text-gray-500 hover:border-white/30'}`}
            >
              {type === 'LENS' ? t('lens') : t('body')}
            </button>
          ))}
        </div>
      </div>

      {/* Sensor Format */}
      <div className="space-y-3">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-500">{tc('sensorFormat')}</label>
        <div className="flex flex-wrap gap-2">
          {formats.map(fmt => (
            <button
              key={fmt}
              onClick={() => handleFormatToggle(fmt)}
              className={`px-3 py-1.5 text-[10px] font-bold border transition-colors ${filters.sensorFormats.includes(fmt) ? 'bg-red-600/20 border-red-600 text-white' : 'bg-black border-white/10 text-gray-500 hover:border-white/30'}`}
            >
              {fmt}
            </button>
          ))}
        </div>
      </div>

      {/* Reset */}
      <button 
        onClick={() => setFilters({
          q: '',
          sortBy: 'newest',
          minPrice: 0,
          maxPrice: maxPriceData,
          minYear: minYearData,
          maxYear: maxYearData,
          sensorFormats: [],
          gearTypes: [],
          brands: [],
          mounts: []
        })}
        className="w-full py-2 text-[10px] font-bold uppercase tracking-[0.2em] text-gray-500 hover:text-white border border-dashed border-white/10 hover:border-white/30 transition-colors"
      >
        {tc('resetFilters')}
      </button>
    </div>
  );
}
