'use client';

import { useState, useEffect } from 'react';
import { ArrowRightLeft, Check } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function CompareButton({ gearId, locale }: { gearId: number, locale: string }) {
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const router = useRouter();

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('compare_ids');
    if (stored) {
      setSelectedIds(JSON.parse(stored));
    }
  }, []);

  const isSelected = selectedIds.includes(gearId);

  const toggleSelect = () => {
    const newIds = isSelected 
      ? selectedIds.filter(id => id !== gearId)
      : [...selectedIds, gearId];
    
    setSelectedIds(newIds);
    localStorage.setItem('compare_ids', JSON.stringify(newIds));
  };

  const goToCompare = () => {
    if (selectedIds.length > 0) {
      router.push(`/${locale}/compare?ids=${selectedIds.join(',')}`);
    }
  };

  return (
    <div className="flex gap-4 w-full">
      <button 
        onClick={toggleSelect}
        className={`flex-1 font-medium py-3 px-6 uppercase tracking-wider text-sm transition-colors flex items-center justify-center gap-2 border
          ${isSelected 
            ? 'bg-red-600 border-red-600 text-white hover:bg-red-700' 
            : 'bg-transparent border-white/20 text-gray-300 hover:border-white hover:text-white'}`}
      >
        {isSelected ? <Check className="w-4 h-4" /> : <ArrowRightLeft className="w-4 h-4" />}
        {isSelected ? 'Selected' : 'Add to Compare'}
      </button>
      
      {selectedIds.length > 0 && (
        <button 
          onClick={goToCompare}
          className="bg-white text-black hover:bg-gray-200 font-bold py-3 px-8 uppercase tracking-wider text-sm transition-colors"
        >
          Compare ({selectedIds.length})
        </button>
      )}
    </div>
  );
}
