import React, { useState, useEffect } from 'react';
import { challengeAPI } from '../api';

function Challenges() {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const data = await challengeAPI.getChallenges();
        setChallenges(data.results || data);
      } catch (err) {
        setError('Failed to load challenges');
        console.error('Challenges error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchChallenges();
  }, []);

  const handleJoinChallenge = async (challengeId) => {
    try {
      await challengeAPI.joinChallenge(challengeId);
      // Refresh challenges
      const data = await challengeAPI.getChallenges();
      setChallenges(data.results || data);
    } catch (err) {
      setError('Failed to join challenge');
      console.error('Join challenge error:', err);
    }
  };

  if (loading) return <div className="container mt-5"><p>Loading...</p></div>;

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Challenges</h1>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="row">
        {challenges.length === 0 ? (
          <div className="col-12">
            <div className="alert alert-info">No challenges available at the moment.</div>
          </div>
        ) : (
          challenges.map((challenge) => (
            <div key={challenge.id} className="col-md-6 mb-4">
              <div className="card">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <h5 className="card-title">{challenge.name}</h5>
                    {challenge.is_active && (
                      <span className="badge bg-success">Active</span>
                    )}
                  </div>
                  <p className="card-text">{challenge.description}</p>
                  <div className="row text-center mb-3">
                    <div className="col">
                      <small className="text-muted">Goal Points</small>
                      <p className="h6 mb-0">{challenge.goal_points}</p>
                    </div>
                    <div className="col">
                      <small className="text-muted">Participants</small>
                      <p className="h6 mb-0">{challenge.participants_count}</p>
                    </div>
                  </div>
                  <div className="mb-3">
                    <small className="text-muted">
                      {new Date(challenge.start_date).toLocaleDateString()} -{' '}
                      {new Date(challenge.end_date).toLocaleDateString()}
                    </small>
                  </div>
                  {challenge.is_active && (
                    <button
                      className="btn btn-primary w-100"
                      onClick={() => handleJoinChallenge(challenge.id)}
                    >
                      Join Challenge
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Challenges;
