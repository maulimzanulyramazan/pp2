-- ============================================
-- STORED PROCEDURES AND FUNCTIONS
-- For PhoneBook application
-- ============================================

-- PROCEDURE 1: Add phone to existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,  -- Contact's name
    p_phone VARCHAR,         -- Phone number to add
    p_type VARCHAR           -- Type: home/work/mobile
)
AS $$
DECLARE
    v_contact_id INTEGER;    -- Variable to store contact ID
BEGIN
    -- Find contact ID by name
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    
    -- Check if contact exists
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact with name "%" does not exist', p_contact_name;
    ELSE
        -- Insert new phone number
        INSERT INTO phones (contact_id, phone, type) 
        VALUES (v_contact_id, p_phone, p_type);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- PROCEDURE 2: Move contact to group (creates group if needed)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,  -- Contact's name
    p_group_name VARCHAR     -- Target group name
)
AS $$
DECLARE
    v_group_id INTEGER;      -- Group ID variable
    v_contact_id INTEGER;    -- Contact ID variable
BEGIN
    -- Get contact ID
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    
    -- Check if contact exists
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact with name "%" does not exist', p_contact_name;
    END IF;
    
    -- Try to find existing group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    -- Create group if it doesn't exist
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) 
        RETURNING id INTO v_group_id;
    END IF;
    
    -- Update contact's group
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$ LANGUAGE plpgsql;

-- FUNCTION 3: Enhanced search across all fields
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INTEGER,                      -- Contact ID
    name VARCHAR(100),               -- Contact name
    phone_numbers TEXT,              -- All phone numbers (concatenated)
    email VARCHAR(100),              -- Email address
    birthday DATE,                   -- Birthday date
    group_name VARCHAR(50),          -- Group name
    created_at TIMESTAMP             -- Creation timestamp
)
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,                                                       -- Contact ID
        c.name,                                                     -- Name
        STRING_AGG(DISTINCT p.phone || '(' || p.type || ')', ', ')  -- Phones with types
            AS phone_numbers,
        c.email,                                                    -- Email
        c.birthday,                                                 -- Birthday
        g.name AS group_name,                                       -- Group name
        c.created_at                                                -- Creation time
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id      -- Join with phones
    LEFT JOIN groups g ON c.group_id = g.id        -- Join with groups
    WHERE c.name ILIKE '%' || p_query || '%'       -- Search in name
       OR c.email ILIKE '%' || p_query || '%'      -- Search in email
       OR p.phone ILIKE '%' || p_query || '%'      -- Search in phone
       OR g.name ILIKE '%' || p_query || '%'       -- Search in group
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- EXISTING PROCEDURES FROM PRACTICE 8
-- (Kept for compatibility)
-- ============================================

-- Pagination function
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (id INT, name VARCHAR(100), phone BIGINT)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Upsert procedure (insert or update)
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name VARCHAR, p_phone BIGINT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Bulk insert procedure
CREATE OR REPLACE PROCEDURE insert_many_users(p_names TEXT[], p_phones TEXT[])
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) >= 10 THEN
            CALL insert_or_update_user(p_names[i], p_phones[i]::BIGINT);
        ELSE
            RAISE NOTICE 'Invalid: name=%, phone=%', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Delete procedure
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_value OR CAST(phone AS TEXT) = p_value;
END;
$$ LANGUAGE plpgsql;