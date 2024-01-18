import { faker } from '@faker-js/faker';
import fs from 'fs';

// Function to read names from a file
function readNamesFromFile(filename) {
    try {
        const data = fs.readFileSync(filename, 'utf8');
        return data.split('\n');
    } catch (err) {
        console.error('Error reading from file:', err);
        return [];
    }
}

const names = readNamesFromFile('names.txt');
const groups = readNamesFromFile('groups.txt');

// Function to generate a specified number of fake data documents for bulk insert
function generateFakeDataForBulk( outputFile, indexName) {
    if (names.length < 2 || groups.length < 1) {
        console.error('Not enough data in files');
        return;
    }

    let bulkData = '';

    for (let i = 0; i < names.length; i++) {
        const serviceName = names[i];
        const domainName = names[Math.floor(Math.random() * names.length)];
        const group = groups[Math.floor(Math.random() * groups.length)];
        const additionalName = faker.random.word();

        const doc = {
            "serviceName": serviceName,
            "kind": "SPAN_KIND_CLIENT",
            "destination": {
                "resource": `oteldemo.${serviceName}/${additionalName}`,
                "domain": domainName
            },
            "target": null,
            "traceGroupName": group,
            "hashId": "UOwC+hoZOfhXEDa/OnqcAQ=="
        };

        // Add action metadata for Elasticsearch bulk API
        bulkData += JSON.stringify({ index: { _index: indexName, _id: i } }) + '\n';
        bulkData += JSON.stringify(doc) + '\n';
    }

    // Write the bulk data to a file
    fs.writeFileSync(outputFile, bulkData);
}

// Example usage: Generate 100 documents for 'my_custom_index' and write to 'bulk_data.json'
generateFakeDataForBulk( 'bulk_data.json', 'my_custom_index');
