import React, { useState, useEffect } from 'react';
import { teamAPI } from '../api';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const data = await teamAPI.getTeams();
        setTeams(data.results || data);
      } catch (err) {
        setError('Failed to load teams');
        console.error('Teams error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
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
      await teamAPI.createTeam(formData);
      setFormData({ name: '', description: '' });
      setShowForm(false);
      const updatedTeams = await teamAPI.getTeams();
      setTeams(updatedTeams.results || updatedTeams);
    } catch (err) {
      setError('Failed to create team');
      console.error('Create team error:', err);
    }
  };

  if (loading) return <div className="container mt-5"><p>Loading...</p></div>;

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Teams</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Create Team'}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {showForm && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Create New Team</h5>
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Team Name</label>
                <input
                  type="text"
                  className="form-control"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
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
                Create Team
              </button>
            </form>
          </div>
        </div>
      )}

      <div className="row">
        {teams.length === 0 ? (
          <div className="col-12">
            <div className="alert alert-info">No teams found. Create one to get started!</div>
          </div>
        ) : (
          teams.map((team) => (
            <div key={team.id} className="col-md-6 mb-4">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{team.name}</h5>
                  <p className="card-text">{team.description}</p>
                  <div className="row text-center">
                    <div className="col">
                      <small className="text-muted">Members</small>
                      <p className="h5 mb-0">{team.members_count}</p>
                    </div>
                    <div className="col">
                      <small className="text-muted">Points</small>
                      <p className="h5 mb-0">{team.total_points}</p>
                    </div>
                  </div>
                  <button className="btn btn-sm btn-outline-primary w-100 mt-3">
                    View Team
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Teams;
