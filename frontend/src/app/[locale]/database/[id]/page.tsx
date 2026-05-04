'use client';

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/navigation';
import { notFound } from 'next/navigation';
import { Link } from '@/i18n/routing';
import React from 'react';
import { Camera, ChevronLeft, Calendar, Tag, Shield, Zap, Maximize, Cpu, Video, Layers } from 'lucide-react';
import CompareButton from '../CompareButton';
import products from '@/data/products.json';

async function getGear(id: string) {
  const item = products.find((p: any) => String(p.id) === id || p.slug === id);
  
  if (!item) return null;

  return {
    ...item,
    id: item.id,
    brand: typeof item.brand === 'string' ? { 
      slug: item.brand.toLowerCase(), 
      nameI18n: { enUs: item.brand, zhTw: item.brand } 
    } : item.brand,
    modelNameI18n: typeof item.modelName === 'string' ? {
      enUs: item.modelName,
      zhTw: item.modelName
    } : item.modelNameI18n
  };
}

function SpecRow({ label, value, unit }: { label: string; value: any; unit?: string }) {
  if (value === null || value === undefined || value === "") return null;
  
  const displayValue = (typeof value === 'number' && value === 0) ? "0" : String(value);
  
  if (displayValue === "0" && !unit) return null;

  const unitStr = unit || '';
  const finalUnit = (unitStr && !displayValue.toLowerCase().includes(unitStr.toLowerCase())) ? unitStr : '';
  
  return (
    <div className="flex justify-between items-center border-b border-white/5 py-3 px-4 hover:bg-white/[0.02] transition-colors">
      <span className="text-gray-500 text-xs uppercase tracking-widest font-bold">{label}</span>
      <span className="text-white text-sm font-light">{displayValue}{finalUnit}</span>
    </div>
  );
}

function FeatureBadge({ label, value, t }: { label: string; value: boolean | null | undefined; t: any }) {
  if (value === null || value === undefined) return null;
  return (
    <div className={`px-3 py-1.5 text-xs font-semibold uppercase tracking-wider border ${
      value 
        ? 'bg-green-600/10 border-green-600/30 text-green-400' 
        : 'bg-white/5 border-white/10 text-gray-600'
    }`}>
      {value ? '✓' : '✗'} {label}
    </div>
  );
}

export default function GearDetailPage({ params }: { params: Promise<{ id: string, locale: string }> }) {
  const { id, locale } = React.use(params);
  const router = useRouter();
  const t = useTranslations('GearSpecs');
  const tc = useTranslations('Common');
  
  // Note: Since this is now a Client Component, getGear needs to be handled via API or data fetching hook
  // Keeping original async implementation for now as requested
  const gear = products.find((p: any) => String(p.id) === id || p.slug === id);
  
  if (!gear) notFound();

  // Robustly handle both old nested structure and new flat structure
  const name = gear.modelNameI18n?.enUs || gear.modelName || 'Unknown Model';
  const brandName = typeof gear.brand === 'string' 
    ? gear.brand 
    : (gear.brand.nameI18n?.enUs || gear.brand.name || 'Unknown Brand');
  
  const isLens = gear.gearType === 'LENS';
  const isPrime = isLens && gear.focalLengthMinMm === gear.focalLengthMaxMm;

  return (
    <div className="flex flex-col min-h-screen bg-black text-white">
      <header className="border-b border-white/10 p-4 flex justify-between items-center bg-black/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <Camera className="w-6 h-6 text-red-600" />
          <h1 className="text-xl font-bold tracking-widest uppercase">LensHistory</h1>
        </div>
        <nav className="flex gap-6 text-sm font-medium text-gray-400">
          <Link href="/" className="hover:text-red-500 transition-colors">Home</Link>
          <Link href="/database" className="text-white hover:text-red-500 transition-colors">Database</Link>
        </nav>
      </header>

      <main className="flex-1 max-w-6xl mx-auto w-full p-8">
        <div className="mb-8">
          <button 
            onClick={() => router.back()}
            className="group flex items-center gap-2 text-gray-400 hover:text-white transition-colors mb-8"
          >
            <ChevronLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            <span className="text-xs uppercase tracking-[0.2em] font-medium">{tc('backToDatabase')}</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-12">
          <div className="bg-[#111] border border-white/5 p-8 flex items-center justify-center min-h-[400px] relative group">
            <div className="absolute top-4 left-4 bg-red-600 text-white text-xs font-bold px-3 py-1 uppercase tracking-wider">
              {brandName}
            </div>
            {gear.series && (
              <div className="absolute top-4 right-4 border border-amber-500/50 text-amber-400 text-[10px] font-bold px-2 py-0.5 uppercase tracking-wider">
                {gear.series}
              </div>
            )}
            {gear.imageUrl ? (
              <img src={gear.imageUrl} alt={name} className="w-full max-w-md object-contain hover:scale-105 transition-transform duration-500" />
            ) : (
              <div className="flex flex-col items-center gap-4">
                <Camera className="w-32 h-32 text-gray-800" />
                <span className="text-gray-600 font-bold tracking-widest uppercase">{gear.gearType}</span>
              </div>
            )}
          </div>

          {/* Title & Summary */}
          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-light tracking-wide text-white mb-2">{name}</h1>
              <div className="flex items-center gap-3 flex-wrap">
                <span className="text-red-500 uppercase tracking-widest text-sm font-semibold">
                  {isLens ? (isPrime ? t('prime') : t('zoom')) : t('body')}
                </span>
                {gear.lensType && <span className="text-gray-600 text-sm">· {gear.lensType}</span>}
                {gear.sensorFormat && <span className="text-gray-600 text-sm">· {gear.sensorFormat}</span>}
              </div>
            </div>

            {/* Quick specs */}
            <div className="grid grid-cols-2 gap-3">
              {isLens ? (
                <>
                  {gear.focalLengthMinMm && (
                    <div className="bg-[#111] border border-white/5 p-4">
                      <div className="text-gray-500 text-[10px] uppercase tracking-widest mb-1">{t('focalLength')}</div>
                      <div className="text-white text-xl font-light">
                        {isPrime ? `${gear.focalLengthMinMm}mm` : `${gear.focalLengthMinMm}-${gear.focalLengthMaxMm}mm`}
                      </div>
                    </div>
                  )}
                  {gear.apertureMax && (
                    <div className="bg-[#111] border border-white/5 p-4">
                      <div className="text-gray-500 text-[10px] uppercase tracking-widest mb-1">{t('maxAperture')}</div>
                      <div className="text-white text-xl font-light">f/{gear.apertureMax}</div>
                    </div>
                  )}
                </>
              ) : (
                <>
                  {gear.megapixels && (
                    <div className="bg-[#111] border border-white/5 p-4">
                      <div className="text-gray-500 text-[10px] uppercase tracking-widest mb-1">{t('megapixels')}</div>
                      <div className="text-white text-xl font-light">{gear.megapixels}MP</div>
                    </div>
                  )}
                  {gear.sensorType && (
                    <div className="bg-[#111] border border-white/5 p-4">
                      <div className="text-gray-500 text-[10px] uppercase tracking-widest mb-1">{t('sensorType')}</div>
                      <div className="text-white text-lg font-light truncate" title={gear.sensorType}>{gear.sensorType}</div>
                    </div>
                  )}
                </>
              )}
              {gear.weightGrams && (
                <div className="bg-[#111] border border-white/5 p-4">
                  <div className="text-gray-500 text-[10px] uppercase tracking-widest mb-1">{t('weight')}</div>
                  <div className="text-white text-xl font-light">{gear.weightGrams}g</div>
                </div>
              )}
              {gear.launchPrice && (
                <div className="bg-[#111] border border-white/5 p-4">
                  <div className="text-gray-500 text-[10px] uppercase tracking-widest mb-1">{t('launchPrice')}</div>
                  <div className="text-white text-xl font-light">NT${Number(gear.launchPrice).toLocaleString()}</div>
                </div>
              )}
            </div>

            {/* Feature badges */}
            <div className="flex flex-wrap gap-2">
              {isLens ? (
                <>
                  <FeatureBadge label={t('ois')} value={gear.hasOIS} t={t} />
                  <FeatureBadge label={t('weatherSeal')} value={gear.hasWeatherSeal} t={t} />
                  <FeatureBadge label={t('apertureRing')} value={gear.hasApertureRing} t={t} />
                  <FeatureBadge label={t('customButton')} value={gear.hasCustomButton} t={t} />
                </>
              ) : (
                <>
                  <FeatureBadge label={t('ibis')} value={gear.hasIBIS} t={t} />
                  <FeatureBadge label={t('weatherSeal')} value={gear.hasWeatherSeal} t={t} />
                  <div className="bg-white/5 border border-white/10 px-3 py-1.5 text-[10px] text-gray-400 uppercase tracking-widest">
                    {gear.sensorType || '--'}
                  </div>
                </>
              )}
            </div>

            <div className="pt-4">
              <CompareButton gearId={gear.id} locale={locale} />
            </div>
          </div>
        </div>

        {/* Full Specs Table */}
        <div className="bg-[#111] border border-white/5">
          <div className="p-6 border-b border-white/10">
            <h3 className="text-xl font-light uppercase tracking-wider text-gray-300">{t('fullSpecs')}</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2">
            {isLens ? (
              <>
                {/* 1. Imaging Core */}
                <div className="border-r border-b border-white/5">
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('imaging')}</span>
                  </div>
                  <SpecRow label={t('focalLength')} value={isPrime ? `${gear.focalLengthMinMm}mm` : `${gear.focalLengthMinMm}-${gear.focalLengthMaxMm}mm`} />
                  <SpecRow label={t('maxAperture')} value={gear.apertureMax ? `f/${gear.apertureMax}` : null} />
                  <SpecRow label={t('minAperture')} value={gear.minAperture ? `f/${gear.minAperture}` : '--'} />
                  <SpecRow label={t('motorType')} value={gear.motorType || '--'} />
                  <SpecRow label={t('maxMagnification')} value={(gear.maxMagnification && !isNaN(Number(gear.maxMagnification))) ? `${Number(gear.maxMagnification).toFixed(2)}x` : '--'} />
                  <SpecRow label={t('closeFocus')} value={gear.closeFocus || '--'} unit={gear.closeFocus && gear.closeFocus !== '--' ? "m" : ""} />
                </div>

                {/* 2. Optical Performance */}
                <div className="border-b border-white/5">
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('optical')}</span>
                  </div>
                  <SpecRow label={t('opticalDesign')} value={gear.opticalDesign || '--'} />
                  <SpecRow label={t('specialElements')} value={gear.specialElements || '--'} />
                  <SpecRow label={t('coatings')} value={gear.coatings || '--'} />
                  <SpecRow label={t('filterSize')} value={gear.filterSizeMm === 0 ? "後置濾鏡 (Rear) / 前組不可裝" : (gear.filterSizeMm || '--')} unit={gear.filterSizeMm > 0 ? "mm" : ""} />
                </div>

                {/* 3. Key Features */}
                <div className="border-r border-white/5">
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('features')}</span>
                  </div>
                  <SpecRow label={t('ois')} value={gear.hasOIS === true ? tc('yes') : tc('no')} />
                  <SpecRow label={t('apertureRing')} value={gear.hasApertureRing === true ? tc('yes') : tc('no')} />
                  <SpecRow label={t('customButton')} value={gear.hasCustomButton === true ? tc('yes') : tc('no')} />
                  <SpecRow label={t('weatherSeal')} value={gear.hasWeatherSeal === true ? tc('yes') : tc('no')} />
                </div>

                {/* 4. Physical & Market */}
                <div>
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('physical')}</span>
                  </div>
                  <SpecRow label={t('series')} value={gear.series || '--'} />
                  <SpecRow label={t('weight')} value={gear.weightGrams || '--'} unit={gear.weightGrams ? "g" : ""} />
                  <SpecRow label={t('dimensions')} value={(gear.widthMm || gear.diameter) && gear.lengthMm ? `${gear.widthMm || gear.diameter} x ${gear.lengthMm}` : '--'} unit={gear.lengthMm ? "mm" : ""} />
                  <SpecRow label={t('releaseYear')} value={gear.releaseYear || '--'} />
                  <SpecRow label={t('launchPrice')} value={gear.launchPrice ? `NT$${Number(gear.launchPrice).toLocaleString()}` : '--'} />
                </div>
              </>
            ) : (
              <>
                {/* Body Specs (Existing Layout) */}
                <div className="border-r border-b border-white/5">
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('imaging')}</span>
                  </div>
                  <SpecRow label={t('megapixels')} value={gear.megapixels} unit="MP" />
                  <SpecRow label={t('sensorType')} value={gear.sensorType} />
                  <SpecRow label={t('sensorFormat')} value={gear.sensorFormat} />
                  <SpecRow label={t('video')} value={gear.videoResolution} />
                </div>
                <div className="border-b border-white/5">
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('performance')}</span>
                  </div>
                  <SpecRow label={t('afPoints')} value={gear.afPoints} />
                  <SpecRow label={t('burstSpeed')} value={gear.burstSpeed} />
                  <SpecRow label={t('evfResolution')} value={gear.evfResolution} />
                  <SpecRow label={t('weight')} value={gear.weightGrams} unit="g" />
                </div>
                {/* Add more body rows if needed */}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

