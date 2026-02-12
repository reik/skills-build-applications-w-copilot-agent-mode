import React, { useState, useEffect } from 'react';
import { activityAPI, activityTypeAPI } from '../api';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [activityTypes, setActivityTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    activity_type_id: '',
    distance_or_duration: '',
    calories_burned: '',
    description: '',
    points_earned: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [activitiesData, typesData] = await Promise.all([
          activityAPI.getActivities(),
          activityTypeAPI.getActivityTypes(),
        ]);
        setActivities(activitiesData.results || activitiesData);
        setActivityTypes(typesData.results || typesData);
      } catch (err) {
        setError('Failed to load activities');
        console.error('Activities error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await activityAPI.createActivity(formData);
      setFormData({
        activity_type_id: '',
        distance_or_duration: '',
        calories_burned: '',
        description: '',
        points_earned: '',
      });
      setShowForm(false);
      // Refresh activities
      const updatedActivities = await activityAPI.getActivities();
      setActivities(updatedActivities.results || updatedActivities);
    } catch (err) {
      setError('Failed to create activity');
      console.error('Create activity error:', err);
    }
  };

  if (loading) return <div className="container mt-5"><p>Loading...</p></div>;

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Activities</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Log Activity'}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {showForm && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Log New Activity</h5>
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Activity Type</label>
                <select
                  className="form-select"
                  name="activity_type_id"
                  value={formData.activity_type_id}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select an activity type</option>
                  {activityTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">Duration/Distance</label>
                  <input
                    type="number"
                    className="form-control"
                    name="distance_or_duration"
                    value={formData.distance_or_duration}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label className="form-label">Calories Burned</label>
                  <input
                    type="number"
                    className="form-control"
                    name="calories_burned"
                    value={formData.calories_burned}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">Points Earned</label>
                  <input
                    type="number"
                    className="form-control"
                    name="points_earned"
                    value={formData.points_earned}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
              <div className="mb-3">
                <label className="form-label">Description</label>
                <textarea
                  className="form-control"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows="3"
                ></textarea>
              </div>
              <button type="submit" className="btn btn-success">
                Log Activity
              </button>
            </form>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-body">
          {activities.length === 0 ? (
            <p className="text-muted">No activities logged yet.</p>
          ) : (
            <div className="table-responsive">
              <table className="table">
                <thead>
                  <tr>
                    <th>Activity</th>
                    <th>Duration/Distance</th>
                    <th>Calories</th>
                    <th>Points</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {activities.map((activity) => (
                    <tr key={activity.id}>
                      <td>{activity.activity_type?.name}</td>
                      <td>
                        {activity.distance_or_duration} {activity.activity_type?.unit}
                      </td>
                      <td>{activity.calories_burned}</td>
                      <td>
                        <span className="badge bg-success">{activity.points_earned}</span>
                      </td>
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
  );
}

export default Activities;
