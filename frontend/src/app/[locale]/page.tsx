import { useTranslations } from 'next-intl';
import { Camera, ChevronRight, Zap, Database, Scale, Layers } from 'lucide-react';
import { Link } from '@/i18n/routing';

export default function HomePage() {
  const tNav = useTranslations('Navigation');
  const tc = useTranslations('Common');

  const heroImages = [
    { brand: 'SONY', model: 'A1 II', src: '/images/products/sony/sony-a1-ii.jpg', delay: '0ms' },
    { brand: 'NIKON', model: 'Z9', src: '/images/products/nikon/nikon-z9.jpg', delay: '150ms' },
    { brand: 'CANON', model: 'EOS R1', src: '/images/products/canon/canon-eos-r1.jpg', delay: '300ms' },
    { brand: 'FUJIFILM', model: 'GFX100 II', src: '/images/products/fujifilm/fujifilm-gfx100-ii.jpg', delay: '450ms' }
  ];

  return (
    <div className="flex flex-col min-h-screen bg-black text-white selection:bg-red-500/30">
      {/* Header */}
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

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center relative overflow-hidden">
        {/* Abstract Background Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-red-900/20 blur-[120px] rounded-full pointer-events-none" />

        <div className="max-w-7xl mx-auto w-full px-8 py-20 flex flex-col items-center text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm mb-8">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span className="text-[10px] uppercase tracking-widest font-bold text-gray-300">Database v2.0 Live</span>
          </div>

          <h2 className="text-6xl md:text-8xl font-black tracking-tighter uppercase mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-gray-500">
            The Ultimate <br/> Gear Archive
          </h2>
          
          <p className="max-w-2xl text-lg text-gray-400 font-light mb-12">
            A meticulously curated, high-fidelity database covering the flagship ecosystems of Sony, Nikon, Canon, and Fujifilm. Explore technical specifications, compare lenses, and discover the history of modern optics.
          </p>

          <Link 
            href="/database" 
            className="group relative inline-flex items-center gap-4 px-8 py-4 bg-white text-black font-bold uppercase tracking-widest overflow-hidden transition-all hover:scale-105"
          >
            <span className="relative z-10">Enter Database</span>
            <ChevronRight className="w-5 h-5 relative z-10 group-hover:translate-x-1 transition-transform" />
            <div className="absolute inset-0 bg-red-600 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-in-out z-0" />
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-in-out z-0 text-white flex items-center justify-center gap-4">
              <span>Enter Database</span>
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>
        </div>

        {/* Floating Gear Showcase */}
        <div className="w-full max-w-6xl mx-auto px-8 pb-20 relative z-10">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {heroImages.map((img, idx) => (
              <div 
                key={idx} 
                className="group flex flex-col items-center bg-[#0a0a0a] border border-white/5 p-6 transition-all duration-500 hover:border-white/20 hover:bg-[#111] hover:-translate-y-2"
                style={{ animationDelay: img.delay }}
              >
                <div className="text-red-500 text-[10px] font-bold tracking-widest uppercase mb-4 opacity-50 group-hover:opacity-100 transition-opacity">
                  {img.brand}
                </div>
                <div className="h-40 w-full flex items-center justify-center relative mb-4">
                  <div className="absolute inset-0 bg-gradient-to-b from-transparent to-white/5 opacity-0 group-hover:opacity-100 transition-opacity rounded-full blur-xl" />
                  <img 
                    src={img.src} 
                    alt={img.model} 
                    className="w-full h-full object-contain relative z-10 drop-shadow-2xl transition-transform duration-700 group-hover:scale-110" 
                  />
                </div>
                <div className="text-gray-400 font-medium uppercase tracking-wider text-sm">{img.model}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Feature Highlights */}
        <div className="w-full border-t border-white/5 bg-[#050505]">
          <div className="max-w-7xl mx-auto px-8 py-24 grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="flex flex-col items-center text-center">
              <Database className="w-8 h-8 text-red-500 mb-6" />
              <h3 className="text-lg font-bold uppercase tracking-widest mb-3">Vast Collection</h3>
              <p className="text-sm text-gray-500 leading-relaxed font-light">Over 140+ meticulously documented cameras and lenses, featuring pure RGB 0,0,0 high-resolution isolations.</p>
            </div>
            <div className="flex flex-col items-center text-center">
              <Scale className="w-8 h-8 text-red-500 mb-6" />
              <h3 className="text-lg font-bold uppercase tracking-widest mb-3">Deep Comparison</h3>
              <p className="text-sm text-gray-500 leading-relaxed font-light">Instantly cross-reference technical metrics, optical formulas, and dimensions across multiple systems.</p>
            </div>
            <div className="flex flex-col items-center text-center">
              <Layers className="w-8 h-8 text-red-500 mb-6" />
              <h3 className="text-lg font-bold uppercase tracking-widest mb-3">Historical Accuracy</h3>
              <p className="text-sm text-gray-500 leading-relaxed font-light">Trace the lineage of legendary optical designs from DSLR eras to the modern mirrorless revolution.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
