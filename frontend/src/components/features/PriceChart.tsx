"use client";

import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
  { date: "Jan", value: 12000 },
  { date: "Feb", value: 12200 },
  { date: "Mar", value: 12500 },
  { date: "Apr", value: 13000 },
  { date: "May", value: 12800 },
  { date: "Jun", value: 13500 },
  { date: "Jul", value: 14000 },
  { date: "Aug", value: 14500 },
];

export function PriceChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data} margin={{ top: 20, right: 0, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#E50000" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#E50000" stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis 
          dataKey="date" 
          stroke="#888888" 
          fontSize={12} 
          tickLine={false} 
          axisLine={false} 
          dy={10}
        />
        <YAxis 
          stroke="#888888" 
          fontSize={12} 
          tickLine={false} 
          axisLine={false} 
          tickFormatter={(value) => `$${value}`}
          dx={-10}
        />
        <Tooltip 
          contentStyle={{ backgroundColor: "#1A1A1A", border: "1px solid #333", borderRadius: 0 }}
          itemStyle={{ color: "#E0E0E0" }}
          labelStyle={{ color: "#888888", marginBottom: 4 }}
        />
        <Area 
          type="monotone" 
          dataKey="value" 
          stroke="#E50000" 
          strokeWidth={2}
          fillOpacity={1} 
          fill="url(#colorValue)" 
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
