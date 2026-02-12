import React from 'react';
import { Link } from 'react-router-dom';
import { getAuthToken } from '../api';
import './Home.css';

function Home() {
  const isAuthenticated = !!getAuthToken();

  return (
    <div className="home-container">
      <section className="hero-section text-center py-5">
        <div className="container">
          <h1 className="display-3 fw-bold mb-4">🐙 Welcome to OctoFit Tracker</h1>
          <p className="lead mb-4">
            Your personal fitness companion for tracking activities, competing with friends, and achieving your health goals!
          </p>
          <div className="hero-buttons">
            {isAuthenticated ? (
              <>
                <Link className="btn btn-primary btn-lg me-3" to="/dashboard">
                  Go to Dashboard
                </Link>
                <Link className="btn btn-outline-secondary btn-lg" to="/leaderboard">
                  View Leaderboard
                </Link>
              </>
            ) : (
              <>
                <Link className="btn btn-primary btn-lg me-3" to="/login">
                  Login
                </Link>
                <Link className="btn btn-outline-primary btn-lg" to="/register">
                  Create Account
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      <section className="features-section py-5 bg-light">
        <div className="container">
          <h2 className="text-center mb-5">Features</h2>
          <div className="row">
            <div className="col-md-3 mb-4">
              <div className="feature-card text-center p-4">
                <div className="feature-icon mb-3">📊</div>
                <h4>Track Activities</h4>
                <p>Log your workouts and activities to earn points and track your progress.</p>
              </div>
            </div>
            <div className="col-md-3 mb-4">
              <div className="feature-card text-center p-4">
                <div className="feature-icon mb-3">👥</div>
                <h4>Build Teams</h4>
                <p>Create teams and compete with friends in fitness challenges.</p>
              </div>
            </div>
            <div className="col-md-3 mb-4">
              <div className="feature-card text-center p-4">
                <div className="feature-icon mb-3">🏆</div>
                <h4>Leaderboards</h4>
                <p>Climb the ranks with our competitive leaderboard system.</p>
              </div>
            </div>
            <div className="col-md-3 mb-4">
              <div className="feature-card text-center p-4">
                <div className="feature-icon mb-3">🎯</div>
                <h4>Challenges</h4>
                <p>Join monthly challenges and achieve special accomplishments.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="stats-section py-5">
        <div className="container">
          <div className="row text-center">
            <div className="col-md-4 mb-4">
              <h3 className="display-5 fw-bold">500+</h3>
              <p className="lead">Active Users</p>
            </div>
            <div className="col-md-4 mb-4">
              <h3 className="display-5 fw-bold">10K+</h3>
              <p className="lead">Activities Logged</p>
            </div>
            <div className="col-md-4 mb-4">
              <h3 className="display-5 fw-bold">50+</h3>
              <p className="lead">Active Teams</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section text-center py-5 bg-primary text-white">
        <div className="container">
          <h2 className="mb-4">Ready to Get Started?</h2>
          <p className="lead mb-4">Join OctoFit Tracker today and start your fitness journey!</p>
          {!isAuthenticated && (
            <Link className="btn btn-light btn-lg" to="/register">
              Sign Up Now
            </Link>
          )}
        </div>
      </section>
    </div>
  );
}

export default Home;
