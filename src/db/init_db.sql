-- Mocktest infos
INSERT INTO client (id, mail, prenom, nom) VALUES
(1, 'john.doe@example.com', 'John', 'Doe'),
(2, 'jane.smith@example.com', 'Jane', 'Smith');

INSERT INTO staff (id, name) VALUES
(1, 'Online'),
(2, 'Delta'),
(3, 'Echo');

INSERT INTO discount (id, value, code) VALUES
(1, 20, 'STUDENT20'),
(2, 15, 'EARLYBIRD15');

INSERT INTO typeOfSeat (id, type) VALUES 
(1, 'Standard'),
(2, 'Easy Access'),
(3, 'VIP');

INSERT INTO room (id, name, nbSeats, subRoom) VALUES
(1, 'Main Hall', 0, NULL),
(2, 'Balcony', 0, 1);

INSERT INTO seat (id, typeId) VALUES
('A01', 1),
('A02', 1),
('A03', 1),
('B01', 2), --easy
('B02', 1),
('B03', 1),
('C01', 2), --easy
('C02', 1),
('C03', 1),
('D01', 1),
('D02', 1),
('D03', 1);

INSERT INTO typeOfEvent (id, name, isFree, needReservation, sittingPlanId) VALUES 
(1, 'Concert de Rock', false, true, 1),
(2, 'Exposotion d art', true,false,1),
(3,'Festival de jazz',false,true,1),
(4,'Conférence Tech',true,true,1),
(5,'Pièce de théâtre',false,true,1);

INSERT INTO event (id, typeId, date, hour, dateFin, heureFin,name) VALUES
(1, 1, '2026-07-15', '20:00:00', '2026-07-15', '22:30:00','Concert de Rock'),
(2,2,'2026-08-01','10:00','2026-08-01','18:00','Exposition d''Art'),
(3,3,'2026-09-10','18:30','2026-09-11','03:00','Festival de Jazz'),
(4,4,'2026-10-05','09:00','2026-10-05','10:00','Conférence Tech'),
(5,5,'2026-11-20','19:30','2026-11-20','21:00','Otello');

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