-- Get contacts with group name
CREATE OR REPLACE FUNCTION get_contacts_with_groups()
RETURNS TABLE (
    id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id;  -- join group info
END;
$$ LANGUAGE plpgsql;