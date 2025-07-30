#!/usr/bin/env python3
"""
Instagram DM Automation Tool - Backend Server
Professional Instagram Direct Messaging automation with safety features
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import time
import random
import threading
import logging
from datetime import datetime, timedelta
import sqlite3
import hashlib
import os
import csv
import io
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
import requests
from urllib.parse import urlparse
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_dm_tool.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
class Config:
    DATABASE_PATH = 'instagram_dm_tool.db'
    MAX_DAILY_MESSAGES = 200
    MAX_HOURLY_MESSAGES = 50
    MIN_MESSAGE_DELAY = 30  # seconds
    MAX_MESSAGE_DELAY = 300  # seconds
    DEFAULT_ACTIVE_HOURS = {'start': '08:00', 'end': '21:00'}
    RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
    MAX_AUDIENCE_SIZE = 10000
    SESSION_TIMEOUT = 86400  # 24 hours

@dataclass
class InstagramAccount:
    id: str
    username: str
    session_data: str
    auth_method: str
    proxy_url: Optional[str] = None
    nickname: Optional[str] = None
    status: str = 'inactive'
    messages_today: int = 0
    last_activity: Optional[datetime] = None
    created_at: Optional[datetime] = None

@dataclass
class MessageTemplate:
    id: str
    name: str
    content: str
    variables: List[str]
    include_media: bool = False
    media_path: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class TargetUser:
    username: str
    full_name: Optional[str] = None
    followers_count: Optional[int] = None
    status: str = 'pending'  # pending, sent, failed, blocked
    last_contact: Optional[datetime] = None
    method: str = 'manual'  # manual, csv, followers, likers, etc.
    notes: Optional[str] = None

@dataclass
class Campaign:
    id: str
    name: str
    template_id: str
    audience_filter: str
    schedule_type: str
    status: str = 'created'  # created, active, paused, completed, cancelled
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    stats: Dict[str, int] = None

@dataclass
class MessageLog:
    id: str
    campaign_id: Optional[str]
    username: str
    template_id: str
    status: str  # sent, failed, pending
    message_content: str
    error_message: Optional[str] = None
    timestamp: Optional[datetime] = None

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Accounts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    session_data TEXT NOT NULL,
                    auth_method TEXT NOT NULL,
                    proxy_url TEXT,
                    nickname TEXT,
                    status TEXT DEFAULT 'inactive',
                    messages_today INTEGER DEFAULT 0,
                    last_activity TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Templates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS templates (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    variables TEXT,
                    include_media BOOLEAN DEFAULT FALSE,
                    media_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Target users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS target_users (
                    username TEXT PRIMARY KEY,
                    full_name TEXT,
                    followers_count INTEGER,
                    status TEXT DEFAULT 'pending',
                    last_contact TIMESTAMP,
                    method TEXT DEFAULT 'manual',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Campaigns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    template_id TEXT NOT NULL,
                    audience_filter TEXT,
                    schedule_type TEXT,
                    status TEXT DEFAULT 'created',
                    stats TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (template_id) REFERENCES templates (id)
                )
            ''')
            
            # Message logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS message_logs (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT,
                    username TEXT NOT NULL,
                    template_id TEXT,
                    status TEXT NOT NULL,
                    message_content TEXT,
                    error_message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns (id),
                    FOREIGN KEY (template_id) REFERENCES templates (id)
                )
            ''')
            
            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Auto reply rules table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auto_reply_rules (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    keywords TEXT NOT NULL,
                    reply_message TEXT NOT NULL,
                    delay_minutes INTEGER DEFAULT 5,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a query and return results as list of dictionaries"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update/insert query and return affected rows"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

class InstagramAPI:
    """Mock Instagram API for demonstration purposes"""
    
    def __init__(self):
        self.authenticated_accounts = {}
        self.rate_limits = {}
    
    def authenticate(self, username: str, session_data: str, auth_method: str, proxy_url: str = None) -> Dict[str, Any]:
        """Simulate Instagram authentication"""
        try:
            # In a real implementation, this would validate the session/token
            # For demo purposes, we'll simulate successful authentication
            
            if not username or not session_data:
                return {'success': False, 'error': 'Missing credentials'}
            
            # Simulate authentication delay
            time.sleep(1)
            
            # Store authenticated session
            self.authenticated_accounts[username] = {
                'session_data': session_data,
                'auth_method': auth_method,
                'proxy_url': proxy_url,
                'authenticated_at': datetime.now(),
                'last_activity': datetime.now()
            }
            
            logger.info(f"Successfully authenticated Instagram account: {username}")
            return {
                'success': True,
                'username': username,
                'followers_count': random.randint(100, 10000),
                'following_count': random.randint(50, 1000)
            }
            
        except Exception as e:
            logger.error(f"Authentication failed for {username}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def send_direct_message(self, sender_username: str, recipient_username: str, message: str) -> Dict[str, Any]:
        """Simulate sending a direct message"""
        try:
            # Check if sender is authenticated
            if sender_username not in self.authenticated_accounts:
                return {'success': False, 'error': 'Account not authenticated'}
            
            # Check rate limits
            if not self._check_rate_limit(sender_username):
                return {'success': False, 'error': 'Rate limit exceeded'}
            
            # Simulate message sending delay
            delay = random.randint(Config.MIN_MESSAGE_DELAY, Config.MAX_MESSAGE_DELAY)
            time.sleep(delay / 10)  # Reduced for demo
            
            # Simulate success/failure (90% success rate)
            success = random.random() > 0.1
            
            if success:
                self._update_rate_limit(sender_username)
                logger.info(f"Message sent from {sender_username} to {recipient_username}")
                return {
                    'success': True,
                    'message_id': f"msg_{int(time.time())}_{random.randint(1000, 9999)}",
                    'timestamp': datetime.now().isoformat()
                }
            else:
                error_messages = [
                    'User not found',
                    'Message blocked by recipient',
                    'Temporary network error',
                    'Account restrictions'
                ]
                error = random.choice(error_messages)
                logger.warning(f"Failed to send message from {sender_username} to {recipient_username}: {error}")
                return {'success': False, 'error': error}
                
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_followers(self, username: str, limit: int = 100) -> Dict[str, Any]:
        """Simulate getting followers list"""
        try:
            if username not in self.authenticated_accounts:
                return {'success': False, 'error': 'Account not authenticated'}
            
            # Simulate API delay
            time.sleep(2)
            
            # Generate mock followers
            followers = []
            for i in range(min(limit, 50)):  # Limit for demo
                followers.append({
                    'username': f'user_{random.randint(100, 9999)}',
                    'full_name': f'User {i+1}',
                    'followers_count': random.randint(10, 5000),
                    'following_count': random.randint(10, 1000)
                })
            
            return {'success': True, 'followers': followers, 'count': len(followers)}
            
        except Exception as e:
            logger.error(f"Error getting followers: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_post_likers(self, post_url: str, limit: int = 100) -> Dict[str, Any]:
        """Simulate getting post likers"""
        try:
            # Extract post ID from URL (simplified)
            if 'instagram.com/p/' not in post_url:
                return {'success': False, 'error': 'Invalid post URL'}
            
            time.sleep(2)
            
            # Generate mock likers
            likers = []
            for i in range(min(limit, 30)):  # Limit for demo
                likers.append({
                    'username': f'liker_{random.randint(100, 9999)}',
                    'full_name': f'Liker {i+1}',
                    'followers_count': random.randint(10, 5000)
                })
            
            return {'success': True, 'likers': likers, 'count': len(likers)}
            
        except Exception as e:
            logger.error(f"Error getting post likers: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _check_rate_limit(self, username: str) -> bool:
        """Check if user has exceeded rate limits"""
        now = datetime.now()
        if username not in self.rate_limits:
            self.rate_limits[username] = {'hourly': [], 'daily': []}
        
        # Clean old entries
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        self.rate_limits[username]['hourly'] = [
            t for t in self.rate_limits[username]['hourly'] if t > hour_ago
        ]
        self.rate_limits[username]['daily'] = [
            t for t in self.rate_limits[username]['daily'] if t > day_ago
        ]
        
        # Check limits
        hourly_count = len(self.rate_limits[username]['hourly'])
        daily_count = len(self.rate_limits[username]['daily'])
        
        return hourly_count < Config.MAX_HOURLY_MESSAGES and daily_count < Config.MAX_DAILY_MESSAGES
    
    def _update_rate_limit(self, username: str):
        """Update rate limit counters"""
        now = datetime.now()
        if username not in self.rate_limits:
            self.rate_limits[username] = {'hourly': [], 'daily': []}
        
        self.rate_limits[username]['hourly'].append(now)
        self.rate_limits[username]['daily'].append(now)

class CampaignManager:
    def __init__(self, db_manager: DatabaseManager, instagram_api: InstagramAPI):
        self.db = db_manager
        self.instagram_api = instagram_api
        self.active_campaigns = {}
        self.campaign_threads = {}
    
    def start_campaign(self, campaign_id: str, account_username: str) -> Dict[str, Any]:
        """Start a campaign"""
        try:
            # Get campaign details
            campaigns = self.db.execute_query(
                "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
            )
            if not campaigns:
                return {'success': False, 'error': 'Campaign not found'}
            
            campaign = campaigns[0]
            
            # Get template
            templates = self.db.execute_query(
                "SELECT * FROM templates WHERE id = ?", (campaign['template_id'],)
            )
            if not templates:
                return {'success': False, 'error': 'Template not found'}
            
            template = templates[0]
            
            # Get target audience
            audience_query = "SELECT * FROM target_users WHERE status = 'pending'"
            if campaign['audience_filter'] and campaign['audience_filter'] != 'all':
                # Add specific filters based on audience_filter
                pass
            
            target_users = self.db.execute_query(audience_query)
            
            if not target_users:
                return {'success': False, 'error': 'No target users found'}
            
            # Update campaign status
            self.db.execute_update(
                "UPDATE campaigns SET status = 'active', started_at = CURRENT_TIMESTAMP WHERE id = ?",
                (campaign_id,)
            )
            
            # Start campaign thread
            campaign_thread = threading.Thread(
                target=self._execute_campaign,
                args=(campaign_id, account_username, template, target_users)
            )
            campaign_thread.daemon = True
            campaign_thread.start()
            
            self.campaign_threads[campaign_id] = campaign_thread
            self.active_campaigns[campaign_id] = {
                'status': 'active',
                'started_at': datetime.now(),
                'total_users': len(target_users),
                'sent': 0,
                'failed': 0
            }
            
            logger.info(f"Started campaign {campaign_id} with {len(target_users)} target users")
            return {'success': True, 'message': f'Campaign started with {len(target_users)} users'}
            
        except Exception as e:
            logger.error(f"Error starting campaign {campaign_id}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _execute_campaign(self, campaign_id: str, account_username: str, template: Dict, target_users: List[Dict]):
        """Execute campaign in background thread"""
        try:
            for user in target_users:
                # Check if campaign is still active
                if campaign_id not in self.active_campaigns:
                    break
                
                if self.active_campaigns[campaign_id]['status'] != 'active':
                    break
                
                # Personalize message
                message_content = self._personalize_message(template['content'], user)
                
                # Send message
                result = self.instagram_api.send_direct_message(
                    account_username, user['username'], message_content
                )
                
                # Log result
                log_id = f"log_{int(time.time())}_{random.randint(1000, 9999)}"
                status = 'sent' if result['success'] else 'failed'
                error_message = result.get('error') if not result['success'] else None
                
                self.db.execute_update(
                    """INSERT INTO message_logs (id, campaign_id, username, template_id, status, 
                       message_content, error_message) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (log_id, campaign_id, user['username'], template['id'], 
                     status, message_content, error_message)
                )
                
                # Update user status
                user_status = 'sent' if result['success'] else 'failed'
                self.db.execute_update(
                    "UPDATE target_users SET status = ?, last_contact = CURRENT_TIMESTAMP WHERE username = ?",
                    (user_status, user['username'])
                )
                
                # Update campaign stats
                if result['success']:
                    self.active_campaigns[campaign_id]['sent'] += 1
                else:
                    self.active_campaigns[campaign_id]['failed'] += 1
                
                # Random delay between messages
                delay = random.randint(Config.MIN_MESSAGE_DELAY, Config.MAX_MESSAGE_DELAY)
                time.sleep(delay / 10)  # Reduced for demo
            
            # Mark campaign as completed
            self.db.execute_update(
                "UPDATE campaigns SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                (campaign_id,)
            )
            
            if campaign_id in self.active_campaigns:
                self.active_campaigns[campaign_id]['status'] = 'completed'
            
            logger.info(f"Campaign {campaign_id} completed")
            
        except Exception as e:
            logger.error(f"Error executing campaign {campaign_id}: {str(e)}")
            # Mark campaign as failed
            self.db.execute_update(
                "UPDATE campaigns SET status = 'failed' WHERE id = ?",
                (campaign_id,)
            )
    
    def _personalize_message(self, template: str, user: Dict) -> str:
        """Personalize message template with user data"""
        message = template
        message = message.replace('{{username}}', user['username'])
        message = message.replace('{{fullname}}', user.get('full_name', user['username']))
        message = message.replace('{{followers}}', str(user.get('followers_count', 0)))
        message = message.replace('{{date}}', datetime.now().strftime('%Y-%m-%d'))
        message = message.replace('{{time}}', datetime.now().strftime('%H:%M'))
        return message
    
    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign"""
        if campaign_id in self.active_campaigns:
            self.active_campaigns[campaign_id]['status'] = 'paused'
            self.db.execute_update(
                "UPDATE campaigns SET status = 'paused' WHERE id = ?",
                (campaign_id,)
            )
            return {'success': True, 'message': 'Campaign paused'}
        return {'success': False, 'error': 'Campaign not found or not active'}
    
    def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign statistics"""
        if campaign_id in self.active_campaigns:
            return self.active_campaigns[campaign_id]
        
        # Get from database for completed campaigns
        campaigns = self.db.execute_query(
            "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
        )
        if campaigns:
            campaign = campaigns[0]
            logs = self.db.execute_query(
                "SELECT status, COUNT(*) as count FROM message_logs WHERE campaign_id = ? GROUP BY status",
                (campaign_id,)
            )
            stats = {log['status']: log['count'] for log in logs}
            return {
                'status': campaign['status'],
                'sent': stats.get('sent', 0),
                'failed': stats.get('failed', 0),
                'pending': stats.get('pending', 0)
            }
        
        return {'success': False, 'error': 'Campaign not found'}

# Initialize components
db_manager = DatabaseManager(Config.DATABASE_PATH)
instagram_api = InstagramAPI()
campaign_manager = CampaignManager(db_manager, instagram_api)

# API Routes
@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory('.', 'instagram-dm-tool.html')

@app.route('/api/auth/connect', methods=['POST'])
def connect_instagram():
    """Connect to Instagram account"""
    try:
        data = request.get_json()
        username = data.get('username')
        session_data = data.get('session_data')
        auth_method = data.get('auth_method', 'session')
        proxy_url = data.get('proxy_url')
        
        if not username or not session_data:
            return jsonify({'success': False, 'error': 'Missing credentials'}), 400
        
        # Authenticate with Instagram
        result = instagram_api.authenticate(username, session_data, auth_method, proxy_url)
        
        if result['success']:
            # Save account to database
            account_id = f"acc_{int(time.time())}_{random.randint(1000, 9999)}"
            db_manager.execute_update(
                """INSERT OR REPLACE INTO accounts (id, username, session_data, auth_method, 
                   proxy_url, status, last_activity) VALUES (?, ?, ?, ?, ?, 'active', CURRENT_TIMESTAMP)""",
                (account_id, username, session_data, auth_method, proxy_url)
            )
            
            return jsonify({
                'success': True,
                'account_id': account_id,
                'username': username,
                'followers_count': result.get('followers_count', 0)
            })
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error connecting to Instagram: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/test', methods=['POST'])
def test_connection():
    """Test Instagram connection"""
    try:
        data = request.get_json()
        username = data.get('username')
        
        if username in instagram_api.authenticated_accounts:
            return jsonify({'success': True, 'message': 'Connection is active'})
        else:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 400
            
    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/audience/add', methods=['POST'])
def add_audience():
    """Add users to target audience"""
    try:
        data = request.get_json()
        method = data.get('method', 'manual')
        users = []
        
        if method == 'manual':
            usernames = data.get('usernames', [])
            users = [{'username': username.strip(), 'method': 'manual'} for username in usernames if username.strip()]
        
        elif method == 'csv':
            csv_data = data.get('csv_data', '')
            csv_reader = csv.DictReader(io.StringIO(csv_data))
            for row in csv_reader:
                if 'username' in row and row['username']:
                    users.append({
                        'username': row['username'].strip(),
                        'full_name': row.get('full_name', ''),
                        'followers_count': int(row.get('followers_count', 0)) if row.get('followers_count') else None,
                        'method': 'csv'
                    })
        
        elif method in ['followers', 'likers', 'commenters']:
            account_username = data.get('account_username')
            limit = data.get('limit', 100)
            post_url = data.get('post_url') if method in ['likers', 'commenters'] else None
            
            if method == 'followers':
                result = instagram_api.get_followers(account_username, limit)
                if result['success']:
                    users = [{'username': user['username'], 'full_name': user['full_name'], 
                             'followers_count': user['followers_count'], 'method': 'followers'} 
                            for user in result['followers']]
            
            elif method == 'likers' and post_url:
                result = instagram_api.get_post_likers(post_url, limit)
                if result['success']:
                    users = [{'username': user['username'], 'full_name': user['full_name'],
                             'followers_count': user['followers_count'], 'method': 'likers'}
                            for user in result['likers']]
        
        # Insert users into database
        added_count = 0
        for user in users:
            try:
                db_manager.execute_update(
                    """INSERT OR REPLACE INTO target_users (username, full_name, followers_count, 
                       method, status) VALUES (?, ?, ?, ?, 'pending')""",
                    (user['username'], user.get('full_name'), user.get('followers_count'), user['method'])
                )
                added_count += 1
            except Exception as e:
                logger.warning(f"Failed to add user {user['username']}: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': f'Added {added_count} users to audience',
            'count': added_count
        })
        
    except Exception as e:
        logger.error(f"Error adding audience: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/audience/list', methods=['GET'])
def list_audience():
    """Get target audience list"""
    try:
        users = db_manager.execute_query("SELECT * FROM target_users ORDER BY created_at DESC")
        return jsonify({'success': True, 'users': users, 'count': len(users)})
    except Exception as e:
        logger.error(f"Error listing audience: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/audience/remove', methods=['DELETE'])
def remove_audience():
    """Remove user from audience"""
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({'success': False, 'error': 'Username required'}), 400
        
        rows_affected = db_manager.execute_update(
            "DELETE FROM target_users WHERE username = ?", (username,)
        )
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': 'User removed from audience'})
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
    except Exception as e:
        logger.error(f"Error removing user from audience: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/templates/create', methods=['POST'])
def create_template():
    """Create message template"""
    try:
        data = request.get_json()
        name = data.get('name')
        content = data.get('content')
        include_media = data.get('include_media', False)
        
        if not name or not content:
            return jsonify({'success': False, 'error': 'Name and content required'}), 400
        
        # Extract variables from template
        variables = re.findall(r'\{\{(\w+)\}\}', content)
        
        template_id = f"tpl_{int(time.time())}_{random.randint(1000, 9999)}"
        db_manager.execute_update(
            """INSERT INTO templates (id, name, content, variables, include_media) 
               VALUES (?, ?, ?, ?, ?)""",
            (template_id, name, content, json.dumps(variables), include_media)
        )
        
        return jsonify({
            'success': True,
            'template_id': template_id,
            'message': 'Template created successfully'
        })
        
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/templates/list', methods=['GET'])
def list_templates():
    """Get all message templates"""
    try:
        templates = db_manager.execute_query("SELECT * FROM templates ORDER BY created_at DESC")
        return jsonify({'success': True, 'templates': templates})
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/templates/delete/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete message template"""
    try:
        rows_affected = db_manager.execute_update(
            "DELETE FROM templates WHERE id = ?", (template_id,)
        )
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': 'Template deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Template not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting template: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/create', methods=['POST'])
def create_campaign():
    """Create new campaign"""
    try:
        data = request.get_json()
        name = data.get('name')
        template_id = data.get('template_id')
        audience_filter = data.get('audience_filter', 'all')
        schedule_type = data.get('schedule_type', 'immediate')
        
        if not name or not template_id:
            return jsonify({'success': False, 'error': 'Name and template required'}), 400
        
        campaign_id = f"camp_{int(time.time())}_{random.randint(1000, 9999)}"
        stats = json.dumps({'sent': 0, 'failed': 0, 'pending': 0})
        
        db_manager.execute_update(
            """INSERT INTO campaigns (id, name, template_id, audience_filter, schedule_type, stats) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (campaign_id, name, template_id, audience_filter, schedule_type, stats)
        )
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Campaign created successfully'
        })
        
    except Exception as e:
        logger.error(f"Error creating campaign: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/list', methods=['GET'])
def list_campaigns():
    """Get all campaigns"""
    try:
        campaigns = db_manager.execute_query("SELECT * FROM campaigns ORDER BY created_at DESC")
        return jsonify({'success': True, 'campaigns': campaigns})
    except Exception as e:
        logger.error(f"Error listing campaigns: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/start/<campaign_id>', methods=['POST'])
def start_campaign(campaign_id):
    """Start campaign"""
    try:
        data = request.get_json()
        account_username = data.get('account_username')
        
        if not account_username:
            return jsonify({'success': False, 'error': 'Account username required'}), 400
        
        result = campaign_manager.start_campaign(campaign_id, account_username)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error starting campaign: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/pause/<campaign_id>', methods=['POST'])
def pause_campaign(campaign_id):
    """Pause campaign"""
    try:
        result = campaign_manager.pause_campaign(campaign_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error pausing campaign: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/stats/<campaign_id>', methods=['GET'])
def get_campaign_stats(campaign_id):
    """Get campaign statistics"""
    try:
        stats = campaign_manager.get_campaign_stats(campaign_id)
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        logger.error(f"Error getting campaign stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logs/list', methods=['GET'])
def list_logs():
    """Get message logs"""
    try:
        logs = db_manager.execute_query(
            "SELECT * FROM message_logs ORDER BY timestamp DESC LIMIT 100"
        )
        return jsonify({'success': True, 'logs': logs})
    except Exception as e:
        logger.error(f"Error listing logs: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get dashboard analytics"""
    try:
        # Get today's stats
        today = datetime.now().strftime('%Y-%m-%d')
        
        stats = {
            'messages_sent_today': 0,
            'success_rate': 0,
            'pending_messages': 0,
            'failed_messages': 0,
            'total_audience': 0,
            'active_campaigns': 0
        }
        
        # Messages sent today
        sent_today = db_manager.execute_query(
            "SELECT COUNT(*) as count FROM message_logs WHERE status = 'sent' AND DATE(timestamp) = ?",
            (today,)
        )
        stats['messages_sent_today'] = sent_today[0]['count'] if sent_today else 0
        
        # Success rate
        total_messages = db_manager.execute_query(
            "SELECT COUNT(*) as count FROM message_logs WHERE DATE(timestamp) = ?",
            (today,)
        )
        if total_messages and total_messages[0]['count'] > 0:
            stats['success_rate'] = round((stats['messages_sent_today'] / total_messages[0]['count']) * 100)
        
        # Pending messages
        pending = db_manager.execute_query(
            "SELECT COUNT(*) as count FROM target_users WHERE status = 'pending'"
        )
        stats['pending_messages'] = pending[0]['count'] if pending else 0
        
        # Failed messages today
        failed_today = db_manager.execute_query(
            "SELECT COUNT(*) as count FROM message_logs WHERE status = 'failed' AND DATE(timestamp) = ?",
            (today,)
        )
        stats['failed_messages'] = failed_today[0]['count'] if failed_today else 0
        
        # Total audience
        audience = db_manager.execute_query("SELECT COUNT(*) as count FROM target_users")
        stats['total_audience'] = audience[0]['count'] if audience else 0
        
        # Active campaigns
        active = db_manager.execute_query(
            "SELECT COUNT(*) as count FROM campaigns WHERE status = 'active'"
        )
        stats['active_campaigns'] = active[0]['count'] if active else 0
        
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        logger.error(f"Error getting dashboard analytics: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/settings/save', methods=['POST'])
def save_settings():
    """Save application settings"""
    try:
        data = request.get_json()
        
        for key, value in data.items():
            db_manager.execute_update(
                "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (key, json.dumps(value))
            )
        
        return jsonify({'success': True, 'message': 'Settings saved successfully'})
        
    except Exception as e:
        logger.error(f"Error saving settings: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/settings/load', methods=['GET'])
def load_settings():
    """Load application settings"""
    try:
        settings = db_manager.execute_query("SELECT key, value FROM settings")
        settings_dict = {setting['key']: json.loads(setting['value']) for setting in settings}
        return jsonify({'success': True, 'settings': settings_dict})
    except Exception as e:
        logger.error(f"Error loading settings: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/logs', methods=['GET'])
def export_logs():
    """Export logs as CSV"""
    try:
        logs = db_manager.execute_query("SELECT * FROM message_logs ORDER BY timestamp DESC")
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Timestamp', 'Username', 'Status', 'Message Content', 'Error Message'])
        
        # Write data
        for log in logs:
            writer.writerow([
                log['timestamp'],
                log['username'],
                log['status'],
                log['message_content'],
                log['error_message'] or ''
            ])
        
        csv_data = output.getvalue()
        output.close()
        
        return jsonify({'success': True, 'csv_data': csv_data})
        
    except Exception as e:
        logger.error(f"Error exporting logs: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Instagram DM Automation Tool Server")
    app.run(host='0.0.0.0', port=5000, debug=True)