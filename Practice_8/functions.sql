-- 1. Function: search by pattern
CREATE OR REPLACE FUNCTION search_contacts(pattern_text TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    phone BIGINT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.phone
    FROM contacts c
    WHERE c.name ILIKE '%' || pattern_text || '%'
       OR CAST(c.phone AS TEXT) LIKE '%' || pattern_text || '%'
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


-- 4. Function: pagination with LIMIT and OFFSET
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    phone BIGINT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;