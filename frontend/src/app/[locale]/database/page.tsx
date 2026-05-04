import { Camera } from 'lucide-react';
import { Link } from '@/i18n/routing';
import {setRequestLocale, getTranslations} from 'next-intl/server';
import GearGrid from './GearGrid';

// This is a server component, we will fetch data from our Spring Boot backend.
// We catch errors to fallback to mock data if the backend isn't running yet.
async function getGears(searchParams: { brand?: string, type?: string, q?: string }) {
  try {
    const backendBase = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8083';
    // Add timestamp to bypass cache
    const url = new URL(`${backendBase}/api/v1/gear/search?t=${Date.now()}`);
    if (searchParams.brand) url.searchParams.append('brandId', searchParams.brand);
    if (searchParams.type) url.searchParams.append('type', searchParams.type);
    if (searchParams.q) url.searchParams.append('q', searchParams.q);

    const res = await fetch(url.toString(), { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch data');
    return res.json();
  } catch (error) {
    console.error('Backend is not reachable, using mock data:', error);
    // Mock data for UI preview
    return [
      {
        id: 1,
        brand: { slug: "sony", nameI18n: { enUs: "Sony", zhTw: "索尼" } },
        modelNameI18n: { enUs: "Sony a7 III", zhTw: "Sony a7 III" },
        gearType: "CAMERA_BODY",
        releaseYear: 2018,
        sensorFormat: "Full Frame"
      },
      {
        id: 2,
        brand: { slug: "sony", nameI18n: { enUs: "Sony", zhTw: "索尼" } },
        modelNameI18n: { enUs: "Sony FE 50mm f/1.8", zhTw: "Sony FE 50mm f/1.8" },
        gearType: "LENS",
        releaseYear: 2016,
        focalLengthMinMm: 50,
        focalLengthMaxMm: 50,
        apertureMax: 1.8,
        sensorFormat: "Full Frame"
      },
      {
        id: 3,
        brand: { slug: "sigma", nameI18n: { enUs: "Sigma", zhTw: "適馬" } },
        modelNameI18n: { enUs: "Sigma 35mm f/1.4 DG DN Art", zhTw: "Sigma 35mm f/1.4 DG DN Art" },
        gearType: "LENS",
        releaseYear: 2021,
        focalLengthMinMm: 35,
        focalLengthMaxMm: 35,
        apertureMax: 1.4,
        sensorFormat: "Full Frame"
      }
    ];
  }
}


export default async function DatabasePage({
  searchParams,
  params
}: {
  searchParams: Promise<{ brand?: string, type?: string, q?: string }>;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const tc = await getTranslations('Common');

  const resolvedSearchParams = await searchParams;
  const gears = await getGears(resolvedSearchParams);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header / Navigation */}
      <header className="border-b border-white/10 p-4 flex justify-between items-center bg-black/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <Camera className="w-6 h-6 text-red-600" />
          <h1 className="text-xl font-bold tracking-widest uppercase">LensHistory</h1>
        </div>
        <nav className="flex gap-6 text-sm font-medium text-gray-400">
          <Link href="/" className="hover:text-red-500 transition-colors">Home</Link>
          <Link href="/database" className="text-white hover:text-red-500 transition-colors">Gear Database</Link>
        </nav>
        <div className="flex gap-4">
          <Link href="/database" locale="en" className="text-xs hover:text-white transition-colors">EN</Link>
          <span className="text-xs text-gray-600">|</span>
          <Link href="/database" locale="zh" className="text-xs hover:text-white transition-colors">繁</Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 p-8 max-w-7xl mx-auto w-full">
        <div className="mb-8 border-b border-white/10 pb-6">
          <h2 className="text-4xl font-light text-white tracking-tighter uppercase mb-2">
            {tc('database')}
          </h2>
          <p className="text-xs text-gray-500 tracking-[0.3em] uppercase font-bold">
            {gears.length} {tc('itemsTotal')}
          </p>
        </div>

        <GearGrid gears={gears} locale={locale} />
      </main>
    </div>
  );
}
