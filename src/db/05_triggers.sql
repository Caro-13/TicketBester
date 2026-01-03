CREATE OR REPLACE TRIGGER trg_prevent_double_booking
BEFORE INSERT ON ticket
FOR EACH ROW
EXECUTE FUNCTION prevent_double_booking();

CREATE OR REPLACE TRIGGER trg_check_hold_expiration
BEFORE UPDATE ON event_seat
FOR EACH ROW
EXECUTE FUNCTION check_hold_expiration();

CREATE OR REPLACE TRIGGER trg_sync_seats_with_reservation
AFTER INSERT OR UPDATE ON reservation
FOR EACH ROW
EXECUTE FUNCTION sync_seat_with_reservation();

CREATE OR REPLACE TRIGGER trg_payment_confirms_reservation
AFTER INSERT ON payment
FOR EACH ROW
EXECUTE FUNCTION update_reservation_on_payment();

CREATE OR REPLACE TRIGGER trg_validate_ticket_seat
BEFORE INSERT ON ticket
FOR EACH ROW
EXECUTE FUNCTION check_event_capacity();