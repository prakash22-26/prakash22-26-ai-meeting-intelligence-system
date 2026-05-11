"use client";

import { useState } from "react";

import TranscriptForm from "./TranscriptForm";
import SummaryCard from "./SummaryCard";
import StatusCard from "./StatusCard";

import "../styles/dashboard.css";

export default function Dashboard() {

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  return (

    <div className="dashboard-container">

      {/* HEADER */}

      <div className="dashboard-header">

        <div>

          <h1>
            AI Meeting Intelligence
          </h1>

          <p>
            Upload audio/video meetings and generate AI-powered insights.
          </p>

        </div>

      </div>

      {/* TOP GRID */}

      <div className="dashboard-grid">

        <TranscriptForm

          setResult={setResult}

          setLoading={setLoading}

          setError={setError}

        />

        <StatusCard />

      </div>

      {/* LOADING */}

      {
        loading && (

          <div className="loading-card">

            <h3>
              Processing Meeting...
            </h3>

            <p>
              Transcribing audio/video and generating AI insights.
            </p>

          </div>
        )
      }

      {/* ERROR */}

      {
        error && (

          <div className="error-card">

            <h3>
              Error
            </h3>

            <p>
              {error}
            </p>

          </div>
        )
      }

      {/* RESULTS */}

      {
        result && (

          <SummaryCard
            result={result}
          />
        )
      }

      {/* EMPTY STATE */}

      {
        !loading &&
        !result &&
        !error && (

          <div className="empty-card">

            <h3>
              No Meeting Uploaded
            </h3>

            <p>
              Upload a meeting audio or video file to generate summaries, action items, risks, decisions, and technical insights.
            </p>

          </div>
        )
      }

    </div>
  );
}