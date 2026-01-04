# Wedding Site Cleanup - TODO List

**Last Updated**: 2026-01-01
**Goal**: Remove RSVP app and create clean wedding information site

---

## 🔴 High Priority - Active Work

- [x] **Fix JavaScript API URL** - `wedding/static/js/ourstory-modal.js:7`
  - Change: `fetch('/story-entries/${storyId}/')`
  - To: `fetch('/wedding/story-entries/${storyId}/')`
  - **Impact**: Photo modals on "Our Story" page will 404 without this

- [ ] **Add StoryEntry content via Django admin**
  - Database has 0 story entries currently
  - Need to add photos/content before modals can be tested
  - Access: http://127.0.0.1:8000/admin/

- [ ] **Convert "Our Story" page to TailwindCSS grid**
  - Currently using Bootstrap classes (row, col-sm-3) - NOT WORKING
  - Need to convert to Tailwind grid layout
  - Make images responsive and arranged in proper grid
  - See options: 4-column grid OR masonry layout

---

## 🟡 Medium Priority - URL Rewiring

### Completed ✅

- [x] Updated root redirect from `/rsvp/` to `/wedding/`
- [x] Commented out RSVP URL include in `wedding_site/urls.py`
- [x] Fixed desktop navigation links to include `/wedding/` prefix
- [x] Fixed mobile navigation links to include `/wedding/` prefix
- [x] Removed/commented RSVP links from navigation

### Still To Do

- [ ] **Clean up outdated comment** in `wedding_site/urls.py:23`

  - Change comment from "Redirect root URL to RSVP"
  - To: "Redirect root URL to wedding home"
  - Optionally rename function from `redirect_to_rsvp` to `redirect_to_wedding`

- [ ] **Test all navigation links**
  - [ ] Desktop: Our Story, Itinerary, Gallery, Honeymoon Fund, FAQ
  - [ ] Mobile: All links (resize browser or test on phone)
  - [ ] Verify no 404 errors

---

## 🟢 Low Priority - Code Cleanup & Optimization

### ⚠️ RSVP Files Status: KEEPING THEM (Not Deleting)
**Decision:** Keep RSVP files in codebase but disable from active use

### Django Settings Cleanup

- [ ] **Remove 'rsvp' from INSTALLED_APPS** in `wedding_site/settings.py` (Line 58)
  ```python
  INSTALLED_APPS = [
      # ... other apps ...
      'wedding',
      'rest_framework',
      # 'rsvp'  ← Comment out or delete this line
  ]
  ```

- [ ] **Remove 'widget_tweaks' from INSTALLED_APPS** in `wedding_site/settings.py` (Line 55)
  - ✅ Confirmed: NOT used in wedding app
  - Remove line: `"widget_tweaks",`

- [ ] **Check if 'rsvp/static' is in STATICFILES_DIRS**
  - If explicitly listed, remove it
  - Likely not there (implicitly included)

### TailwindCSS Config

- [ ] **Remove RSVP templates from content paths** in `tailwind.config.js` (Line 5)
  ```javascript
  content: [
    "./wedding/templates/**/*.html",
    // "./rsvp/templates/**/*.html",  ← Remove this line
    "./wedding/static/js/**/*.js",
  ],
  ```

- [ ] **Rebuild CSS after config change**
  ```bash
  npm run build-css
  ```
  - Watcher will auto-rebuild if running
  - Or run manually with above command

### Procfile & Deployment

- [ ] **Update Procfile** - Remove reference to `run_migration.py`
  - Change: `web: python run_migration.py && gunicorn wedding_site.wsgi:application`
  - To: `web: python manage.py migrate && gunicorn wedding_site.wsgi:application`

### Dependency Cleanup (Optional)

- [ ] **Remove django-widget-tweaks from requirements.txt**
  - ✅ Confirmed: NOT used in wedding app
  - Optional: Can remove to reduce dependencies
  ```bash
  pip uninstall django-widget-tweaks
  pip freeze > requirements.txt
  ```

### Database Cleanup (Optional - If Removing RSVP from Settings)

- [ ] **After removing 'rsvp' from INSTALLED_APPS, Django may prompt to drop Guest table**
  ```bash
  python manage.py makemigrations
  # May detect rsvp app removal
  ```
  - You can choose to drop the table or leave it (harmless if unused)
  - Guest table will just sit there unused if you don't drop it

---

## 🧪 Testing Checklist

### Local Testing (Before Deploy)

- [ ] **All pages load without errors**

  - [ ] Home: http://127.0.0.1:8000 or http://127.0.0.1:8000/wedding/
  - [ ] Our Story: http://127.0.0.1:8000/wedding/our-story/
  - [ ] Itinerary: http://127.0.0.1:8000/wedding/itinerary/
  - [ ] Gallery: http://127.0.0.1:8000/wedding/gallery/
  - [ ] Honeymoon Fund: http://127.0.0.1:8000/wedding/honeymoon-fund/
  - [ ] FAQ: http://127.0.0.1:8000/wedding/faq/
  - [ ] Admin: http://127.0.0.1:8000/admin/

- [ ] **Static files load correctly**

  - [ ] CSS styles apply
  - [ ] Images display
  - [ ] JavaScript works (mobile menu, modals)

- [ ] **Check browser console**

  - [ ] No 404 errors
  - [ ] No JavaScript errors
  - [ ] No missing static files

- [ ] **Mobile responsiveness**
  - [ ] Resize browser to mobile width
  - [ ] Test mobile navigation menu
  - [ ] Verify all links work

### Production Testing (After Deploy)

- [ ] **Railway deployment succeeds**

  - Check Railway logs for errors
  - Verify migrations ran successfully

- [ ] **Ugly URL works**: http://wedding-site-production-8735.up.railway.app

  - Test all pages
  - Verify static files load

- [ ] **When ready: Re-add custom domain**

  - Add `foreverandalways.love` back in Railway
  - Wait 5-10 mins for DNS propagation
  - Test production site

- [ ] **Production site fully functional**
  - All pages load
  - No errors in Railway logs
  - Static files and media files work
  - Admin panel accessible

---

## 🚀 Deployment Steps

- [ ] **Pre-deployment checks**

  - [ ] All local tests passing
  - [ ] CSS rebuilt: `npm run build-css`
  - [ ] No uncommitted changes (or commit them)

- [ ] **Commit cleanup changes**

  ```bash
  git add .
  git commit -m "Remove RSVP app and clean up codebase

  - Deleted /rsvp/ directory and related scripts
  - Updated URL routing to wedding-only
  - Fixed navigation links (desktop + mobile)
  - Removed RSVP from settings and dependencies
  - Updated Procfile for standard migrations
  - Created migration to drop Guest table"
  ```

- [ ] **Push to Railway**

  ```bash
  git push origin main
  ```

- [ ] **Monitor deployment**

  - Watch Railway dashboard
  - Check build logs
  - Verify deployment succeeds

- [ ] **Post-deployment verification**
  - Test ugly URL
  - Check Railway logs for errors
  - Verify database migration ran

---

## 📝 Optional Improvements (Future)

- [ ] **Consider removing `/wedding/` prefix entirely**

  - Change `wedding_site/urls.py` to: `path('', include('wedding.urls'))`
  - URLs become: `/`, `/our-story/`, `/itinerary/` (cleaner)
  - Update all template links to remove `/wedding/` prefix

- [ ] **Evaluate if DRF is still needed**

  - If StoryEntry API is only used for "Our Story" page
  - Consider simplifying to server-side rendering
  - Would remove djangorestframework dependency

- [ ] **Add "Coming Soon" or "Under Construction" page**

  - If you want to hide work-in-progress from family

- [ ] **SEO improvements**

  - Add meta descriptions
  - Add Open Graph tags for social sharing
  - Add structured data for wedding event

- [ ] **Performance optimizations**
  - Image compression
  - Lazy loading for images
  - CSS minification

---

## 🐛 Known Issues / Bugs

_None currently - add any issues you discover here_

---

## 💡 Ideas / Future Features

_Add any ideas for the site here_

---

## Notes

- **Domain Status**: Custom domain removed from Railway
- **Ugly URL**: wedding-site-production-8735.up.railway.app
- **Local Dev**: Two terminals (Django + TailwindCSS watcher)
- **RSVP Files**: KEEPING in codebase, just removing from settings/config
- **Hard Refresh**: Always use Cmd+Shift+R after CSS/HTML changes! (See LOCAL_DEV_SETUP.md)
- **Our Story Issue**: Currently using Bootstrap grid classes but no Bootstrap CSS loaded
- **StoryEntry Database**: 0 entries currently - need to add via admin

---

**Progress Tracker**:

- ✅ URL rewiring complete
- ✅ JavaScript API fix complete
- ✅ Navigation links fixed (desktop + mobile)
- 🔄 Settings/config cleanup in progress
- 🔄 "Our Story" grid layout redesign in progress
- ⏳ RSVP settings removal pending (keeping files)
- ⏳ Final testing pending
- ⏳ Deployment pending
