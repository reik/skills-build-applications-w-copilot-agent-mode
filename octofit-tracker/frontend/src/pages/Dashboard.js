import React, { useState, useEffect } from 'react';
import { userAPI, activityAPI } from '../api';

function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [stats, setStats] = useState(null);
  const [recentActivities, setRecentActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileData, statsData, activitiesData] = await Promise.all([
          userAPI.getProfile('me'),
          activityAPI.getActivityStats(),
          activityAPI.getRecentActivities(),
        ]);
        setProfile(profileData);
        setStats(statsData);
        setRecentActivities(activitiesData);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="container mt-5"><p>Loading...</p></div>;
  if (error) return <div className="container mt-5"><div className="alert alert-danger">{error}</div></div>;

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Dashboard</h1>
      
      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h5 className="card-title">Total Points</h5>
              <h2 className="text-primary">{profile?.total_points || 0}</h2>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h5 className="card-title">Activities</h5>
              <h2 className="text-success">{stats?.total_activities || 0}</h2>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h5 className="card-title">Calories Burned</h5>
              <h2 className="text-warning">{stats?.total_calories || 0}</h2>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-center">
            <div className="card-body">
              <h5 className="card-title">Fitness Level</h5>
              <h3 className="text-info">{profile?.fitness_level || 'N/A'}</h3>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-md-8">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Recent Activities</h5>
            </div>
            <div className="card-body">
              {recentActivities.length === 0 ? (
                <p className="text-muted">No activities yet. Start logging your workouts!</p>
              ) : (
                <div className="table-responsive">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Activity</th>
                        <th>Duration</th>
                        <th>Points</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {recentActivities.map((activity) => (
                        <tr key={activity.id}>
                          <td>{activity.activity_type?.name}</td>
                          <td>{activity.distance_or_duration} {activity.activity_type?.unit}</td>
                          <td><span className="badge bg-success">{activity.points_earned}</span></td>
                          <td>{new Date(activity.logged_at).toLocaleDateString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">User Info</h5>
            </div>
            <div className="card-body">
              <p><strong>Username:</strong> {profile?.user?.username}</p>
              <p><strong>Email:</strong> {profile?.user?.email}</p>
              <p><strong>Fitness Level:</strong> {profile?.fitness_level}</p>
              <p><strong>Member Since:</strong> {new Date(profile?.created_at).toLocaleDateString()}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
