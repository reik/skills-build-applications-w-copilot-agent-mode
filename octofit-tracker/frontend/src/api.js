// API service for communicating with the OctoFit Tracker backend

// Get the base URL for the backend API
const getApiBaseUrl = () => {
  // Check if we're in a GitHub Codespaces environment
  if (window.location.hostname.includes('github.dev') || window.location.hostname.includes('app.github.dev')) {
    // Extract the hostname and replace the frontend port (3000) with backend port (8000)
    const hostname = window.location.hostname.replace('-3000.', '-8000.');
    const protocol = window.location.protocol;
    return `${protocol}//${hostname}/api`;
  }
  
  // Default to localhost for local development or use environment variable
  return process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
};

const API_BASE_URL = getApiBaseUrl();

// Helper function to get the authorization token
const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

// Helper function to set the authorization token
const setAuthToken = (token) => {
  localStorage.setItem('authToken', token);
};

// Helper function to clear the authorization token
const clearAuthToken = () => {
  localStorage.removeItem('authToken');
};

// Helper function to make API calls
const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const token = getAuthToken();
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken();
      window.location.href = '/login';
    }
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

// Auth API endpoints
export const authAPI = {
  login: (username, password) =>
    apiCall('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
  logout: () =>
    apiCall('/auth/logout/', { method: 'POST' }),
  register: (userData) =>
    apiCall('/auth/registration/', {
      method: 'POST',
      body: JSON.stringify(userData),
    }),
  getCurrentUser: () =>
    apiCall('/profiles/me/'),
};

// User Profile API endpoints
export const userAPI = {
  getProfile: (userId) =>
    apiCall(`/profiles/${userId}/`),
  updateProfile: (userId, data) =>
    apiCall(`/profiles/${userId}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  getLeaderboard: () =>
    apiCall('/profiles/leaderboard/'),
};

// Activity API endpoints
export const activityAPI = {
  getActivities: (page = 1) =>
    apiCall(`/activities/?page=${page}`),
  getActivity: (id) =>
    apiCall(`/activities/${id}/`),
  createActivity: (data) =>
    apiCall('/activities/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  updateActivity: (id, data) =>
    apiCall(`/activities/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  deleteActivity: (id) =>
    apiCall(`/activities/${id}/`, { method: 'DELETE' }),
  getRecentActivities: () =>
    apiCall('/activities/recent/'),
  getActivityStats: () =>
    apiCall('/activities/stats/'),
};

// Activity Type API endpoints
export const activityTypeAPI = {
  getActivityTypes: () =>
    apiCall('/activity-types/'),
  getActivityType: (id) =>
    apiCall(`/activity-types/${id}/`),
};

// Team API endpoints
export const teamAPI = {
  getTeams: (page = 1) =>
    apiCall(`/teams/?page=${page}`),
  getTeam: (id) =>
    apiCall(`/teams/${id}/`),
  createTeam: (data) =>
    apiCall('/teams/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  updateTeam: (id, data) =>
    apiCall(`/teams/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  deleteTeam: (id) =>
    apiCall(`/teams/${id}/`, { method: 'DELETE' }),
  addMember: (teamId, userId) =>
    apiCall(`/teams/${teamId}/add_member/`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    }),
  removeMember: (teamId, userId) =>
    apiCall(`/teams/${teamId}/remove_member/`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    }),
  getMembers: (teamId) =>
    apiCall(`/teams/${teamId}/members/`),
};

// Leaderboard API endpoints
export const leaderboardAPI = {
  getLeaderboard: (type = 'individual', period = 'weekly') =>
    apiCall(`/leaderboard/?type=${type}&period=${period}`),
  getIndividualLeaderboard: (period = 'weekly') =>
    apiCall(`/leaderboard/individual/?period=${period}`),
  getTeamLeaderboard: (period = 'weekly') =>
    apiCall(`/leaderboard/teams/?period=${period}`),
};

// Challenge API endpoints
export const challengeAPI = {
  getChallenges: (page = 1) =>
    apiCall(`/challenges/?page=${page}`),
  getChallenge: (id) =>
    apiCall(`/challenges/${id}/`),
  getActiveChallenges: () =>
    apiCall('/challenges/active/'),
  createChallenge: (data) =>
    apiCall('/challenges/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  joinChallenge: (id) =>
    apiCall(`/challenges/${id}/join/`, { method: 'POST' }),
  leaveChallenge: (id) =>
    apiCall(`/challenges/${id}/leave/`, { method: 'POST' }),
  getChallengeParticipants: (id) =>
    apiCall(`/challenges/${id}/participants/`),
};

// Achievement API endpoints
export const achievementAPI = {
  getAchievements: () =>
    apiCall('/achievements/'),
  getUserAchievements: () =>
    apiCall('/achievements/user_achievements/'),
};

// Export auth token utility functions
export { getAuthToken, setAuthToken, clearAuthToken };
