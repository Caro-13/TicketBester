-- Master file to create de database

\echo 'Starting database initialization...'
\echo ''

\echo '1/6 Creating ENUM types...'
\i 'src/db/01_types.sql'
\echo '✓ ENUM types created'
\echo ''

\echo '2/6 Creating tables...'
\i 'src/db/02_tables.sql'
\echo '✓ Tables created'
\echo ''

\echo '3/6 Creating indexes...'
\i 'src/db/03_indexes.sql'
\echo '✓ Indexes created'
\echo ''

\echo '4/6 Creating functions...'
\i 'src/db/04_functions.sql'
\echo '✓ Functions created'
\echo ''

\echo '5/6 Creating triggers...'
\i 'src/db/05_triggers.sql'
\echo '✓ Triggers created'
\echo ''

\echo '6/6 Initialisation of the db...'
\i 'src/db/06_init_db.sql'
\echo '✓ Initialisation finished'
\echo ''