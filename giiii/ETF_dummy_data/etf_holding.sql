CREATE TABLE `etf_holding_snapshot` (
	`id`	BIGINT	NOT NULL,
	`isa_account_id`	BIGINT	NOT NULL,
	`etf_id`	BIGINT	NOT NULL,
	`snapshot_date`	DATETIME	NOT NULL,
	`evaluated_amount`	Decimal(20, 2)	NOT NULL
);

INSERT INTO etf_holding (etf_id, isa_account_id, quantity, avg_cost, acquired_at, updated_at)
VALUES
(1, 6, 28.000000, 10020.00, '2025-01-02 10:00:00', '2025-01-02 11:30:00'),
(26, 6, 27.000000, 32010.00, '2025-01-02 11:00:00', '2025-01-02 11:30:00'),
(40, 6, 32.000000, 32215.00, '2025-01-02 10:30:00', '2025-01-02 11:30:00'),
(318, 6, 22.000000, 10095.00, '2025-01-02 09:30:00', '2025-01-02 11:30:00'),
(353, 6, 42.000000, 12135.00, '2025-01-02 11:30:00', '2025-01-02 11:30:00')
;