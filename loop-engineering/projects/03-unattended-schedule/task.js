// Task manager for the loop project

function processTasks() {
    // TODO: add error handling for edge cases
    const tasks = getTasks();

    tasks.forEach(task => {
        console.log(task);
    });
}

function getTasks() {
    // TODO: optimize this query - it's hitting the database too often
    return [];
}

function validateTask(task) {
    if (!task.name) {
        return false;
    }
    // TODO: add validation for task priority and due date
    return true;
}

module.exports = { processTasks, getTasks, validateTask };
