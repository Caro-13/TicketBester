CREATE INDEX IF NOT EXISTS idx_event_date ON event(start_at);
CREATE INDEX IF NOT EXISTS idx_event_type ON event(type_id);
CREATE INDEX IF NOT EXISTS idx_event_room ON event(room_id);
CREATE INDEX IF NOT EXISTS idx_event_status ON event(status);
CREATE INDEX IF NOT EXISTS idx_event_on_sale ON event(status, start_at)
    WHERE status = 'on_sale' OR status = 'on_site';

CREATE INDEX IF NOT EXISTS idx_event_seat_status ON event_seat(status);
CREATE INDEX IF NOT EXISTS idx_event_seat_event ON event_seat(event_id);

CREATE INDEX IF NOT EXISTS idx_reservation_client ON reservation(client_id)
    WHERE client_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_reservation_event ON reservation(event_id);
CREATE INDEX IF NOT EXISTS idx_reservation_status ON reservation(status);

CREATE INDEX IF NOT EXISTS idx_ticket_reservation ON ticket(reservation_id);
CREATE INDEX IF NOT EXISTS idx_ticket_event ON ticket(event_id);
CREATE INDEX IF NOT EXISTS idx_ticket_seat ON ticket(seat_id);

CREATE INDEX IF NOT EXISTS idx_payment_reservation ON payment(reservation_id);

CREATE INDEX IF NOT EXISTS idx_seat_sector ON seat(sector_id);
CREATE INDEX IF NOT EXISTS idx_seat_room ON seat(room_id);

CREATE INDEX IF NOT EXISTS idx_tarif_event ON tarif(event_id);

CREATE INDEX IF NOT EXISTS idx_scan_ticket ON scan_ticket(ticket_id);
CREATE INDEX IF NOT EXISTS idx_scan_staff ON scan_ticket(staff_id);