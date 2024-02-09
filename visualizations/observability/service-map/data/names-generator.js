import { faker } from '@faker-js/faker';
import fs from 'fs';

// Function to generate a specified number of unique names
function generateNames(size) {
    const names = new Set();

    while(names.size < size) {
        names.add(faker.internet.userName());
    }

    return Array.from(names);
}

// Function to write names to a file
function writeNamesToFile(filename, size) {
    const names = generateNames(size);
    fs.writeFile(filename, names.join('\n'), err => {
        if (err) {
            console.error('Error writing to file:', err);
        } else {
            console.log(`Successfully wrote ${size} names to ${filename}`);
        }
    });
}

// Usage - specify the size as needed
writeNamesToFile('groups.txt', 20); // Adjust the size as needed
writeNamesToFile('names.txt', 100); // Adjust the size as needed
