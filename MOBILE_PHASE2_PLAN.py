"""
RIJWAL_LANG Mobile Web Version - Phase 2
Responsive IDE for phones/tablets
"""

# ============================================================================
# KEY CHANGES FOR MOBILE
# ============================================================================

MOBILE_CHANGES = """
PHASE 2: MOBILE WEB VERSION (Weeks 5-8)
========================================

✅ WEEK 5: Responsive Design
  - Fluid layouts (320px - 1920px)
  - Touch-friendly buttons (44px minimum)
  - Mobile-first CSS
  - Hamburger menu instead of sidebars
  - Collapsible panels

✅ WEEK 6: Mobile Features
  - Touch keyboard support
  - Swipe gestures
  - Mobile-optimized editor
  - Reduced animations
  - Offline mode (PWA)

✅ WEEK 7: Progressive Web App
  - Service worker
  - Installable app
  - Push notifications
  - Background sync
  - Works offline

✅ WEEK 8: Testing & Launch
  - iOS Safari testing
  - Android Chrome testing
  - Performance optimization
  - Marketing push

========================================
TARGET METRICS:
- 30% traffic from mobile (vs 5% now)
- 2,000+ users
- 50K mobile sessions/month
- 10K app installs
- $5K/month revenue
========================================
"""

# ============================================================================
# RESPONSIVE CSS BREAKPOINTS
# ============================================================================

RESPONSIVE_CSS = """
/* Mobile First - Base styles for mobile (320px) */

.container { width: 100%; padding: 10px; }
.sidebar { display: none; }  /* Hide sidebars on mobile */
.toolbar { display: flex; flex-wrap: wrap; gap: 8px; }
.editor { font-size: 14px; }
.button { min-height: 44px; min-width: 44px; }

/* Hamburger menu for mobile */
.hamburger-menu { display: block; }

/* Tablet (768px+) */
@media (min-width: 768px) {
  .sidebar { display: block; width: 300px; }
  .hamburger-menu { display: none; }
  .toolbar { flex-wrap: nowrap; }
  .editor { font-size: 16px; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: auto; }
  .dual-sidebar { display: flex; gap: 10px; }
  .editor { font-size: 14px; }
  .button { min-height: auto; min-width: auto; }
}
"""

# ============================================================================
# TOUCH GESTURES
# ============================================================================

TOUCH_GESTURES = """
// Handle touch events on mobile
document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchend', handleTouchEnd, false);

let xDown = null;
let yDown = null;

function handleTouchStart(e) {
  xDown = e.touches[0].clientX;
  yDown = e.touches[0].clientY;
}

function handleTouchEnd(e) {
  let xUp = e.changedTouches[0].clientX;
  let yUp = e.changedTouches[0].clientY;
  
  let xDiff = xDown - xUp;
  let yDiff = yDown - yUp;
  
  if (Math.abs(xDiff) > Math.abs(yDiff)) {
    // Horizontal swipe
    if (xDiff > 0) {
      // Swipe left - hide sidebar
      document.getElementById('sidebar').style.right = '-100%';
    } else {
      // Swipe right - show sidebar
      document.getElementById('sidebar').style.right = '0';
    }
  }
}
"""

# ============================================================================
# PWA SERVICE WORKER
# ============================================================================

PWA_SERVICE_WORKER = """
// service-worker.js - PWA offline support

const CACHE_NAME = 'rijwal-v1';
const urlsToCache = [
  '/',
  '/ide_with_games.html',
  '/style.css',
  '/script.js',
  '/manifest.json'
];

// Install - cache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      if (response) return response;
      
      return fetch(event.request).then(response => {
        // Cache successful responses
        if (!response || response.status !== 200) {
          return response;
        }
        
        const responseToCache = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseToCache);
        });
        
        return response;
      });
    }).catch(() => {
      // Offline fallback
      return new Response('Offline - some features unavailable', {
        status: 503,
        statusText: 'Service Unavailable'
      });
    })
  );
});

// Activate - clean old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
"""

# ============================================================================
# PWA MANIFEST
# ============================================================================

PWA_MANIFEST = """
{
  "name": "Rijwal_Lang IDE",
  "short_name": "Rijwal",
  "description": "Code anywhere, anytime - Rijwal_Lang IDE",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1a1a2e",
  "orientation": "portrait-primary",
  
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icon-192-maskable.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  
  "screenshots": [
    {
      "src": "/screenshot-540x720.png",
      "sizes": "540x720",
      "type": "image/png"
    }
  ],
  
  "categories": ["productivity", "utilities"],
  "shortcuts": [
    {
      "name": "Create New File",
      "short_name": "New",
      "description": "Create a new Rijwal file",
      "url": "/?new",
      "icons": [{"src": "/icon-192.png", "sizes": "192x192"}]
    }
  ]
}
"""

# ============================================================================
# MOBILE OPTIMIZATIONS
# ============================================================================

MOBILE_OPTIMIZATIONS = """
// mobile-optimizations.js

class MobileOptimizations {
  
  // Reduce animation on low-end devices
  static reduceAnimations() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.documentElement.style.setProperty('--animation-duration', '0s');
    }
  }
  
  // Detect device capabilities
  static detectCapabilities() {
    return {
      touch: 'ontouchstart' in window,
      vibration: 'vibrate' in navigator,
      camera: navigator.mediaDevices?.getUserMedia,
      geolocation: 'geolocation' in navigator,
      offline: 'serviceWorker' in navigator,
      battery: 'getBattery' in navigator
    };
  }
  
  // Optimize for dark mode
  static applyDarkMode() {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  }
  
  // Lazy load non-critical resources
  static lazyLoad() {
    if ('IntersectionObserver' in window) {
      const images = document.querySelectorAll('img[data-src]');
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.src = entry.target.dataset.src;
            observer.unobserve(entry.target);
          }
        });
      });
      images.forEach(img => imageObserver.observe(img));
    }
  }
  
  // Monitor battery status
  static monitorBattery() {
    if ('getBattery' in navigator) {
      navigator.getBattery().then(battery => {
        battery.addEventListener('levelchange', () => {
          if (battery.level < 20 && !battery.charging) {
            console.warn('⚠️ Battery low - reducing animations');
          }
        });
      });
    }
  }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
  MobileOptimizations.reduceAnimations();
  MobileOptimizations.applyDarkMode();
  MobileOptimizations.lazyLoad();
  MobileOptimizations.monitorBattery();
  
  console.log('📱 Mobile optimizations applied');
  console.log('Capabilities:', MobileOptimizations.detectCapabilities());
});
"""

# ============================================================================
# MOBILE GAMES OPTIMIZATION
# ============================================================================

MOBILE_GAMES = """
// Mobile Game Optimizations

class MobileGameOptimizer {
  
  static optimizeSnake() {
    // Use arrow buttons or swipe gestures
    // Reduce grid size on small screens
    // Lower frame rate for battery saving
    return {
      grid_size: window.innerWidth < 768 ? 12 : 20,
      touch_buttons: true,
      swipe_enabled: true,
      fps: window.innerWidth < 768 ? 10 : 15
    };
  }
  
  static optimizePong() {
    // Single finger control on mobile
    // Simplified physics
    // Touch-friendly paddle
    return {
      control: 'touch',
      paddle_size: window.innerWidth < 768 ? 60 : 40,
      touch_responsive: true
    };
  }
  
  static optimizeCodeChallenge() {
    // Larger text for readability
    // Less code per challenge
    // Swipe to next challenge
    return {
      font_size: window.innerWidth < 768 ? '16px' : '14px',
      code_lines: window.innerWidth < 768 ? 3 : 5,
      swipe_navigation: true
    };
  }
}
"""

# ============================================================================
# PROGRESSIVE ENHANCEMENT
# ============================================================================

PROGRESSIVE_ENHANCEMENT = """
// Progressive Enhancement - works without JavaScript

<!-- Basic HTML works -->
<form action="/api/execute" method="POST">
  <textarea name="code"></textarea>
  <button type="submit">Run Code</button>
</form>

<!-- JavaScript enhances with:
  - Live preview
  - Syntax highlighting
  - Code completion
  - Games
  - AI assistant
  - Plugins
  - Dark mode
  - etc
-->
"""

if __name__ == "__main__":
    print("📱 PHASE 2: MOBILE WEB VERSION")
    print("=" * 60)
    print("""
✅ Files to create:
   1. service-worker.js - PWA offline support
   2. manifest.json - App configuration
   3. mobile-optimizations.js - Touch & device detection
   4. mobile-styles.css - Responsive design
   5. mobile-games.js - Optimized games

✅ Changes to ide_with_games.html:
   - Responsive grid layout
   - Hamburger menu
   - Touch gestures
   - Mobile toolbar
   - PWA manifest link

✅ Testing:
   - Chrome DevTools Device Emulation
   - iPhone/iPad simulator
   - Android emulator
   - Real device testing

✅ Deployment:
   - HTTPS required for PWA
   - Service worker registration
   - App install prompt
   - Analytics tracking

📊 Target:
   - 30% mobile traffic
   - 2K+ mobile users
   - 50K mobile sessions/month
   - 10K+ app installs
   - $5K/month revenue
""")
