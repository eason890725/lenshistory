import { Camera } from 'lucide-react';
import { Link } from '@/i18n/routing';
import {setRequestLocale, getTranslations} from 'next-intl/server';
import GearGrid from './GearGrid';

import products from '@/data/products.json';

// Transform the flat JSON data into the multi-language structure expected by the UI
function getGears() {
  return products.map((item: any, index: number) => ({
    ...item,
    id: item.id || (index + 1),
    brand: typeof item.brand === 'string' ? { 
      slug: item.brand.toLowerCase(), 
      nameI18n: { enUs: item.brand, zhTw: item.brand } 
    } : item.brand,
    modelNameI18n: typeof item.modelName === 'string' ? {
      enUs: item.modelName,
      zhTw: item.modelName
    } : item.modelNameI18n
  }));
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
  const gears = getGears();

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
