-- 2. Procedure: insert new user, if exists then update phone
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name VARCHAR, p_phone BIGINT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


-- 3. Procedure: insert many users, validate phone, show incorrect data
CREATE OR REPLACE PROCEDURE insert_many_users(
    IN p_names TEXT[],
    IN p_phones TEXT[]
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1)
    LOOP
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) >= 10 THEN
            CALL insert_or_update_user(p_names[i], p_phones[i]::BIGINT);
        ELSE
            RAISE NOTICE 'Incorrect data: name = %, phone = %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- 5. Procedure: delete by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value
       OR CAST(phone AS TEXT) = p_value;
END;
$$ LANGUAGE plpgsql;