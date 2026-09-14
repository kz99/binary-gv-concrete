import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const data = JSON.parse(readFileSync(resolve(root, 'data/records.json'), 'utf8'));
const N = 2 ** 30;
const D = (7 * N) / 16;

const ids = new Set();
let previousRate = Infinity;

for (const record of data.records) {
  if (ids.has(record.id)) throw new Error(`duplicate record id: ${record.id}`);
  ids.add(record.id);
  if (record.blockLength !== N) throw new Error(`${record.id}: block length is not 2^30`);
  if (record.minimumDistance < D) throw new Error(`${record.id}: distance is below 7n/16`);
  if (Math.abs(record.rate - record.dimension / N) > 1e-15) {
    throw new Error(`${record.id}: rate does not equal dimension / block length`);
  }
  if (record.status === 'verified') {
    if (record.verification.arithmetic !== 'passed' || record.verification.proof !== 'passed') {
      throw new Error(`${record.id}: verified entry has an incomplete audit`);
    }
    if (record.verification.reviewers < 2 || new Set(record.verification.agents).size < 2) {
      throw new Error(`${record.id}: verified entry needs two separate AI verifier agents`);
    }
    if (record.verification.writing !== 'passed') {
      throw new Error(`${record.id}: verified entry has not passed the pragmatic writing review`);
    }
    const acceptedReviews = record.verification.reviews.filter(
      (review) => review.decision === 'accepted' && review.correctness === 'passed' && review.writing === 'passed',
    );
    if (acceptedReviews.length < 2 || new Set(acceptedReviews.map((review) => review.agent)).size < 2) {
      throw new Error(`${record.id}: verified entry needs two recorded independent acceptances`);
    }
    if (record.rate > previousRate) throw new Error('verified records are not rate-sorted');
    previousRate = record.rate;
  }
  if (!existsSync(resolve(root, record.proofPath))) {
    throw new Error(`${record.id}: missing proof note ${record.proofPath}`);
  }
}

console.log(`Validated ${data.records.length} exact-size code records.`);
