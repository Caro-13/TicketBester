-- Mocktest infos
INSERT INTO room (id, name, address) VALUES
(1, 'ISC Room','Rue de l''Industrie 42,1950 Sion');


INSERT INTO sector (id, name, supplement, room_id) VALUES
(1, 'Main Floor', 0.00, 1), -- Standard + Easy Access + VIP
(2, 'Balcony', 15.00, 1);

INSERT INTO type_of_seat (id, type) VALUES
(1, 'Standard'),
(2, 'Easy Access'),
(3, 'VIP'),
(4, 'Balcony');

INSERT INTO seat (id, name, type_id, sector_id, room_id) VALUES
-- Main Floor
(1, 'A01', 1, 1, 1),
(2, 'A02', 1, 1, 1),
(3, 'A03', 1, 1, 1),
(4, 'A04', 1, 1, 1),
(5, 'B01', 1, 1, 1),
(6, 'B02', 1, 1, 1),
(7, 'B03', 1, 1, 1),
(8, 'B04', 1, 1, 1),
(9, 'C01', 2, 1, 1),  -- Easy Access
(10, 'C02', 1, 1, 1),
(11, 'C03', 1, 1, 1),
(12, 'C04', 2, 1, 1),  -- Easy Access
-- VIP
(13, 'D01', 3, 1, 1),
(14, 'D02', 3, 1, 1),
(15, 'D03', 3, 1, 1),
(16, 'D04', 3, 1, 1),
-- Balcony
(17, 'E01', 4, 2, 1),
(18, 'E02', 4, 2, 1),
(19, 'E03', 4, 2, 1),
(20, 'E04', 4, 2, 1);

INSERT INTO configuration (id, name) VALUES
(1, 'Main Floor'), -- sector 1
(2, 'Balcony'), -- sector 2
(3, 'Full Room'); -- sector 1 + 2

INSERT INTO config_with_sector (config_id, sector_id) VALUES
(1, 1), -- Main Floor only
(2, 2), -- Balcony only
(3, 1), -- Full Room
(3, 2);

INSERT INTO type_of_event (id, name, is_free, need_reservation) VALUES
(1, 'Concert', false, true),
(2, 'Exposition', true, false),
(3, 'Festival', false, true),
(4, 'Conférence', true, true),
(5, 'Pièce de Théâtre', false, true);

INSERT INTO event (id, type_id, name, start_at, end_at, room_id, config_id, status) VALUES
(1, 1, 'Concert de Rock: Tour 2025', '2026-07-15 20:00:00', '2026-07-15 22:30:00', 1, 1, 'on_sale'),
(2, 2, 'Rétrospective Picasso', '2026-08-01 10:00:00', '2026-08-01 18:00:00', 1, 2, 'on_sale'),
(3, 3, 'Festival du Rire', '2026-09-10 18:30:00', '2026-09-11 03:00:00', 1, 3, 'on_sale'),
(4, 4, 'Conférence Tech 2026', '2026-10-05 09:00:00', '2026-10-05 17:00:00', 1, 1, 'on_sale'),
(5, 5, 'Otello par la Troupe Nationale', '2026-11-20 19:30:00', '2026-11-20 21:30:00', 1, 3, 'on_sale');



--event_seat
INSERT INTO event_seat (event_id, seat_id, status, hold_expires_at) VALUES
-- event 1 : Main Floor
(1, 1, 'AVAILABLE', NULL),
(1, 2, 'AVAILABLE', NULL),
(1, 3, 'AVAILABLE', NULL),
(1, 4, 'AVAILABLE', NULL),
(1, 5, 'AVAILABLE', NULL),
(1, 6, 'AVAILABLE', NULL),
(1, 7, 'AVAILABLE', NULL),
(1, 8, 'AVAILABLE', NULL),
(1, 9, 'AVAILABLE', NULL),
(1, 10, 'AVAILABLE', NULL),
(1, 11, 'AVAILABLE', NULL),
(1, 12, 'AVAILABLE', NULL),
(1, 13, 'AVAILABLE', NULL),
(1, 14, 'AVAILABLE', NULL),
(1, 15, 'AVAILABLE', NULL),
(1, 16, 'AVAILABLE', NULL),
-- event 2 : Balcony
(2, 17, 'AVAILABLE', NULL),
(2, 18, 'AVAILABLE', NULL),
(2, 19, 'AVAILABLE', NULL),
(2, 20, 'AVAILABLE', NULL),
-- event 3 : Full Room
(3, 1, 'AVAILABLE', NULL),
(3, 2, 'AVAILABLE', NULL),
(3, 3, 'AVAILABLE', NULL),
(3, 4, 'AVAILABLE', NULL),
(3, 5, 'AVAILABLE', NULL),
(3, 6, 'AVAILABLE', NULL),
(3, 7, 'AVAILABLE', NULL),
(3, 8, 'AVAILABLE', NULL),
(3, 9, 'AVAILABLE', NULL),
(3, 10, 'AVAILABLE', NULL),
(3, 11, 'AVAILABLE', NULL),
(3, 12, 'AVAILABLE', NULL),
(3, 13, 'AVAILABLE', NULL),
(3, 14, 'AVAILABLE', NULL),
(3, 15, 'AVAILABLE', NULL),
(3, 16, 'AVAILABLE', NULL),
(3, 17, 'AVAILABLE', NULL),
(3, 18, 'AVAILABLE', NULL),
(3, 19, 'AVAILABLE', NULL),
(3, 20, 'AVAILABLE', NULL),
-- event 4 : Main Floor
(4, 1, 'AVAILABLE', NULL),
(4, 2, 'AVAILABLE', NULL),
(4, 3, 'AVAILABLE', NULL),
(4, 4, 'AVAILABLE', NULL),
(4, 5, 'AVAILABLE', NULL),
(4, 6, 'AVAILABLE', NULL),
(4, 7, 'AVAILABLE', NULL),
(4, 8, 'AVAILABLE', NULL),
(4, 9, 'AVAILABLE', NULL),
(4, 10, 'AVAILABLE', NULL),
(4, 11, 'AVAILABLE', NULL),
(4, 12, 'AVAILABLE', NULL),
(4, 13, 'AVAILABLE', NULL),
(4, 14, 'AVAILABLE', NULL),
(4, 15, 'AVAILABLE', NULL),
(4, 16, 'AVAILABLE', NULL),
-- event 5
(5, 1, 'AVAILABLE', NULL),
(5, 2, 'AVAILABLE', NULL),
(5, 3, 'AVAILABLE', NULL),
(5, 4, 'AVAILABLE', NULL),
(5, 5, 'AVAILABLE', NULL),
(5, 6, 'AVAILABLE', NULL),
(5, 7, 'AVAILABLE', NULL),
(5, 8, 'AVAILABLE', NULL),
(5, 9, 'AVAILABLE', NULL),
(5, 10, 'AVAILABLE', NULL),
(5, 11, 'AVAILABLE', NULL),
(5, 12, 'AVAILABLE', NULL),
(5, 13, 'AVAILABLE', NULL),
(5, 14, 'AVAILABLE', NULL),
(5, 15, 'AVAILABLE', NULL),
(5, 16, 'AVAILABLE', NULL),
(5, 17, 'AVAILABLE', NULL),
(5, 18, 'AVAILABLE', NULL),
(5, 19, 'AVAILABLE', NULL),
(5, 20, 'AVAILABLE', NULL);



INSERT INTO client (id, mail, firstname, lastname) VALUES
(1, 'john.doe@example.com', 'John', 'Doe'),
(2, 'jane.smith@example.com', 'Jane', 'Smith'),
(3, 'alice.martin@example.com', 'Alice', 'Martin');


INSERT INTO staff (id, name) VALUES
(2, 'Delta'),
(3, 'Echo');

INSERT INTO tarif (id, event_id, name, price, discount_id) VALUES--event 1
(1, 1, 'Normal', 50.00, NULL),
(2, 1, 'Student', 35.00, NULL),
(3, 1, 'Staff',25.00,NULL),
-- event 2 free
(4, 2, 'Normal', 0.00, NULL),
(5, 2, 'Student', 0.00, NULL),
(6, 2, 'Staff',0.00,NULL),
-- event 3
(7, 3, 'Normal', 30.00, NULL),
(8, 3, 'Student', 25.00, NULL),
(9, 3, 'Staff', 15.00, NULL),
-- event 4 free
(10, 4, 'Normal', 0.00, NULL),
(11, 4, 'Student', 0.00, NULL),
(12, 4, 'Staff',0.00,NULL),
-- event 5
(13, 5, 'Normal', 12.00, NULL),
(14, 5, 'Student', 10.00, NULL),
(15, 5, 'Staff', 6.00, NULL);



-------------------------------------------------------------

-- Reservation 1: staff Delta
INSERT INTO reservation (id, event_id, vendor, status, reservation_time, client_id) VALUES
(1, 1, 2, 'paid', '2025-12-15 14:30:00', NULL);

INSERT INTO ticket (id, reservation_id, event_id, seat_id, tarif_name) VALUES
(1, 1, 1, 1, 'Normal'),
(2, 1, 1, 2, 'Normal'),
(3, 1, 1, 3, 'Student');

INSERT INTO payment (id, reservation_id, total, method, payed_at) VALUES
(1, 1, 135.00, 'cash', '2025-12-15 14:35:00');

-- Reservation 2: Staff Echo
INSERT INTO reservation (id, event_id, vendor, status, reservation_time, client_id) VALUES
(2, 1, 3, 'paid', '2025-12-15 15:45:00', NULL);

INSERT INTO ticket (id, reservation_id, event_id, seat_id, tarif_name) VALUES
(4, 2, 1, 5, 'Student'),
(5, 2, 1, 9, 'Normal'),
(6, 2, 1, 10, 'Staff');

INSERT INTO payment (id, reservation_id, total, method, payed_at) VALUES
(2, 2, 135.00, 'card', '2025-12-15 15:50:00');

-- Reservation 3: Online by John Doe
INSERT INTO reservation (id, event_id, vendor, status, reservation_time, client_id) VALUES
(3, 1, 1, 'pending', '2025-12-16 10:20:00', 1);

INSERT INTO ticket (id, reservation_id, event_id, seat_id, tarif_name) VALUES
(7, 3, 1, 4, 'Student');
-------------------------------------------------------------
-- Reset sequences to avoid conflicts
SELECT setval('client_id_seq', (SELECT MAX(id) FROM client));
SELECT setval('staff_id_seq', (SELECT MAX(id) FROM staff));
SELECT setval('discount_id_seq', (SELECT MAX(id) FROM discount));
SELECT setval('type_of_seat_id_seq', (SELECT MAX(id) FROM type_of_seat));
SELECT setval('room_id_seq', (SELECT MAX(id) FROM room));
SELECT setval('sector_id_seq', (SELECT MAX(id) FROM sector));
SELECT setval('seat_id_seq', (SELECT MAX(id) FROM seat));
SELECT setval('configuration_id_seq', (SELECT MAX(id) FROM configuration));
SELECT setval('type_of_event_id_seq', (SELECT MAX(id) FROM type_of_event));
SELECT setval('event_id_seq', (SELECT MAX(id) FROM event));
SELECT setval('tarif_id_seq', (SELECT MAX(id) FROM tarif));
SELECT setval('reservation_id_seq', (SELECT MAX(id) FROM reservation));
SELECT setval('ticket_id_seq', (SELECT MAX(id) FROM ticket));
SELECT setval('payment_id_seq', (SELECT MAX(id) FROM payment));

---------------
-- Updates for mock data (doesn't trigger the triggers at this point...)
UPDATE event_seat es
SET status = 'SOLD'
FROM ticket t
JOIN reservation r ON r.id = t.reservation_id
WHERE r.status = 'paid'
  AND es.event_id = t.event_id
  AND es.seat_id = t.seat_id;

UPDATE event_seat es
SET status = 'RESERVED'
FROM ticket t
JOIN reservation r ON r.id = t.reservation_id
WHERE r.status = 'pending'
  AND es.event_id = t.event_id
  AND es.seat_id = t.seat_id;
