"""
RIJWAL_LANG Plugin Marketplace - Database Layer
Version: v0.19 Marketplace Phase 1
Database operations for plugins, ratings, creators, revenue tracking
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path


class MarketplaceDB:
    """Database management for plugin marketplace"""
    
    def __init__(self, db_path="marketplace.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize marketplace database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Plugins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plugins (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                author_id TEXT NOT NULL,
                description TEXT,
                code TEXT NOT NULL,
                version TEXT DEFAULT "1.0.0",
                category TEXT,
                tags TEXT,
                rating REAL DEFAULT 0.0,
                downloads INTEGER DEFAULT 0,
                revenue_total REAL DEFAULT 0.0,
                verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                plugin_id TEXT NOT NULL,
                author_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                helpful INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plugin_id) REFERENCES plugins (id)
            )
        ''')
        
        # Creators table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS creators (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                bio TEXT,
                avatar_url TEXT,
                total_revenue REAL DEFAULT 0.0,
                plugins_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Installations table (for tracking user installs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS installations (
                id TEXT PRIMARY KEY,
                plugin_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plugin_id) REFERENCES plugins (id)
            )
        ''')
        
        # Revenue tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue (
                id TEXT PRIMARY KEY,
                plugin_id TEXT NOT NULL,
                creator_id TEXT NOT NULL,
                amount REAL NOT NULL,
                platform_fee REAL NOT NULL,
                creator_payout REAL NOT NULL,
                transaction_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plugin_id) REFERENCES plugins (id),
                FOREIGN KEY (creator_id) REFERENCES creators (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ============ PLUGIN OPERATIONS ============
    
    def create_plugin(self, name, author_id, code, description="", category="", tags=None):
        """Create new plugin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        plugin_id = str(uuid.uuid4())
        tags = json.dumps(tags or [])
        
        try:
            cursor.execute('''
                INSERT INTO plugins 
                (id, name, author_id, code, description, category, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (plugin_id, name, author_id, code, description, category, tags))
            conn.commit()
            return plugin_id
        except sqlite3.IntegrityError:
            return None  # Plugin name already exists
        finally:
            conn.close()
    
    def get_plugin(self, plugin_id):
        """Get plugin details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plugins WHERE id = ?', (plugin_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_plugin(row)
        return None
    
    def get_plugin_by_name(self, name):
        """Get plugin by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plugins WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_plugin(row)
        return None
    
    def search_plugins(self, query="", category="", tags=None, limit=50):
        """Search plugins by name, description, category, tags"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = 'SELECT * FROM plugins WHERE 1=1'
        params = []
        
        if query:
            sql += ' AND (name LIKE ? OR description LIKE ?)'
            search_term = f'%{query}%'
            params.extend([search_term, search_term])
        
        if category:
            sql += ' AND category = ?'
            params.append(category)
        
        sql += ' ORDER BY downloads DESC, rating DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_plugin(row) for row in rows]
    
    def get_trending_plugins(self, limit=10):
        """Get trending plugins (top downloads + ratings)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM plugins 
            ORDER BY downloads DESC, rating DESC 
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_plugin(row) for row in rows]
    
    def get_creator_plugins(self, author_id):
        """Get all plugins by creator"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plugins WHERE author_id = ? ORDER BY created_at DESC', 
                      (author_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_plugin(row) for row in rows]
    
    def increment_downloads(self, plugin_id):
        """Increment plugin download count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE plugins 
            SET downloads = downloads + 1, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (plugin_id,))
        conn.commit()
        conn.close()
    
    def update_plugin_rating(self, plugin_id):
        """Recalculate plugin rating from reviews"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT AVG(rating) FROM reviews WHERE plugin_id = ?
        ''', (plugin_id,))
        result = cursor.fetchone()
        avg_rating = result[0] if result[0] else 0.0
        
        cursor.execute('''
            UPDATE plugins 
            SET rating = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (avg_rating, plugin_id))
        conn.commit()
        conn.close()
    
    def verify_plugin(self, plugin_id):
        """Mark plugin as verified"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE plugins 
            SET verified = 1, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (plugin_id,))
        conn.commit()
        conn.close()
    
    # ============ REVIEW OPERATIONS ============
    
    def add_review(self, plugin_id, author_id, rating, comment=""):
        """Add review for plugin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        review_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO reviews (id, plugin_id, author_id, rating, comment)
            VALUES (?, ?, ?, ?, ?)
        ''', (review_id, plugin_id, author_id, rating, comment))
        conn.commit()
        
        # Update plugin rating
        self.update_plugin_rating(plugin_id)
        
        conn.close()
        return review_id
    
    def get_plugin_reviews(self, plugin_id):
        """Get all reviews for plugin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reviews 
            WHERE plugin_id = ? 
            ORDER BY created_at DESC
        ''', (plugin_id,))
        rows = cursor.fetchall()
        conn.close()
        
        reviews = []
        for row in rows:
            reviews.append({
                'id': row[0],
                'plugin_id': row[1],
                'author_id': row[2],
                'rating': row[3],
                'comment': row[4],
                'helpful': row[5],
                'created_at': row[6]
            })
        return reviews
    
    # ============ CREATOR OPERATIONS ============
    
    def create_creator(self, username, email="", bio=""):
        """Create creator account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        creator_id = str(uuid.uuid4())
        
        try:
            cursor.execute('''
                INSERT INTO creators (id, username, email, bio)
                VALUES (?, ?, ?, ?)
            ''', (creator_id, username, email, bio))
            conn.commit()
            return creator_id
        except sqlite3.IntegrityError:
            return None  # Username already exists
        finally:
            conn.close()
    
    def get_creator(self, creator_id):
        """Get creator info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM creators WHERE id = ?', (creator_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'bio': row[3],
                'avatar_url': row[4],
                'total_revenue': row[5],
                'plugins_count': row[6],
                'created_at': row[7]
            }
        return None
    
    def update_creator_revenue(self, creator_id, amount):
        """Update creator total revenue"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE creators 
            SET total_revenue = total_revenue + ?, plugins_count = plugins_count + 1
            WHERE id = ?
        ''', (amount, creator_id))
        conn.commit()
        conn.close()
    
    # ============ INSTALLATION OPERATIONS ============
    
    def record_installation(self, plugin_id, user_id):
        """Record user installation of plugin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        install_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO installations (id, plugin_id, user_id)
            VALUES (?, ?, ?)
        ''', (install_id, plugin_id, user_id))
        conn.commit()
        conn.close()
        
        # Increment download count
        self.increment_downloads(plugin_id)
        return install_id
    
    def get_user_installations(self, user_id):
        """Get all plugins installed by user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT plugin_id FROM installations 
            WHERE user_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]
    
    # ============ REVENUE OPERATIONS ============
    
    def record_revenue(self, plugin_id, creator_id, amount, transaction_type="sale"):
        """Record revenue transaction (70/30 split)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        revenue_id = str(uuid.uuid4())
        platform_fee = amount * 0.30  # Platform gets 30%
        creator_payout = amount * 0.70  # Creator gets 70%
        
        cursor.execute('''
            INSERT INTO revenue 
            (id, plugin_id, creator_id, amount, platform_fee, creator_payout, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (revenue_id, plugin_id, creator_id, amount, platform_fee, creator_payout, transaction_type))
        conn.commit()
        
        # Update plugin revenue total
        cursor.execute('''
            UPDATE plugins 
            SET revenue_total = revenue_total + ? 
            WHERE id = ?
        ''', (amount, plugin_id))
        conn.commit()
        
        # Update creator revenue
        self.update_creator_revenue(creator_id, creator_payout)
        
        conn.close()
        return revenue_id
    
    def get_creator_revenue(self, creator_id):
        """Get creator total revenue"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(creator_payout) FROM revenue WHERE creator_id = ?
        ''', (creator_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0.0
    
    def get_platform_revenue(self):
        """Get platform total revenue (30% from all sales)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(platform_fee) FROM revenue')
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0.0
    
    # ============ UTILITY ============
    
    def _row_to_plugin(self, row):
        """Convert database row to plugin dict"""
        return {
            'id': row[0],
            'name': row[1],
            'author_id': row[2],
            'description': row[3],
            'code': row[4],
            'version': row[5],
            'category': row[6],
            'tags': json.loads(row[7]) if row[7] else [],
            'rating': row[8],
            'downloads': row[9],
            'revenue_total': row[10],
            'verified': row[11],
            'created_at': row[12],
            'updated_at': row[13]
        }
    
    def clear_all(self):
        """Clear all data (for testing)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM revenue')
        cursor.execute('DELETE FROM installations')
        cursor.execute('DELETE FROM reviews')
        cursor.execute('DELETE FROM plugins')
        cursor.execute('DELETE FROM creators')
        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Test database
    db = MarketplaceDB()
    
    # Create test creator
    creator_id = db.create_creator("alice", "alice@example.com", "Plugin creator")
    print(f"✅ Created creator: {creator_id}")
    
    # Create test plugin
    plugin_id = db.create_plugin(
        "Django Helper",
        creator_id,
        "console.log('Hello from plugin')",
        "AI-powered Django ORM suggestions",
        "AI Assistant",
        ["django", "orm", "ai"]
    )
    print(f"✅ Created plugin: {plugin_id}")
    
    # Get plugin
    plugin = db.get_plugin(plugin_id)
    print(f"✅ Plugin: {plugin['name']} - {plugin['description']}")
    
    # Add review
    db.add_review(plugin_id, "user123", 5, "Amazing plugin!")
    reviews = db.get_plugin_reviews(plugin_id)
    print(f"✅ Reviews: {len(reviews)}")
    
    # Record installation
    db.record_installation(plugin_id, "user123")
    print(f"✅ Installation recorded")
    
    # Record revenue
    db.record_revenue(plugin_id, creator_id, 10.0, "sale")
    creator_revenue = db.get_creator_revenue(creator_id)
    print(f"✅ Creator revenue: ${creator_revenue}")
