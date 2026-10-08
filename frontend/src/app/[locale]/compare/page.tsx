import { Fragment } from 'react';
import { Camera, ChevronLeft } from 'lucide-react';
import { Link } from '@/i18n/routing';
import { setRequestLocale, getTranslations } from 'next-intl/server';
import { focalLength, weightLabel, type Gear } from '@/lib/gear';
import { gears as allGears } from '@/lib/gear-data';

function getCompareGears(ids: string) {
  if (!ids) return [];
  const idList = ids.split(',').map(id => id.trim());
  return allGears.filter(g => idList.includes(g.id) || (g.slug && idList.includes(g.slug)));
}

// Appends the unit only to bare numbers; free-text values like "Approx. 630 g" are shown as-is
function withUnit(v: string | number | undefined, unit: string) {
  if (v === undefined || v === '') return '-';
  return /^\d+(\.\d+)?$/.test(String(v)) ? `${v}${unit}` : String(v);
}

function zoomRatio(g: Gear) {
  if (!g.focalLengthMinMm || !g.focalLengthMaxMm || g.focalLengthMinMm === g.focalLengthMaxMm) return '-';
  return `${(g.focalLengthMaxMm / g.focalLengthMinMm).toFixed(2)}x`;
}

export default async function ComparePage({
  searchParams,
  params
}: {
  searchParams: Promise<{ ids?: string }>;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const resolvedParams = await searchParams;
  const ids = resolvedParams.ids || '';

  const t = await getTranslations('GearSpecs');
  const tc = await getTranslations('Common');
  const gears = getCompareGears(ids);

  const bool = (v?: boolean) => (v === undefined ? '-' : v ? tc('yes') : tc('no'));
  const lens = (render: (g: Gear) => string) => (g: Gear) => (g.gearType === 'LENS' ? render(g) : null);
  const body = (render: (g: Gear) => string) => (g: Gear) => (g.gearType === 'CAMERA_BODY' ? render(g) : null);

  const specRows: { section: string; label: string; render: (g: Gear) => string | number | null }[] = [
    // --- Lens Specific ---
    { section: t('optical'), label: t('focalLength'), render: lens(g => focalLength(g) ?? '-') },
    { section: t('optical'), label: t('maxAperture'), render: lens(g => (g.apertureMax ? `f/${g.apertureMax}` : '-')) },
    { section: t('optical'), label: t('minAperture'), render: lens(g => (g.minAperture ? `f/${g.minAperture}` : '-')) },
    { section: t('optical'), label: t('zoomRatio'), render: lens(zoomRatio) },
    { section: t('optical'), label: t('filterSize'), render: lens(g => (g.filterSizeMm ? `${g.filterSizeMm}mm` : '-')) },

    // --- Body Specific ---
    { section: t('sensorType'), label: t('megapixels'), render: body(g => withUnit(g.megapixels, 'MP')) },
    { section: t('sensorType'), label: t('sensorType'), render: body(g => g.sensorType || '-') },
    { section: t('sensorType'), label: t('processor'), render: body(g => g.processor || '-') },
    { section: t('sensorType'), label: t('isoRange'), render: body(g => g.isoRange || '-') },
    { section: t('features'), label: t('video'), render: body(g => g.videoResolution || '-') },
    { section: t('features'), label: t('continuousShooting'), render: body(g => g.burstSpeed || '-') },
    { section: t('features'), label: t('ibis'), render: body(g => bool(g.hasIBIS)) },

    // --- Shared ---
    { section: t('physical'), label: t('weight'), render: g => weightLabel(g) || '-' },
    { section: t('physical'), label: t('dimensions'), render: g => g.dimensions || '-' },
    { section: t('features'), label: t('weatherSeal'), render: g => bool(g.hasWeatherSeal) },

    // --- More Lens Specific ---
    { section: t('features'), label: t('ois'), render: lens(g => bool(g.hasOIS)) },
    { section: t('features'), label: t('apertureRing'), render: lens(g => bool(g.hasApertureRing)) },

    // --- Release Info ---
    { section: t('releaseInfo'), label: t('releaseYear'), render: g => g.releaseYear || '-' },
    { section: t('releaseInfo'), label: t('launchPrice'), render: g => (g.launchPrice ? `NT$${g.launchPrice.toLocaleString()}` : '-') },
  ];
  const visibleRows = specRows.filter(row => {
    // Only show rows that have at least one non-null render result for the current set of gears
    return gears.some(g => row.render(g) !== null);
  });

  let lastSection = '';

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

      <main className="flex-1 max-w-7xl mx-auto w-full p-8 overflow-x-auto">
        <div className="mb-8">
          <Link href="/database" className="inline-flex items-center text-sm text-gray-500 hover:text-white transition-colors">
            <ChevronLeft className="w-4 h-4 mr-1" />
            {tc('backToDatabase')}
          </Link>
        </div>

        <h2 className="text-3xl font-light text-gray-300 tracking-wider uppercase mb-8">{tc('compare')}</h2>

        {gears.length === 0 ? (
          <div className="text-gray-500 text-center py-20">
            No gear selected for comparison. Please go to the database and select items to compare.
          </div>
        ) : (
          <div className="bg-[#111] border border-white/5 overflow-hidden">
            <table className="w-full text-left text-sm text-gray-300 border-collapse">
              <thead>
                <tr>
                  <th className="p-6 border-b border-white/10 w-48 font-bold uppercase tracking-widest text-gray-500 text-[10px] bg-black/50 sticky left-0 z-20">{t('fullSpecs')}</th>
                  {gears.map(g => (
                    <th key={g.id} className="p-6 border-b border-white/10 text-center min-w-[280px] bg-black/20">
                      <div className="h-36 mb-3 flex items-center justify-center relative group">
                        {g.image_url ? (
                          <img src={g.image_url} alt={g.modelName} className="w-full h-full object-contain p-4 group-hover:scale-105 transition-transform duration-500" />
                        ) : (
                          <Camera className="w-12 h-12 text-gray-800" />
                        )}
                      </div>
                      <h3 className="font-medium text-white text-base mb-1 leading-tight h-12 overflow-hidden line-clamp-2">
                        {g.modelName}
                      </h3>
                      <div className="text-xs text-red-500 font-bold tracking-widest uppercase mb-1">
                        {g.brand}
                        {g.series && <span className="text-amber-500 ml-2">{g.series}</span>}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {visibleRows.map((row, idx) => {
                  const showSectionHeader = row.section !== lastSection;
                  lastSection = row.section;
                  return (
                    <Fragment key={idx}>
                      {showSectionHeader && (
                        <tr>
                          <td colSpan={1 + gears.length} className="bg-white/[0.03] px-6 py-2 border-t border-b border-white/10">
                            <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{row.section}</span>
                          </td>
                        </tr>
                      )}
                      <tr className={`${idx % 2 === 0 ? 'bg-white/[0.01]' : ''} hover:bg-white/5 transition-colors group`}>
                        <td className="p-4 font-bold text-gray-500 uppercase text-[10px] tracking-widest border-r border-white/5 bg-black/50 sticky left-0 z-10 group-hover:text-white transition-colors">
                          {row.label}
                        </td>
                        {gears.map(g => (
                          <td key={g.id} className="p-4 text-center text-white font-light text-sm">
                            {row.render(g)}
                          </td>
                        ))}
                      </tr>
                    </Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

