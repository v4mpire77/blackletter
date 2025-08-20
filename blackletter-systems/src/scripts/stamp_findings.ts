import fs from 'fs';
import path from 'path';
import { computeRulesetHash, loadRuleMetadata } from '../utils/provenance';

interface FindingInput {
  rule_id: string;
  evidence: {
    source_file: string;
    page: number;
    section?: string;
    snippet: string;
  };
}

interface FindingOutput extends FindingInput {
  rule_text: string;
  evidence_snippet: string;
  metadata: {
    rule_version: string;
    ruleset_hash: string;
    engine_version: string;
    source_file: string;
    page: number;
    section?: string;
    timestamp: string;
  };
}

const outDir = path.resolve('out');
const findingsPath = path.join(outDir, 'findings.json');
if (!fs.existsSync(findingsPath)) {
  console.error(`Missing findings file at ${findingsPath}`);
  process.exit(1);
}

const rulesDir = path.resolve('rules');
const rules = loadRuleMetadata(rulesDir);
const rulesetHash = computeRulesetHash(rulesDir);
const engineVersion = require('../../package.json').version;
const timestamp = new Date().toISOString();

const raw: FindingInput[] = JSON.parse(fs.readFileSync(findingsPath, 'utf-8'));
const stamped: FindingOutput[] = raw.map(f => {
  const rule = rules.get(f.rule_id);
  return {
    ...f,
    rule_text: rule?.text || '',
    evidence_snippet: f.evidence.snippet,
    metadata: {
      rule_version: rule?.version || 'unknown',
      ruleset_hash: rulesetHash,
      engine_version: engineVersion,
      source_file: f.evidence.source_file,
      page: f.evidence.page,
      section: f.evidence.section,
      timestamp
    }
  };
});

fs.writeFileSync(findingsPath, JSON.stringify(stamped, null, 2));

const manifest = {
  generated_at: timestamp,
  engine_version: engineVersion,
  ruleset_hash: rulesetHash
};
fs.mkdirSync('assurance', { recursive: true });
fs.writeFileSync(path.join('assurance', 'manifest.json'), JSON.stringify(manifest, null, 2));
console.log('Findings stamped with provenance metadata.');
