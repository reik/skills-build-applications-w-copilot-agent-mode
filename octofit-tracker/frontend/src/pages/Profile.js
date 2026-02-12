import React, { useState, useEffect } from 'react';
import { userAPI, achievementAPI } from '../api';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    bio: '',
    fitness_level: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileData, achievementsData] = await Promise.all([
          userAPI.getProfile('me'),
          achievementAPI.getUserAchievements(),
        ]);
        setProfile(profileData);
        setAchievements(achievementsData.results || achievementsData);
        setFormData({
          bio: profileData.bio || '',
          fitness_level: profileData.fitness_level || '',
        });
      } catch (err) {
        setError('Failed to load profile');
        console.error('Profile error:', err);
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
      const updatedProfile = await userAPI.updateProfile('me', formData);
      setProfile(updatedProfile);
      setEditMode(false);
    } catch (err) {
      setError('Failed to update profile');
      console.error('Update profile error:', err);
    }
  };

  if (loading) return <div className="container mt-5"><p>Loading...</p></div>;
  if (error) return <div className="container mt-5"><div className="alert alert-danger">{error}</div></div>;

  return (
    <div className="container mt-5">
      <h1 className="mb-4">My Profile</h1>

      <div className="row">
        <div className="col-md-8">
          <div className="card mb-4">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Profile Information</h5>
              <button
                className="btn btn-sm btn-outline-primary"
                onClick={() => setEditMode(!editMode)}
              >
                {editMode ? 'Cancel' : 'Edit'}
              </button>
            </div>
            <div className="card-body">
              {editMode ? (
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label">Bio</label>
                    <textarea
                      className="form-control"
                      name="bio"
                      value={formData.bio}
                      onChange={handleInputChange}
                      rows="3"
                    ></textarea>
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Fitness Level</label>
                    <select
                      className="form-select"
                      name="fitness_level"
                      value={formData.fitness_level}
                      onChange={handleInputChange}
                    >
                      <option value="">Select fitness level</option>
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>
                  <button type="submit" className="btn btn-success">
                    Save Changes
                  </button>
                </form>
              ) : (
                <>
                  <p>
                    <strong>Username:</strong> {profile?.user?.username}
                  </p>
                  <p>
                    <strong>Email:</strong> {profile?.user?.email}
                  </p>
                  <p>
                    <strong>Bio:</strong> {profile?.bio || 'No bio added yet'}
                  </p>
                  <p>
                    <strong>Fitness Level:</strong>{' '}
                    <span className="badge bg-info">{profile?.fitness_level}</span>
                  </p>
                  <p>
                    <strong>Total Points:</strong>{' '}
                    <span className="badge bg-success fs-6">{profile?.total_points}</span>
                  </p>
                  <p>
                    <strong>Member Since:</strong>{' '}
                    {new Date(profile?.created_at).toLocaleDateString()}
                  </p>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Achievements</h5>
            </div>
            <div className="card-body">
              {achievements.length === 0 ? (
                <p className="text-muted text-center">No achievements yet. Keep logging activities!</p>
              ) : (
                <div className="achievement-grid">
                  {achievements.map((achievement) => (
                    <div key={achievement.id} className="text-center mb-3">
                      <div
                        style={{
                          fontSize: '2rem',
                          marginBottom: '0.5rem',
                        }}
                      >
                        🏆
                      </div>
                      <small className="d-block">{achievement.name}</small>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
