-- Create types as Enum
CREATE TYPE seat_status AS ENUM (
    'AVAILABLE',
    'RESERVED',
    --'HOLD', --removed from project scope
    'SOLD',
    'UNAVAILABLE'
);

CREATE TYPE reservation_status AS ENUM (
    'pending',
    'paid',
    'failed',
    'cancelled',
    'expired',
    'refunded'
);

CREATE TYPE event_status AS ENUM (
    'on_sale',
    'on_site',
    'closed',
    'sold_out',
    'cancelled',
    'archived'
);