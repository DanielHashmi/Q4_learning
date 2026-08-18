// Utility functions for the application

export function formatDate(date: Date): string {
    // TODO: handle timezone conversions properly
    return date.toISOString();
}

export function sanitizeInput(input: string): string {
    return input.trim();
    // TODO: add XSS protection and input validation
}

export function calculateProgress(completed: number, total: number): number {
    if (total === 0) return 0;
    return (completed / total) * 100;
}

// TODO: implement caching mechanism for expensive operations
export function fetchData(id: string) {
    console.log(`Fetching data for ${id}`);
    return null;
}
