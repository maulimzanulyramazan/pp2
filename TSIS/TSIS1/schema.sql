-- ============================================
-- DATABASE SCHEMA FOR PHONEBOOK
-- Extended contact management
-- ============================================

-- Create groups table for contact categorization
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,              -- Auto-incrementing ID
    name VARCHAR(50) UNIQUE NOT NULL    -- Group name (Family/Work/Friend/Other)
);

-- Insert default groups into the table
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;          -- Skip if already exists

-- Add new columns to existing contacts table
ALTER TABLE contacts 
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),           -- Email address field
    ADD COLUMN IF NOT EXISTS birthday DATE,                -- Birthday date field
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id),  -- Foreign key to groups
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;  -- Auto timestamp

-- Create phones table for multiple numbers per contact
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,              -- Auto-incrementing ID
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,  -- Links to contact
    phone VARCHAR(20) NOT NULL,         -- Phone number
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))    -- Phone type
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);
CREATE INDEX IF NOT EXISTS idx_phones_contact_id ON phones(contact_id);