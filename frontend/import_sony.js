const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

const EXCEL_FILE = '../Sony FE Lens.xlsx';
const OUTPUT_FILE = './src/data/products.json';

async function run() {
    try {
        console.log('Attempting to read:', EXCEL_FILE);
        const workbook = XLSX.readFile(EXCEL_FILE, { cellDates: true });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        
        // Convert to JSON
        const rawData = XLSX.utils.sheet_to_json(worksheet);
        console.log(`Successfully read ${rawData.length} rows from Excel.`);

        // Map to our schema
        const mappedProducts = rawData.map((row, index) => {
            // Find keys dynamically as column names might vary
            const name = row['Lens Name'] || row['Model'] || row['Name'] || Object.values(row)[0];
            const specs = row['Specs'] || row['Specifications'] || '';
            
            return {
                id: 5000 + index, // High ID range for imported lenses
                brand: "Sony",
                modelName: name,
                gearType: "LENS",
                lensType: name.toLowerCase().includes('zoom') ? 'ZOOM' : 'PRIME',
                releaseYear: row['Year'] || 2023,
                launchPrice: row['Price'] || 0,
                specs: specs
            };
        });

        // Backup handled by caller, but we verify here
        console.log(`Mapped ${mappedProducts.length} Sony lenses.`);
        
        fs.writeFileSync(OUTPUT_FILE, JSON.stringify(mappedProducts, null, 2), 'utf-8');
        console.log('IMPORT_SUCCESS');
        console.log('COUNT:' + mappedProducts.length);
        console.log('SAMPLE_NAMES:' + mappedProducts.slice(0, 5).map(p => p.modelName).join('|'));

    } catch (e) {
        console.error('IMPORT_ERROR:', e.message);
        process.exit(1);
    }
}

run();
