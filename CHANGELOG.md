# Changelog

All notable changes to django-admin-query-executor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-17

### Added
- Initial release of django-admin-query-executor
- QueryExecutorMixin for adding query execution to Django ModelAdmin classes
- Support for full Django ORM query syntax including:
  - Basic queries (filter, exclude, get, all)
  - Aggregations (Count, Sum, Avg, Max, Min, StdDev, Variance)
  - Annotations and F() expressions
  - Q objects for complex queries
  - Subqueries with Exists, OuterRef, Subquery
  - Database functions (Lower, Upper, Concat, etc.)
  - Date/time functions (TruncDate, Extract, Now, etc.)
- Query history tracking (last 20 queries per user)
- Favorite queries with custom names (up to 50 per user)
- Collapsible interface integrated into admin changelist
- Comprehensive dark mode support:
  - Automatic detection of system color scheme preferences
  - Full compatibility with Django admin's native dark mode
  - Support for popular admin themes (Grappelli, Jazzmin, Admin Interface)
  - CSS variables for easy customization
  - Smooth transitions between light and dark themes
  - Accessible color contrasts in both modes
  - Custom `query_executor_dark_mode.css` stylesheet
- AJAX-based execution without page reload
- Smart result detection (queryset vs scalar results)
- Responsive design with mobile-friendly dark mode
- Automatic application of queryset results to admin changelist
- Session-based query filtering
- Cache-based storage for history and favorites
- Security features:
  - Restricted execution environment
  - Whitelisted functions only
  - No direct SQL execution
  - Model access restrictions
- Customizable query examples per ModelAdmin
- Mobile responsive design
- "Click to expand/collapse" toggle text
- Local storage for UI state persistence

### Security
- Implemented safe query execution using restricted eval() environment
- All user input is validated and sanitized
- Only approved Django ORM functions are accessible
- No access to private methods or attributes
- No file system or network access from queries

[1.0.0]: https://github.com/j4rf/django-admin-query-executor/releases/tag/v1.0.0
