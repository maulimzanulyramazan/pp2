# PhoneBook Application - Extended Contact Management

## 📋 Overview

A comprehensive phonebook management system built with **Python** and **PostgreSQL**. This application extends basic CRUD operations with advanced features like multiple phone numbers per contact, group categorization, JSON/CSV import/export, and interactive console navigation.

## 🎯 Features

### Core Features (Practice 7-8 Base)
- ✅ CRUD operations via psycopg2
- ✅ CSV import and console-based data entry
- ✅ Query by name / phone prefix, update, delete
- ✅ Pattern-search function (name / phone)
- ✅ Upsert procedure with validation
- ✅ Paginated query function (LIMIT / OFFSET)
- ✅ Delete procedure by username or phone

### New Extended Features

#### 1. Enhanced Data Model
- **Multiple phone numbers** per contact (home, work, mobile types)
- **Email field** for each contact
- **Birthday field** (DATE type)
- **Contact groups** (Family, Work, Friend, Other)
- Automatic timestamp for creation date

#### 2. Advanced Console Interface
- **Filter by group** - View contacts from specific categories
- **Email search** - Partial match search (e.g., 'gmail' finds all Gmail contacts)
- **Sorting options** - Sort by name, birthday, or date added
- **Interactive pagination** - Navigate through contacts with next/prev/quit commands

#### 3. Import / Export Capabilities
- **Export to JSON** - Save all contacts (including phones and groups) to a `.json` file
- **Import from JSON** - Load contacts with duplicate handling (skip/overwrite)
- **Extended CSV import** - Support for new fields (email, birthday, group, phone type)

#### 4. Server-Side Logic (PL/pgSQL)
- `add_phone()` - Add new phone number to existing contact
- `move_to_group()` - Move contact to a group (auto-creates groups)
- `search_contacts()` - Enhanced search across name, email, phones, and groups

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.x |
| Database | PostgreSQL |
| Adapter | psycopg2 |
| Data Formats | JSON, CSV |

## 📁 Project Structure
