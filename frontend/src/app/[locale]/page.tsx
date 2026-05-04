import {useTranslations} from 'next-intl';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Camera, TrendingUp } from 'lucide-react';
import { Link } from '@/i18n/routing';
import { PriceChart } from '@/components/features/PriceChart';

export default function HomePage() {
  const t = useTranslations('Dashboard');
  const tNav = useTranslations('Navigation');

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header / Navigation */}
      <header className="border-b border-white/10 p-4 flex justify-between items-center bg-black/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <Camera className="w-6 h-6 text-red-600" />
          <h1 className="text-xl font-bold tracking-widest uppercase">LensHistory</h1>
        </div>
        <nav className="flex gap-6 text-sm font-medium text-gray-400">
          <Link href="/" className="text-white hover:text-red-500 transition-colors">{tNav('home')}</Link>
          <Link href="/database" className="hover:text-red-500 transition-colors">{tNav('database')}</Link>
        </nav>
        <div className="flex gap-4">
          <Link href="/" locale="en" className="text-xs hover:text-white transition-colors">EN</Link>
          <span className="text-xs text-gray-600">|</span>
          <Link href="/" locale="zh" className="text-xs hover:text-white transition-colors">繁</Link>
        </div>
      </header>

      {/* Main Dashboard Content */}
      <main className="flex-1 p-8 max-w-7xl mx-auto w-full space-y-8">
        
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-light text-gray-300 tracking-wider uppercase mb-2">{t('myGears')}</h2>
            <p className="text-gray-500">Your personalized photography gear collection.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-[#1A1A1A] border-none rounded-none">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-400 uppercase tracking-widest">{t('totalValue')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-light text-white">$14,500</div>
            </CardContent>
          </Card>

          <Card className="bg-[#1A1A1A] border-none rounded-none relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4">
              <TrendingUp className="w-6 h-6 text-green-500/50" />
            </div>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-400 uppercase tracking-widest">{t('valueChange')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-light text-green-500">+2.4%</div>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-[#1A1A1A] border-none rounded-none h-[400px] p-6">
          <div className="h-full w-full">
            <PriceChart />
          </div>
        </Card>

      </main>
    </div>
  );
}
