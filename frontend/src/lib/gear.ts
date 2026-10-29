// Types and helpers only. The data itself lives in gear-data.ts so client components
// that import from here don't pull products.json into the browser bundle.

// Shape of one record in products.json. scripts/validate-products.mjs keeps the data in line with it.
export type Gear = {
  id: string;
  slug?: string;
  brand: string;
  modelName: string;
  gearType: 'LENS' | 'CAMERA_BODY';
  aliases?: string[];
  image_url?: string;
  officialUrl?: string;
  mounts?: { mount: { name: string } }[];
  sensorFormat?: string;
  series?: string;
  category?: string;
  releaseYear?: number;   // year it was announced (kept separate so the year filter stays simple)
  releaseMonth?: number;  // 1-12, month it was announced, when known
  launchPrice?: number;     // Taiwan launch suggested price (NT$)
  retailPrice?: number;     // current Taiwan street price for new stock; cards and sorting use it only when there is no launch price
  retailPriceDate?: string; // "2026-10", when retailPrice was checked
  weightGrams?: number | string;
  dimensions?: string;
  hasWeatherSeal?: boolean;

  // lens
  lensType?: string;
  focalLengthMinMm?: number;
  focalLengthMaxMm?: number;
  apertureMax?: number | string;
  minAperture?: string;
  maxMagnification?: number | string;
  closeFocus?: string;
  filterSizeMm?: number;
  motorType?: string;
  opticalDesign?: string;
  specialElements?: string;
  coatings?: string;
  hasOIS?: boolean;
  hasApertureRing?: boolean;
  hasCustomButton?: boolean;

  // camera body
  fixedLens?: string;       // built-in lens of a fixed-lens camera (a body with no mounts), e.g. "23mm F2 (35mm equiv.)"
  megapixels?: number | string;
  sensorType?: string;
  processor?: string;
  isoRange?: string;
  burstSpeed?: string;
  afPoints?: string;
  afTargets?: string;
  afRange?: string;
  hasIBIS?: boolean;
  ibisRating?: string;
  videoResolution?: string;
  videoColorDepth?: string;
  logSupport?: string;
  evfResolution?: string;
  evfMagnification?: string;
  lcdSpec?: string;
  cardSlots?: string;
  batterySpec?: string;
  ports?: string;
};

// weightGrams is a number, or free text like "Approx. 630 g (including battery and card)"
export function weightLabel(g: Gear) {
  return typeof g.weightGrams === 'number' ? `${g.weightGrams}g` : g.weightGrams;
}

export function weightValue(g: Gear) {
  return Number(String(g.weightGrams ?? '').replace(/,/g, '').match(/\d+(\.\d+)?/)?.[0]) || undefined;
}

// Filter category: a body with no mount is a fixed-lens camera (action cams often publish no lens spec, so fixedLens can be empty)
export function gearKind(g: Gear) {
  return g.gearType === 'LENS' ? 'LENS' : g.mounts?.length ? 'CAMERA_BODY' : 'FIXED_LENS';
}

// Launch price when known, else the street price
export function priceValue(g: Gear) {
  return g.launchPrice ?? g.retailPrice;
}

// "NT$39,990", or "Street NT$32,990" when only the street price is known
export function priceText(g: Gear, streetLabel: string) {
  if (g.launchPrice) return `NT$${g.launchPrice.toLocaleString()}`;
  if (g.retailPrice) return `${streetLabel} NT$${g.retailPrice.toLocaleString()}`;
}

// Stored in a spec field when the official spec confirms the feature doesn't exist (no EVF, no Log); shown as 無 / None
export const NONE = 'None';

// afTargets is stored in English; the zh pages swap each known word for its Chinese name
const AF_TARGET_ZH: Record<string, string> = {
  'Eye Control AF': '眼控對焦', 'Action Priority': '動作優先', 'Sport Mode': '運動模式',
  Human: '人物', Humans: '人物', People: '人物', Face: '臉部', Eye: '眼睛',
  Animal: '動物', Animals: '動物', Pet: '寵物', Dog: '狗', Dogs: '狗', Cat: '貓', Cats: '貓',
  Bird: '鳥類', Birds: '鳥類', Horse: '馬', Horses: '馬', Insect: '昆蟲', Fish: '魚',
  Vehicle: '交通工具', Vehicles: '交通工具', Car: '汽車', Cars: '汽車', Automobile: '汽車',
  Motorcycle: '機車', Motorcycles: '機車', Bicycle: '自行車', Bicycles: '自行車', Bike: '兩輪車',
  Train: '火車', Trains: '火車', Airplane: '飛機', Airplanes: '飛機', Plane: '飛機', Aircraft: '飛機', Helicopter: '直升機',
};
const AF_TARGET_WORD = new RegExp(`\\b(${Object.keys(AF_TARGET_ZH).sort((a, b) => b.length - a.length).join('|')})\\b`, 'g');

export function afTargetsLabel(value: string | undefined, locale: string) {
  if (!value || value === NONE || locale !== 'zh') return value;
  return value.replace(AF_TARGET_WORD, w => AF_TARGET_ZH[w]).replace(/, /g, '、').replace(/ ?\(/g, '（').replace(/\)/g, '）').replace(/\//g, '／');
}

// "2026.09", or just "2026" when the month isn't known
export function releaseLabel(g: Gear) {
  if (!g.releaseYear) return undefined;
  return g.releaseMonth ? `${g.releaseYear}.${String(g.releaseMonth).padStart(2, '0')}` : String(g.releaseYear);
}

// Sort key: a known month sorts after "month unknown" within the same year
export function releaseKey(g: Gear) {
  return (g.releaseYear || 0) * 100 + (g.releaseMonth || 0);
}

export function focalLength(g: Gear) {
  if (!g.focalLengthMinMm) return undefined;
  return g.focalLengthMinMm === g.focalLengthMaxMm
    ? `${g.focalLengthMinMm}mm`
    : `${g.focalLengthMinMm}-${g.focalLengthMaxMm}mm`;
}
