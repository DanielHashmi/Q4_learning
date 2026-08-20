function firstN(items, count) {
  if (!Number.isInteger(count) || count < 0) {
    throw new TypeError("count must be a non-negative integer");
  }
  return items.slice(0, count);
}

module.exports = { firstN };
