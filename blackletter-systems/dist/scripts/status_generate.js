"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
// Generates a simple status.json for the status page workflow
const fs_1 = __importDefault(require("fs"));
const status = {
    library_version: "rules-lib@1.0.0",
    last_update_iso: new Date().toISOString(),
    sla_days: Number(process.env.ASSURANCE_SLA_DAYS || 10),
    sla_met_rolling_90d: "N/A"
};
fs_1.default.mkdirSync('public', { recursive: true });
fs_1.default.writeFileSync('public/status.json', JSON.stringify(status, null, 2));
console.log("Status written to public/status.json");
