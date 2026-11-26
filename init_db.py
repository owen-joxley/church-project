import sqlite3

def init_db():
    conn = sqlite3.connect('church.db')
    cursor = conn.cursor()

    # Members Table (Supports OAuth / Google / Facebook / Direct Signups)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        auth_provider TEXT DEFAULT 'local', -- 'google', 'facebook', or 'local'
        profile_pic TEXT,
        primary_group TEXT,
        date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Ministries & Groups Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL, -- e.g., 'Ministry', 'Children', 'Development', 'Choir'
        parent_group_id INTEGER, -- For sub-groups (e.g. Pathfinders under Children)
        description TEXT,
        leader_name TEXT
    )
    ''')

    # Church Construction & Development Updates
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS development_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL, -- 'Construction', 'Fundraising', 'Donation'
        target_amount REAL DEFAULT 0,
        raised_amount REAL DEFAULT 0,
        description TEXT,
        date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Seed Default Church Groups & Sub-Groups
    groups_data = [
        # Executive & Governance
        ('Pastors & Elders', 'Governance', None, 'Spiritual leadership and oversight'),
        ('Church Board', 'Governance', None, 'Executive planning and decision making'),
        
        # Ministries
        ('Adventist Men Ministry (AMM)', 'Ministry', None, 'Men empowering men in faith and service'),
        ('Adventist Women Ministry (AWM)', 'Ministry', None, 'Nurturing women in spiritual growth'),
        ('Youth Ministry', 'Ministry', None, 'Youth fellowship and training'),
        ('Young Adults', 'Ministry', 5, 'Sub-group under Youth Ministry'),
        ('Ambassadors', 'Ministry', 5, 'Sub-group under Youth Ministry'),
        
        # Children Ministry & Sub-groups
        ('Children Ministry', 'Children', None, 'Guiding children in Christ'),
        ('Pathfinders', 'Children', 8, 'Sub-group for ages 10-15'),
        ('Adventurers', 'Children', 8, 'Sub-group for ages 6-9'),
        ('Eager Beavers', 'Children', 8, 'Sub-group for ages 4-5'),

        # Music Ministries
        ('Church Choir', 'Music', None, 'Main church sanctuary choir'),
        ('Youth Choir', 'Music', None, 'Youth singing ministry'),
        ('Children Choir', 'Music', None, 'Little lights choir'),

        # Development Sub-groups
        ('Church Construction', 'Development', None, 'Handling all physical construction projects'),
        ('Fundraising', 'Development', None, 'Planning and executing church fundraisers'),
        ('Donations & Pledges', 'Development', None, 'Tracking donations and project pledges')
    ]

    cursor.executemany('''
    INSERT INTO groups (name, category, parent_group_id, description)
    SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM groups WHERE name = ?)
    ''', [(g[0], g[1], g[2], g[3], g[0]) for g in groups_data])

    conn.commit()
    conn.close()
    print("Database schema updated successfully!")

if __name__ == '__main__':
    init_db()