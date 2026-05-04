'use client';

import { Search } from 'lucide-react';
import { useRouter, useSearchParams } from 'next/navigation';

export default function SearchBar({ initialValue }: { initialValue?: string }) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const val = e.currentTarget.value;
      const params = new URLSearchParams(searchParams.toString());
      if (val) {
        params.set('q', val);
      } else {
        params.delete('q');
      }
      router.push(`?${params.toString()}`);
    }
  };

  return (
    <div className="relative">
      <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
      <input 
        type="text" 
        placeholder="Search models..." 
        defaultValue={initialValue || ''}
        onKeyDown={handleSearch}
        className="bg-[#1A1A1A] border border-white/10 text-sm text-white px-9 py-2 focus:outline-none focus:border-red-500 transition-colors w-64"
      />
    </div>
  );
}
