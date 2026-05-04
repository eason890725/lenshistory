'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Camera, Check } from 'lucide-react';
import { Link } from '@/i18n/routing';

interface CameraCardProps {
  gear: any;
  isSelected: boolean;
  isDisabled: boolean;
  onToggle: (e: React.MouseEvent, gear: any) => void;
  t: (key: string) => string;
  tc: (key: string) => string;
}

export default function CameraCard({ gear, isSelected, isDisabled, onToggle, t, tc }: CameraCardProps) {
  const name = gear.modelNameI18n?.enUs || gear.modelName || 'Unknown';
  const brandName = typeof gear.brand === 'string' 
    ? gear.brand 
    : (gear.brand?.nameI18n?.enUs || gear.brand?.name || gear.brand || 'Unknown');
  const isLens = gear.gearType === 'LENS';

  return (
    <div className={`relative group ${isDisabled ? 'opacity-40' : ''}`}>
      {/* Compare Checkbox */}
      <div 
        className={`absolute top-4 left-4 z-20 w-6 h-6 border flex items-center justify-center transition-colors cursor-pointer
          ${isSelected ? 'bg-red-600 border-red-600' : 'bg-black/50 border-white/50 hover:border-white'}`}
        onClick={(e) => onToggle(e, gear)}
        title={tc('compare')}
      >
        {isSelected && <Check className="w-4 h-4 text-white" />}
      </div>

      <Link href={`/database/${gear.slug || gear.id}`} className="block h-full">
        <Card className={`bg-[#1A1A1A] border-none rounded-none hover:ring-1 transition-all cursor-pointer h-full ${isSelected ? 'ring-2 ring-red-500' : 'hover:ring-red-500'}`}>
          <div className="h-52 bg-black/50 flex items-center justify-center border-b border-white/5 relative overflow-hidden">
            {gear.imageUrl ? (
              <img 
                src={gear.imageUrl} 
                alt={name} 
                className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-700 p-4"
              />
            ) : (
              <div className="flex flex-col items-center gap-2">
                <Camera className="w-12 h-12 text-gray-800" />
                <span className="text-[10px] text-gray-700 font-bold uppercase tracking-widest">{gear.gearType}</span>
              </div>
            )}
            <div className="absolute top-2 right-2 bg-red-600 text-white text-[10px] font-bold px-2 py-0.5 uppercase tracking-tighter">
              {brandName}
            </div>
            {gear.sensorFormat && (
              <div className="absolute bottom-2 left-2 bg-black/80 text-gray-400 text-[9px] px-2 py-0.5 border border-white/10 uppercase tracking-widest">
                {gear.sensorFormat}
              </div>
            )}
          </div>
          <CardHeader className="pb-2">
            <CardTitle className="text-lg font-medium text-gray-200 leading-tight h-12 overflow-hidden line-clamp-2">
              {name}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-[11px] text-gray-500 space-y-1 font-mono uppercase tracking-tight">
              <div className="flex justify-between border-b border-white/5 pb-1">
                <span>{t('releaseYear')}</span>
                <span className="text-gray-300">{gear.releaseYear}</span>
              </div>
              {isLens ? (
                gear.focalLengthMinMm && (
                  <div className="flex justify-between border-b border-white/5 pb-1">
                    <span>{t('focalLength')}</span>
                    <span className="text-gray-300">
                      {gear.focalLengthMinMm === gear.focalLengthMaxMm 
                        ? `${gear.focalLengthMinMm}mm` 
                        : `${gear.focalLengthMinMm}-${gear.focalLengthMaxMm}mm`} 
                      {" "}f/{gear.apertureMax}
                    </span>
                  </div>
                )
              ) : (
                gear.megapixels && (
                  <div className="flex justify-between border-b border-white/5 pb-1">
                    <span>{t('megapixels')}</span>
                    <span className="text-gray-300">{gear.megapixels}MP</span>
                  </div>
                )
              )}
              {gear.weightGrams && (
                <div className="flex justify-between border-b border-white/5 pb-1">
                  <span>{t('weight')}</span>
                  <span className="text-gray-300">{gear.weightGrams}g</span>
                </div>
              )}
              {isLens && gear.filterSizeMm && (
                <div className="flex justify-between border-b border-white/5 pb-1">
                  <span>{t('filterSize')}</span>
                  <span className="text-gray-300">{gear.filterSizeMm}mm</span>
                </div>
              )}
              {!isLens && gear.videoResolution && (
                <div className="flex justify-between border-b border-white/5 pb-1">
                  <span>{t('video')}</span>
                  <span className="text-gray-300 text-[10px] truncate ml-4 text-right">{gear.videoResolution}</span>
                </div>
              )}
              {gear.launchPrice && (
                <div className="flex justify-between border-b border-white/5 pb-1">
                  <span>{t('launchPrice')}</span>
                  <span className="text-gray-300">NT${Number(gear.launchPrice).toLocaleString()}</span>
                </div>
              )}
            </div>
            {/* Feature badges */}
            <div className="flex flex-wrap gap-1 mt-2">
              {gear.hasOIS && <span className="bg-green-900/30 text-green-400 text-[8px] px-1.5 py-0.5 uppercase tracking-wider">{t('ois')}</span>}
              {gear.hasIBIS && <span className="bg-blue-900/30 text-blue-400 text-[8px] px-1.5 py-0.5 uppercase tracking-wider">{t('ibis')}</span>}
              {gear.hasWeatherSeal && <span className="bg-blue-900/30 text-blue-400 text-[8px] px-1.5 py-0.5 uppercase tracking-wider">{t('weatherSeal')}</span>}
              {gear.hasApertureRing && <span className="bg-amber-900/30 text-amber-400 text-[8px] px-1.5 py-0.5 uppercase tracking-wider">{t('apertureRing')}</span>}
              {gear.series && <span className="bg-red-900/30 text-red-400 text-[8px] px-1.5 py-0.5 uppercase tracking-wider">{gear.series}</span>}
            </div>
            {/* Mounts */}
            <div className="flex flex-wrap gap-1 mt-2 border-t border-white/5 pt-2">
               {gear.mounts && Array.isArray(gear.mounts) && gear.mounts.map((gm: any) => (
                 <span key={gm.id || gm.mount?.name} className="bg-gray-800/50 text-gray-400 text-[7px] px-1.5 py-0.5 uppercase tracking-tighter border border-white/5">
                   {gm.mount?.name || gm.name || 'Unknown Mount'}
                 </span>
               ))}
            </div>
          </CardContent>
        </Card>
      </Link>
    </div>
  );
}
