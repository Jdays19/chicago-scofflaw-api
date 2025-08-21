CREATE INDEX IF NOT EXISTS idx_v_date ON violations (violation_date);
CREATE INDEX IF NOT EXISTS idx_v_addr ON violations ((lower(trim(address))));
CREATE INDEX IF NOT EXISTS idx_s_addr ON scofflaws ((lower(trim(address))));
