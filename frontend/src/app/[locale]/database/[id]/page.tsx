import { getTranslations, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Link } from '@/i18n/routing';
import { Camera } from 'lucide-react';
import BackButton from '../BackButton';
import CompareButton from '../CompareButton';
import { focalLength, weightLabel } from '@/lib/gear';
import { findGear } from '@/lib/gear-data';

function SpecRow({ label, value, unit }: { label: string; value: string | number | null | undefined; unit?: string }) {
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

function FeatureBadge({ label, value }: { label: string; value: boolean | null | undefined }) {
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

export default async function GearDetailPage({ params }: { params: Promise<{ id: string, locale: string }> }) {
  const { id, locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('GearSpecs');
  const tc = await getTranslations('Common');

  const gear = findGear(decodeURIComponent(id));
  if (!gear) notFound();

  const name = gear.modelName;
  const brandName = gear.brand;
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
          <BackButton label={tc('backToDatabase')} />
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
            {gear.image_url ? (
              <img src={gear.image_url} alt={name} className="w-full max-w-md object-contain hover:scale-105 transition-transform duration-500" />
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
                        {focalLength(gear)}
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
                      <div className="text-white text-xl font-light">{gear.megapixels}</div>
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
                  <div className="text-white text-xl font-light">{weightLabel(gear)}</div>
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
                  <FeatureBadge label={t('ois')} value={gear.hasOIS} />
                  <FeatureBadge label={t('weatherSeal')} value={gear.hasWeatherSeal} />
                  <FeatureBadge label={t('apertureRing')} value={gear.hasApertureRing} />
                  <FeatureBadge label={t('customButton')} value={gear.hasCustomButton} />
                </>
              ) : (
                <>
                  <FeatureBadge label={t('ibis')} value={gear.hasIBIS} />
                  <FeatureBadge label={t('weatherSeal')} value={gear.hasWeatherSeal} />
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

          <div className="p-0">
            {isLens ? (
              <div className="grid grid-cols-1 md:grid-cols-2">
                {/* 1. Basic Specs (Lens) */}
                <div className="border-r border-b border-white/5">
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('basicSpecs')}</span>
                  </div>
                  <SpecRow label={t('focalLength')} value={focalLength(gear)} />
                  <SpecRow label={t('maxAperture')} value={gear.apertureMax ? `f/${gear.apertureMax}` : null} />
                  <SpecRow label={t('minAperture')} value={gear.minAperture ? `f/${gear.minAperture}` : '--'} />
                  <SpecRow label={t('motorType')} value={gear.motorType || '--'} />
                  <SpecRow label={t('maxMagnification')} value={gear.maxMagnification || '--'} />
                  <SpecRow label={t('closeFocus')} value={gear.closeFocus || '--'} unit={(gear.closeFocus && gear.closeFocus !== '--' && !String(gear.closeFocus).includes('m')) ? "m" : ""} />
                </div>

                {/* 2. Optical Performance */}
                <div className="border-b border-white/5">
                  <div className="bg-white/[0.02] px-4 py-2 border-b border-white/5">
                    <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{t('optical')}</span>
                  </div>
                  <SpecRow label={t('opticalDesign')} value={gear.opticalDesign || '--'} />
                  <SpecRow label={t('specialElements')} value={gear.specialElements || '--'} />
                  <SpecRow label={t('coatings')} value={gear.coatings || '--'} />
                  <SpecRow label={t('filterSize')} value={gear.filterSizeMm === 0 ? "後置濾鏡 (Rear) / 前組不可裝" : (gear.filterSizeMm || '--')} unit={Number(gear.filterSizeMm ?? 0) > 0 ? "mm" : ""} />
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
                  <SpecRow label={t('weight')} value={weightLabel(gear) || '--'} />
                  <SpecRow label={t('dimensions')} value={gear.dimensions || '--'} />
                  <SpecRow label={t('releaseYear')} value={gear.releaseYear || '--'} />
                  <SpecRow label={t('launchPrice')} value={gear.launchPrice ? `NT$${Number(gear.launchPrice).toLocaleString()}` : '--'} />
                </div>
              </div>
            ) : (
              <div className="p-6">
                {/* 1. Imaging Core (Body) */}
                <div className="mb-8">
                  <div className="text-red-500 text-[10px] uppercase tracking-widest font-bold mb-4">{t('imaging')}</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-1">
                    <SpecRow label={t('megapixels')} value={gear.megapixels || '--'} />
                    <SpecRow label={t('sensorType')} value={gear.sensorType || '--'} />
                    <SpecRow label={t('processor')} value={gear.processor || '--'} />
                    <SpecRow label={t('sensorFormat')} value={gear.sensorFormat} />
                    <SpecRow label={t('video')} value={gear.videoResolution || '--'} />
                    <SpecRow label={t('videoColorDepth')} value={gear.videoColorDepth || '--'} />
                    <SpecRow label={t('logSupport')} value={gear.logSupport || '--'} />
                    <SpecRow label={t('ibisRating')} value={gear.ibisRating || '--'} />
                  </div>
                </div>

                {/* 2. Performance Section */}
                <div className="mb-8 border-t border-white/5 pt-4">
                  <div className="text-red-500 text-[10px] uppercase tracking-widest font-bold mb-4">{t('performance')}</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-1">
                    <SpecRow label={t('afPoints')} value={gear.afPoints || '--'} />
                    <SpecRow label={t('afTargets')} value={gear.afTargets || '--'} />
                    <SpecRow label={t('afRange')} value={gear.afRange || '--'} />
                    <SpecRow label={t('continuousShooting')} value={gear.burstSpeed || '--'} />
                    <SpecRow label={t('isoRange')} value={gear.isoRange || '--'} />
                    <SpecRow label={t('evfResolution')} value={gear.evfResolution || '--'} />
                    <SpecRow label={t('evfMagnification')} value={gear.evfMagnification || '--'} />
                  </div>
                </div>

                {/* 3. Hardware & Physical Section */}
                <div className="mb-8 border-t border-white/5 pt-4">
                  <div className="text-red-500 text-[10px] uppercase tracking-widest font-bold mb-4">{t('hardware')}</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-1">
                    <SpecRow label={t('lcdSpec')} value={gear.lcdSpec || '--'} />
                    <SpecRow label={t('cardSlots')} value={gear.cardSlots || '--'} />
                    <SpecRow label={t('batterySpec')} value={gear.batterySpec || '--'} />
                    <SpecRow label={t('ports')} value={gear.ports || '--'} />
                    <SpecRow label={t('weight')} value={weightLabel(gear) || '--'} />
                    <SpecRow label={t('dimensions')} value={gear.dimensions || '--'} />
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
