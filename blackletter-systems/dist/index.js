"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
const app = (0, express_1.default)();
app.use(express_1.default.json());
app.get('/health', (_req, res) => {
    res.json({ ok: true, service: 'blackletter', ts: new Date().toISOString() });
});
// Demo: rules/evidence endpoints
app.get('/api/rules', (_req, res) => {
    res.json({ items: [
            { rule_id: 'gdpr-dpa-1', domain: 'property', title: 'DPA clause present', version: '1.0.0' },
            { rule_id: 'aml-kyc-1', domain: 'property', title: 'KYC checks referenced', version: '1.0.0' }
        ] });
});
app.get('/api/evidence/:flagId', (req, res) => {
    const { flagId } = req.params;
    res.json({
        flag_id: flagId,
        source_url: "https://ico.org.uk/",
        source_version: "2025-08-01",
        approver_id: "advisor-001",
        timestamp: new Date().toISOString()
    });
});
const port = Number(process.env.PORT || 3000);
app.listen(port, () => {
    console.log(`Blackletter dev server listening on http://localhost:${port}`);
});
