# db.py - PostgreSQL database integration (FIXED - no transaction issues)
import psycopg2
import psycopg2.extras
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            print(f"🔌 Connecting to PostgreSQL on port {DB_CONFIG['port']}...")
            # Connect without autocommit
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = True  # Important for CREATE DATABASE
            self.cursor = self.conn.cursor()
            self.create_database()
            self.connect_to_snake_game()
            self.create_tables()
            print("✅ Database connected successfully!")
        except Exception as e:
            print(f"⚠️ Database connection failed: {e}")
            print("   Game will run in offline mode (no leaderboard saves)")
            self.conn = None
            self.cursor = None
    
    def create_database(self):
        """Create snake_game database if it doesn't exist"""
        if not self.conn:
            return
        try:
            # Check if snake_game database exists
            self.cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'snake_game'")
            if not self.cursor.fetchone():
                self.cursor.execute("CREATE DATABASE snake_game")
                print("✅ Database 'snake_game' created")
        except Exception as e:
            print(f"Database creation error: {e}")
    
    def connect_to_snake_game(self):
        """Reconnect to snake_game database"""
        if not self.conn:
            return
        try:
            # Close old connection
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            
            # Connect to snake_game database
            db_config = DB_CONFIG.copy()
            db_config["database"] = "snake_game"
            self.conn = psycopg2.connect(**db_config)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Reconnect error: {e}")
    
    def create_tables(self):
        """Create tables if they don't exist"""
        if not self.conn:
            return
        try:
            # Create players table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            
            # Create game_sessions table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                )
            """)
            print("✅ Tables created/verified")
        except Exception as e:
            print(f"Table creation error: {e}")
    
    def get_or_create_player(self, username):
        """Get existing player ID or create new player"""
        if not self.conn:
            return None
        try:
            self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                self.cursor.execute(
                    "INSERT INTO players (username) VALUES (%s) RETURNING id",
                    (username,)
                )
                player_id = self.cursor.fetchone()[0]
                return player_id
        except Exception as e:
            print(f"Player error: {e}")
            return None
    
    def save_game_result(self, username, score, level_reached):
        """Save game session to database"""
        if not self.conn:
            return
        try:
            player_id = self.get_or_create_player(username)
            if player_id:
                self.cursor.execute("""
                    INSERT INTO game_sessions (player_id, score, level_reached)
                    VALUES (%s, %s, %s)
                """, (player_id, score, level_reached))
                print(f"✅ Game saved: {username} | Score: {score} | Level: {level_reached}")
        except Exception as e:
            print(f"Save error: {e}")
    
    def get_leaderboard(self, limit=10):
        """Get top 10 all-time scores"""
        if not self.conn:
            return []
        try:
            self.cursor.execute("""
                SELECT p.username, gs.score, gs.level_reached,
                       TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI') as played_at
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                ORDER BY gs.score DESC
                LIMIT %s
            """, (limit,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Leaderboard error: {e}")
            return []
    
    def get_personal_best(self, username):
        """Get player's personal best score"""
        if not self.conn:
            return 0
        try:
            player_id = self.get_or_create_player(username)
            if player_id:
                self.cursor.execute("""
                    SELECT COALESCE(MAX(score), 0) FROM game_sessions WHERE player_id = %s
                """, (player_id,))
                result = self.cursor.fetchone()
                return result[0] if result else 0
            return 0
        except Exception as e:
            print(f"Personal best error: {e}")
            return 0
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'cursor') and self.cursor:
            try:
                self.cursor.close()
            except:
                pass
        if hasattr(self, 'conn') and self.conn:
            try:
                self.conn.close()
            except:
                pass
            print("Database connection closed")