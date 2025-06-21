UPDATE general_holding_snapshot 
SET evaluated_amount = evaluated_amount -781645.00
WHERE id = 25;

insert into general_holding_snapshot (isa_account_id, snapshot_type, snapshot_date, evaluated_amount)
values (6,'CASH', '2025-01-31 23:59:59', 14092530.00);

insert into general_holding_snapshot (isa_account_id, snapshot_type, snapshot_date, evaluated_amount)
values (6,'CASH', '2025-02-28 23:59:59', 14092530.00);

insert into general_holding_snapshot (isa_account_id, snapshot_type, snapshot_date, evaluated_amount)
values (6,'CASH', '2025-03-31 23:59:59', 14092530.00);

insert into general_holding_snapshot (isa_account_id, snapshot_type, snapshot_date, evaluated_amount)
values (6,'CASH', '2025-04-30 23:59:59', 14092530.00);

insert into general_holding_snapshot (isa_account_id, snapshot_type, snapshot_date, evaluated_amount)
values (6,'CASH', '2025-05-30 23:59:59', 10101220.00);

insert into general_holding_snapshot (isa_account_id, snapshot_type, snapshot_date, evaluated_amount)
values (6,'CASH', '2025-06-30 23:59:59', 10666450.00);