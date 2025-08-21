// Generates a simple status.json for the status page workflow
import fs from 'fs';
const status = {
  library_version: "rules-lib@1.0.0",
  last_update_iso: new Date().toISOString(),
  sla_days: Number(process.env.ASSURANCE_SLA_DAYS || 10),
  sla_met_rolling_90d: "N/A"
};
fs.mkdirSync('public', { recursive: true });
fs.writeFileSync('public/status.json', JSON.stringify(status, null, 2));
console.log("Status written to public/status.json");
