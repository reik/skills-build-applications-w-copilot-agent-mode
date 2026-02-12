import React, { useState, useEffect } from 'react';
import { leaderboardAPI } from '../api';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [leaderboardType, setLeaderboardType] = useState('individual');
  const [period, setPeriod] = useState('weekly');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true);
        const data = await leaderboardAPI.getLeaderboard(leaderboardType, period);
        setLeaderboard(data.results || data);
      } catch (err) {
        setError('Failed to load leaderboard');
        console.error('Leaderboard error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, [leaderboardType, period]);

  if (loading) return <div className="container mt-5"><p>Loading...</p></div>;

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Leaderboard</h1>

      <div className="row mb-4">
        <div className="col-md-6">
          <label className="form-label">Type</label>
          <select
            className="form-select"
            value={leaderboardType}
            onChange={(e) => setLeaderboardType(e.target.value)}
          >
            <option value="individual">Individual</option>
            <option value="team">Team</option>
          </select>
        </div>
        <div className="col-md-6">
          <label className="form-label">Period</label>
          <select
            className="form-select"
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="all_time">All Time</option>
          </select>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        <div className="card-body">
          {leaderboard.length === 0 ? (
            <p className="text-muted text-center">No leaderboard data available.</p>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>{leaderboardType === 'individual' ? 'User' : 'Team'}</th>
                    <th>Points</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry, index) => (
                    <tr key={entry.id}>
                      <td>
                        <span className="badge bg-primary">{entry.rank}</span>
                      </td>
                      <td>
                        {entry.user ? entry.user.username : entry.team?.name}
                      </td>
                      <td>
                        <span className="badge bg-success fs-6">{entry.points}</span>
                      </td>
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

export default Leaderboard;
