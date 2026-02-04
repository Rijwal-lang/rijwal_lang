#!/usr/bin/env python3
"""
Upload Example Plugins to Marketplace
Run this to populate marketplace with 10 example plugins
"""

import requests
import json
from example_plugins import EXAMPLE_PLUGINS

BASE_URL = "http://localhost:5000/api/marketplace"

def upload_all_plugins():
    """Upload all example plugins"""
    print("🚀 Uploading example plugins to marketplace...")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for plugin in EXAMPLE_PLUGINS:
        try:
            # Upload plugin
            response = requests.post(
                f"{BASE_URL}/plugins/upload",
                json=plugin,
                timeout=5
            )
            
            if response.status_code == 201:
                data = response.json()
                plugin_id = data['plugin']['id']
                print(f"✅ {plugin['name']:<30} (ID: {plugin_id[:8]}...)")
                success_count += 1
                
                # Add 5-star review
                try:
                    requests.post(
                        f"{BASE_URL}/plugins/{plugin_id}/reviews",
                        json={
                            'author_id': 'rijwal_user',
                            'rating': 5,
                            'comment': 'Great plugin!'
                        },
                        timeout=5
                    )
                except:
                    pass
            else:
                print(f"❌ {plugin['name']:<30} (Status: {response.status_code})")
                error_count += 1
        except Exception as e:
            print(f"❌ {plugin['name']:<30} (Error: {str(e)[:30]}...)")
            error_count += 1
    
    print("=" * 60)
    print(f"✅ Uploaded: {success_count}")
    print(f"❌ Failed: {error_count}")
    print(f"📊 Total: {success_count + error_count}")
    
    if success_count > 0:
        # Get stats
        try:
            stats = requests.get(f"{BASE_URL}/stats", timeout=5).json()
            print(f"\n📈 Marketplace Stats:")
            print(f"   Plugins: {stats.get('total_plugins', 0)}")
            print(f"   Downloads: {stats.get('total_downloads', 0)}")
            print(f"   Average Rating: {stats.get('average_rating', 0):.1f}⭐")
            print(f"   Revenue: ${stats.get('platform_revenue', 0):.2f}")
        except:
            pass


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  RIJWAL MARKETPLACE - PLUGIN UPLOADER")
    print("=" * 60 + "\n")
    
    # Check if server is running
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=2)
        if health.status_code == 200:
            upload_all_plugins()
        else:
            print("❌ Marketplace server not responding")
            print(f"   Run: python rijwal_ide_launcher.py")
    except Exception as e:
        print("❌ Cannot connect to marketplace server")
        print(f"   Error: {e}")
        print(f"\n📝 Steps to fix:")
        print(f"   1. Start IDE: python rijwal_ide_launcher.py")
        print(f"   2. Wait for server to start")
        print(f"   3. Run this script again")
