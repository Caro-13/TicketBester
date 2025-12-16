-- Mocktest infos
INSERT INTO staff (id, name) VALUES 
(1, 'Online'),
(2, 'Delta'),
(3, 'Echo');

INSERT INTO client (id, mail, prenom, nom) VALUES 
(1, 'john.doe@example.com', 'John', 'Doe'),
(2, 'jane.smith@example.com', 'Jane', 'Smith');

INSERT INTO typeOfSeat (id, type) VALUES 
(1, 'Standard'),
(2, 'Easy Access'),
(3, 'VIP');

INSERT INTO seat (id, typeId) VALUES 
('A01', 1),
('A02', 1),
('A03', 1),
('B01', 2),
('B02', 1),
('B03', 1),
('C01', 2),
('C02', 1),
('C03', 1),
('D01', 1),
('D02', 1),
('D03', 1);

INSERT INTO sittingPlan (id, name) VALUES 
(1, 'Cinema Test');

INSERT INTO sittingPlan_seat (sittingPlanId, seatId) VALUES 
(1, 'A01'),
(1, 'A02'),
(1, 'A03'),
(1, 'B01'),
(1, 'B02'),
(1, 'B03'),
(1, 'C01'),
(1, 'C02'),
(1, 'C03'),
(1, 'D01'),
(1, 'D02'),
(1, 'D03');

INSERT INTO typeOfEvent (id, name, isFree, needReservation, sittingPlanId) VALUES 
(1, 'Cinema', false, true, 1);

INSERT INTO event (id, typeId, date, hour, dateFin, heureFin) VALUES 
(1, 1, '2025-12-20', '20:00:00', '2025-12-20', '22:30:00');

INSERT INTO discount (id, value, code) VALUES 
(1, 20, 'STUDENT20'),
(2, 15, 'EARLYBIRD15');

INSERT INTO tarif (id, eventId, name, price, discountId) VALUES 
(1, 1, 'Normal', 12.00, NULL),
(2, 1, 'Student', 10.00, NULL),
(3, 1, 'Easy Access', 12.00, NULL),
(4, 1, 'Early Bird', 12.00, 2),
(5,1,'Staff',8.00,NULL);

INSERT INTO event_seat_status (eventId, seatId, isTaken, isHold) VALUES 
(1, 'A01', true, false),
(1, 'A02', true, false),
(1, 'A03', true, false),
(1, 'B01', true, false),
(1, 'C01', true, false),
(1, 'C02', true, false),
(1, 'D01', true, false);

-- Reservation 1: staff Delta
INSERT INTO reservation (id, eventId, vendor, reservationTime, clientId) VALUES 
(1, 1, 2, '2025-12-15 14:30:00', NULL);

INSERT INTO ticket (reservationId,eventId, seatId, tarifName, isScanned) VALUES 
(1, 1, 'A01', 'Normal', false),
(1, 1, 'A02', 'Normal', false),
(1, 1, 'A03', 'Normal', false);

-- Reservation 2: staff Echo
INSERT INTO reservation (id, eventId, vendor, reservationTime, clientId) VALUES 
(2, 1, 3, '2025-12-15 15:45:00', NULL);

INSERT INTO ticket (reservationId, eventId, seatId, tarifName, isScanned) VALUES 
(2, 1, 'C01', 'Student', false),
(2, 1, 'C02', 'Student', false),
(2, 1, 'B01', 'Easy Access', false),
(2, 1, 'D01', 'Early Bird', false);

-- Reservation 3: online by John Doe
INSERT INTO reservation (id, eventId, vendor, reservationTime, clientId) VALUES 
(3, 1, 1, '2025-12-15 16:20:00', 1);

INSERT INTO ticket (reservationId, eventId, seatId, tarifName, isScanned) VALUES 
(3, 1, 'D02', 'Early Bird', false),
(3, 1, 'D03', 'Staff', false);