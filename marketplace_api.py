"""
RIJWAL_LANG Plugin Marketplace - Backend API
Version: v0.19 Marketplace Phase 1
REST API endpoints for marketplace operations
"""

from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
from marketplace_db import MarketplaceDB

# Initialize database
marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/api/marketplace')
db = MarketplaceDB()


# ============ PLUGIN ENDPOINTS ============

@marketplace_bp.route('/plugins/upload', methods=['POST'])
def upload_plugin():
    """Upload new plugin to marketplace"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['name', 'code', 'author_id', 'description']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create plugin
        plugin_id = db.create_plugin(
            name=data['name'],
            author_id=data['author_id'],
            code=data['code'],
            description=data.get('description', ''),
            category=data.get('category', 'General'),
            tags=data.get('tags', [])
        )
        
        if not plugin_id:
            return jsonify({'error': 'Plugin name already exists'}), 409
        
        # Verify plugin (admin would normally do this)
        db.verify_plugin(plugin_id)
        
        plugin = db.get_plugin(plugin_id)
        return jsonify({
            'status': 'success',
            'message': 'Plugin uploaded successfully',
            'plugin': plugin
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/plugins/<plugin_id>', methods=['GET'])
def get_plugin(plugin_id):
    """Get plugin details"""
    try:
        plugin = db.get_plugin(plugin_id)
        if not plugin:
            return jsonify({'error': 'Plugin not found'}), 404
        
        reviews = db.get_plugin_reviews(plugin_id)
        plugin['reviews'] = reviews
        
        return jsonify(plugin), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/plugins/search', methods=['GET'])
def search_plugins():
    """Search plugins"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category', '')
        limit = int(request.args.get('limit', 50))
        
        plugins = db.search_plugins(query=query, category=category, limit=limit)
        
        return jsonify({
            'status': 'success',
            'count': len(plugins),
            'plugins': plugins
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/plugins/trending', methods=['GET'])
def trending_plugins():
    """Get trending plugins"""
    try:
        limit = int(request.args.get('limit', 10))
        plugins = db.get_trending_plugins(limit=limit)
        
        return jsonify({
            'status': 'success',
            'plugins': plugins
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/plugins/by-creator/<creator_id>', methods=['GET'])
def creator_plugins(creator_id):
    """Get all plugins by creator"""
    try:
        plugins = db.get_creator_plugins(creator_id)
        
        return jsonify({
            'status': 'success',
            'count': len(plugins),
            'plugins': plugins
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/plugins/<plugin_id>/install', methods=['POST'])
def install_plugin(plugin_id):
    """Record plugin installation"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        plugin = db.get_plugin(plugin_id)
        if not plugin:
            return jsonify({'error': 'Plugin not found'}), 404
        
        # Record installation
        db.record_installation(plugin_id, user_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Plugin installed successfully',
            'plugin': plugin
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ REVIEW ENDPOINTS ============

@marketplace_bp.route('/plugins/<plugin_id>/reviews', methods=['GET'])
def get_reviews(plugin_id):
    """Get plugin reviews"""
    try:
        reviews = db.get_plugin_reviews(plugin_id)
        
        return jsonify({
            'status': 'success',
            'count': len(reviews),
            'reviews': reviews
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/plugins/<plugin_id>/reviews', methods=['POST'])
def add_review(plugin_id):
    """Add review for plugin"""
    try:
        data = request.json
        
        # Validate
        if 'rating' not in data or 'author_id' not in data:
            return jsonify({'error': 'rating and author_id required'}), 400
        
        if data['rating'] < 1 or data['rating'] > 5:
            return jsonify({'error': 'Rating must be 1-5'}), 400
        
        # Check plugin exists
        plugin = db.get_plugin(plugin_id)
        if not plugin:
            return jsonify({'error': 'Plugin not found'}), 404
        
        # Add review
        review_id = db.add_review(
            plugin_id=plugin_id,
            author_id=data['author_id'],
            rating=data['rating'],
            comment=data.get('comment', '')
        )
        
        # Get updated plugin
        updated_plugin = db.get_plugin(plugin_id)
        
        return jsonify({
            'status': 'success',
            'review_id': review_id,
            'plugin_rating': updated_plugin['rating']
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ CREATOR ENDPOINTS ============

@marketplace_bp.route('/creators', methods=['POST'])
def create_creator():
    """Create creator account"""
    try:
        data = request.json
        
        # Validate
        if 'username' not in data:
            return jsonify({'error': 'username required'}), 400
        
        # Create
        creator_id = db.create_creator(
            username=data['username'],
            email=data.get('email', ''),
            bio=data.get('bio', '')
        )
        
        if not creator_id:
            return jsonify({'error': 'Username already taken'}), 409
        
        creator = db.get_creator(creator_id)
        return jsonify({
            'status': 'success',
            'creator': creator
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/creators/<creator_id>', methods=['GET'])
def get_creator(creator_id):
    """Get creator profile"""
    try:
        creator = db.get_creator(creator_id)
        
        if not creator:
            return jsonify({'error': 'Creator not found'}), 404
        
        # Get creator's plugins
        plugins = db.get_creator_plugins(creator_id)
        creator['plugins'] = plugins
        
        return jsonify(creator), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/creators/<creator_id>/revenue', methods=['GET'])
def creator_revenue(creator_id):
    """Get creator revenue info"""
    try:
        creator = db.get_creator(creator_id)
        
        if not creator:
            return jsonify({'error': 'Creator not found'}), 404
        
        revenue = db.get_creator_revenue(creator_id)
        
        return jsonify({
            'creator_id': creator_id,
            'username': creator['username'],
            'total_revenue': revenue,
            'plugins_count': creator['plugins_count']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ INSTALLATION ENDPOINTS ============

@marketplace_bp.route('/users/<user_id>/installations', methods=['GET'])
def user_installations(user_id):
    """Get user's installed plugins"""
    try:
        plugin_ids = db.get_user_installations(user_id)
        plugins = [db.get_plugin(pid) for pid in plugin_ids]
        plugins = [p for p in plugins if p]  # Filter None values
        
        return jsonify({
            'status': 'success',
            'count': len(plugins),
            'plugins': plugins
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ REVENUE ENDPOINTS ============

@marketplace_bp.route('/revenue/record', methods=['POST'])
def record_sale():
    """Record plugin sale / revenue"""
    try:
        data = request.json
        
        # Validate
        required = ['plugin_id', 'creator_id', 'amount']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        revenue_id = db.record_revenue(
            plugin_id=data['plugin_id'],
            creator_id=data['creator_id'],
            amount=data['amount'],
            transaction_type=data.get('type', 'sale')
        )
        
        creator_revenue = db.get_creator_revenue(data['creator_id'])
        
        return jsonify({
            'status': 'success',
            'revenue_id': revenue_id,
            'creator_total_revenue': creator_revenue
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@marketplace_bp.route('/revenue/platform', methods=['GET'])
def platform_revenue():
    """Get platform total revenue"""
    try:
        revenue = db.get_platform_revenue()
        
        return jsonify({
            'platform_total_revenue': revenue,
            'currency': 'USD'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ STATS ENDPOINTS ============

@marketplace_bp.route('/stats', methods=['GET'])
def marketplace_stats():
    """Get marketplace statistics"""
    try:
        # Get all plugins
        all_plugins = db.search_plugins(limit=10000)
        
        total_plugins = len(all_plugins)
        total_downloads = sum(p['downloads'] for p in all_plugins)
        total_revenue = db.get_platform_revenue()
        
        return jsonify({
            'total_plugins': total_plugins,
            'total_downloads': total_downloads,
            'platform_revenue': total_revenue,
            'average_rating': sum(p['rating'] for p in all_plugins) / total_plugins if total_plugins > 0 else 0
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ HEALTH CHECK ============

@marketplace_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'marketplace'}), 200


if __name__ == "__main__":
    print("🔌 Plugin Marketplace API ready to be integrated")
