const XLSX = require('xlsx');
try {
    const workbook = XLSX.readFile('../Sony FE Lens.xlsx');
    const firstSheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[firstSheetName];
    const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
    console.log('COLUMNS:', data[0]);
    console.log('SAMPLE ROW:', data[1]);
} catch (e) {
    console.error('ERROR:', e.message);
}
