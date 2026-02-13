---
mode: 'agent'
model: 'GPT-4.1'
---

# Django App Updates

- All Django project files are in the `octofit-tracker/backend/octofit_tracker` directory.

1. Update `settings.py` for MongoDB connection and CORS.
2. Update `models.py`, `serializers.py`, `urls.py`, `views.py`, `tests.py`, and `admin.py` to support users, teams, activities, leaderboard, and workouts collections.
3. Ensure `/` points to the api and `api_root` is present in `urls.py`.

# React App Updates

- All React frontend files are in the `octofit-tracker/frontend/src` directory.

## Components to Update

Update the following components to connect to the backend REST API:

- `src/App.js`
- `src/index.js`
- `src/pages/Activities.js`
- `src/pages/Leaderboard.js`
- `src/pages/Teams.js`
- `src/pages/Profile.js`
- `src/pages/Dashboard.js`

## API Connection Requirements

1. **API Endpoint Configuration**
   - In each component, replace fetch URLs with the Codespace URL pattern:
     ```
     https://${REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/[component]/
     ```
   - Use the correct port (8000 for backend) and protocol (https for Codespaces).
   - Ensure all components pull data from the REST API endpoints for display in the React frontend.

2. **Data Fetching**
   - Make components compatible with both paginated (`.results`) and plain array responses.
   - Add console.log statements to log:
     - The REST API endpoint being called
     - The fetched data response
   - Example:
     ```javascript
     console.log(`Fetching from: ${apiUrl}`);
     console.log('Response data:', data);
     ```

3. **Navigation**
   - Update `src/App.js` to include main navigation for all components.
   - Ensure `react-router-dom` is used for the navigation menu.
   - The React app should display both the navigation menu and the routed components.

4. **Error Handling**
   - Add appropriate error handling for failed API requests.
   - Display user-friendly error messages when API calls fail.
