CREATE OR REPLACE FUNCTION prevent_double_booking()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM event_seat
        WHERE event_id = NEW.event_id
          AND seat_id = NEW.seat_id
          AND status IN ('SOLD','RESERVED')
    ) THEN
        RAISE EXCEPTION 'Seat % already booked for event %',
            NEW.seat_id, NEW.event_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Removed from project scope
/*CREATE OR REPLACE FUNCTION check_hold_expiration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'HOLD'
       AND NEW.hold_expires_at IS NOT NULL
       AND NEW.hold_expires_at < NOW() THEN
        NEW.status := 'AVAILABLE';
        NEW.hold_expires_at := NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;*/

CREATE OR REPLACE FUNCTION sync_seat_with_reservation()
RETURNS TRIGGER AS $$
BEGIN
    -- Reservation is now 'paid' → mark seats as SOLD
    IF NEW.status = 'paid' AND (OLD.status IS DISTINCT FROM 'paid') THEN
        UPDATE event_seat es
        SET status = 'SOLD'
        FROM ticket t
        WHERE t.reservation_id = NEW.id
          AND es.event_id = t.event_id
          AND es.seat_id = t.seat_id;

    -- Reservation is now 'pending' → mark seats as RESERVED
    ELSIF NEW.status = 'pending' AND (OLD.status IS DISTINCT FROM 'pending') THEN
        UPDATE event_seat es
        SET status = 'RESERVED'
        FROM ticket t
        WHERE t.reservation_id = NEW.id
          AND es.event_id = t.event_id
          AND es.seat_id = t.seat_id;

    -- Reservation is now cancelled/expired/failed → mark seats as AVAILABLE
    ELSIF NEW.status IN ('cancelled', 'expired', 'failed')
          AND (OLD.status IS DISTINCT FROM NEW.status OR OLD.status IS DISTINCT FROM 'cancelled')
    THEN
        UPDATE event_seat es
        SET status = 'AVAILABLE' /*, hold_expires_at = NULL*/
        FROM ticket t
        WHERE t.reservation_id = NEW.id
          AND es.event_id = t.event_id
          AND es.seat_id = t.seat_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_reservation_on_payment()
RETURNS TRIGGER AS $$
DECLARE
    current_status reservation_status;
BEGIN
    -- Check current reservation status
    SELECT status INTO current_status
    FROM reservation
    WHERE id = NEW.reservation_id;

    -- If already paid, raise an exception
    IF current_status = 'paid' THEN
        RAISE EXCEPTION 'Reservation % is already paid', NEW.reservation_id;
    END IF;

    -- normal update
    UPDATE reservation
    SET status = 'paid'
    WHERE id = NEW.reservation_id AND status = 'pending';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_event_capacity()
RETURNS TRIGGER AS $$
DECLARE
    seat_exists BOOLEAN;
BEGIN
    SELECT EXISTS(
        SELECT 1 FROM event_seat
        WHERE event_id = NEW.event_id AND seat_id = NEW.seat_id
    ) INTO seat_exists;

    IF NOT seat_exists THEN
        RAISE EXCEPTION 'Seat % is not available for event %', NEW.seat_id, NEW.event_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- tigger when tickets inserted (because reservation already created and no update)
CREATE OR REPLACE FUNCTION sync_seats_with_ticket()
RETURNS TRIGGER AS $$
BEGIN
    -- Get the reservation status
    DECLARE
        res_status reservation_status;
    BEGIN
        SELECT status INTO res_status
        FROM reservation
        WHERE id = NEW.reservation_id;

        -- Update seat based on reservation status
        IF res_status = 'pending' THEN
            UPDATE event_seat
            SET status = 'RESERVED'
            WHERE event_id = NEW.event_id AND seat_id = NEW.seat_id;
        ELSIF res_status = 'paid' THEN
            UPDATE event_seat
            SET status = 'SOLD'
            WHERE event_id = NEW.event_id AND seat_id = NEW.seat_id;
        END IF;
    END;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;