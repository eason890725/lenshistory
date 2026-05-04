import { Camera, ChevronLeft, X } from 'lucide-react';
import { Link } from '@/i18n/routing';
import { setRequestLocale, getTranslations } from 'next-intl/server';

async function getCompareGears(ids: string) {
  if (!ids) return [];
  try {
    const backendBase = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8083';
    const res = await fetch(`${backendBase}/api/v1/gear/compare?ids=${ids}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch data');
    return res.json();
  } catch (error) {
    console.error('Backend is not reachable:', error);
    return [];
  }
}

function focalStr(g: any) {
  if (!g.focalLengthMinMm) return 'N/A';
  return g.focalLengthMinMm === g.focalLengthMaxMm
    ? `${g.focalLengthMinMm}mm`
    : `${g.focalLengthMinMm}-${g.focalLengthMaxMm}mm`;
}

function boolStr(val: boolean | null | undefined, tc: any) {
  if (val === null || val === undefined) return '-';
  return val ? tc('yes') : tc('no');
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
  const gears = await getCompareGears(ids);

  const specRows = [
    // --- Lens Specific ---
    { section: t('optical'), label: t('focalLength'), render: (g: any) => g.gearType === 'LENS' ? focalStr(g) : null },
    { section: t('optical'), label: t('maxAperture'), render: (g: any) => g.gearType === 'LENS' ? (g.apertureMax ? `f/${g.apertureMax}` : '-') : null },
    { section: t('optical'), label: t('minAperture'), render: (g: any) => g.gearType === 'LENS' ? (g.apertureMin ? `f/${g.apertureMin}` : '-') : null },
    { section: t('optical'), label: t('zoomRatio'), render: (g: any) => g.gearType === 'LENS' ? (g.zoomRatio ? `${g.zoomRatio.toFixed(2)}x` : '-') : null },
    { section: t('optical'), label: t('filterSize'), render: (g: any) => g.gearType === 'LENS' ? (g.filterSizeMm ? `${g.filterSizeMm}mm` : '-') : null },
    
    // --- Body Specific ---
    { section: t('sensorType'), label: t('megapixels'), render: (g: any) => g.gearType === 'CAMERA_BODY' ? (g.megapixels ? `${g.megapixels}MP` : '-') : null },
    { section: t('sensorType'), label: t('sensorType'), render: (g: any) => g.gearType === 'CAMERA_BODY' ? (g.sensorType || '-') : null },
    { section: t('sensorType'), label: t('processor'), render: (g: any) => g.gearType === 'CAMERA_BODY' ? (g.processor || '-') : null },
    { section: t('sensorType'), label: t('maxIso'), render: (g: any) => g.gearType === 'CAMERA_BODY' ? (g.maxIso ? Number(g.maxIso).toLocaleString() : '-') : null },
    { section: t('features'), label: t('video'), render: (g: any) => g.gearType === 'CAMERA_BODY' ? (g.videoResolution || '-') : null },
    { section: t('features'), label: t('continuousShooting'), render: (g: any) => g.gearType === 'CAMERA_BODY' ? (g.continuousShootingFps ? `${g.continuousShootingFps} fps` : '-') : null },
    { section: t('features'), label: t('ibis'), render: (g: any) => g.gearType === 'CAMERA_BODY' ? boolStr(g.hasIBIS, tc) : null },

    // --- Shared ---
    { section: t('physical'), label: t('weight'), render: (g: any) => g.weightGrams ? `${g.weightGrams}g` : '-' },
    { section: t('physical'), label: t('dimensions'), render: (g: any) => g.dimensions || '-' },
    { section: t('features'), label: t('weatherSeal'), render: (g: any) => boolStr(g.hasWeatherSeal, tc) },
    
    // --- More Lens Specific ---
    { section: t('features'), label: t('ois'), render: (g: any) => g.gearType === 'LENS' ? boolStr(g.hasOIS, tc) : null },
    { section: t('features'), label: t('apertureRing'), render: (g: any) => g.gearType === 'LENS' ? boolStr(g.hasApertureRing, tc) : null },
    
    // --- Release Info ---
    { section: t('releaseInfo'), label: t('releaseYear'), render: (g: any) => g.releaseYear || '-' },
    { section: t('releaseInfo'), label: t('launchPrice'), render: (g: any) => g.launchPrice ? `NT$${Number(g.launchPrice).toLocaleString()}` : '-' },
  ].filter(row => {
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
                  {gears.map((g: any) => (
                    <th key={g.id} className="p-6 border-b border-white/10 text-center min-w-[280px] bg-black/20">
                      <div className="h-36 mb-3 flex items-center justify-center relative group">
                        {g.imageUrl ? (
                          <img src={g.imageUrl} alt={g.modelNameI18n.enUs} className="w-full h-full object-contain p-4 group-hover:scale-105 transition-transform duration-500" />
                        ) : (
                          <Camera className="w-12 h-12 text-gray-800" />
                        )}
                      </div>
                      <h3 className="font-medium text-white text-base mb-1 leading-tight h-12 overflow-hidden line-clamp-2">
                        {g.modelNameI18n.enUs}
                      </h3>
                      <div className="text-xs text-red-500 font-bold tracking-widest uppercase mb-1">
                        {g.brand.nameI18n.enUs}
                        {g.series && <span className="text-amber-500 ml-2">{g.series}</span>}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {specRows.map((row, idx) => {
                  const showSectionHeader = row.section !== lastSection;
                  lastSection = row.section;
                  return (
                    <>
                      {showSectionHeader && (
                        <tr key={`section-${row.section}`}>
                          <td colSpan={1 + gears.length} className="bg-white/[0.03] px-6 py-2 border-t border-b border-white/10">
                            <span className="text-red-500 text-[10px] font-bold uppercase tracking-widest">{row.section}</span>
                          </td>
                        </tr>
                      )}
                      <tr key={idx} className={`${idx % 2 === 0 ? 'bg-white/[0.01]' : ''} hover:bg-white/5 transition-colors group`}>
                        <td className="p-4 font-bold text-gray-500 uppercase text-[10px] tracking-widest border-r border-white/5 bg-black/50 sticky left-0 z-10 group-hover:text-white transition-colors">
                          {row.label}
                        </td>
                        {gears.map((g: any) => (
                          <td key={g.id} className="p-4 text-center text-white font-light text-sm">
                            {row.render(g)}
                          </td>
                        ))}
                      </tr>
                    </>
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

