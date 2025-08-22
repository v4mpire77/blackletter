import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import yaml from 'yaml';

export interface RuleMeta {
  id: string;
  version: string;
  text: string;
}

export function loadRuleMetadata(rulesDir: string): Map<string, RuleMeta> {
  const meta = new Map<string, RuleMeta>();
  const files = listRuleFiles(rulesDir);
  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    const data = yaml.parse(content);
    if (data && data.id) {
      meta.set(data.id, {
        id: data.id,
        version: data.source?.version_label || 'unknown',
        text: data.title || ''
      });
    }
  }
  return meta;
}

function listRuleFiles(dir: string): string[] {
  let files: string[] = [];
  for (const entry of fs.readdirSync(dir)) {
    const full = path.join(dir, entry);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      files = files.concat(listRuleFiles(full));
    } else if (entry.endsWith('.yml') || entry.endsWith('.yaml')) {
      files.push(full);
    }
  }
  return files.sort();
}

export function computeRulesetHash(rulesDir: string): string {
  const files = listRuleFiles(rulesDir);
  const hash = crypto.createHash('sha256');
  for (const file of files) {
    hash.update(fs.readFileSync(file));
  }
  return hash.digest('hex');
}
