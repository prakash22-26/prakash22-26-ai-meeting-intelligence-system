export default function SummaryCard({ result }) {
  return (
    <div className="summary-card">
      <h2>AI Meeting Intelligence</h2>

      {/* MEETING OVERVIEW */}

      <div className="summary-section">
        <h3>Meeting Overview</h3>

        <p>
          <strong>Title:</strong> {result.meeting_overview?.title || "N/A"}
        </p>

        <p>
          <strong>Objective:</strong>{" "}
          {result.meeting_overview?.main_objective || "N/A"}
        </p>

        <p>
          {result.meeting_overview?.overall_summary || "No summary generated"}
        </p>
      </div>

      {/* PARTICIPANTS */}

      <div className="summary-section">
        <h3>Participants</h3>

        {result.participants_detected?.length > 0 ? (
          <ul>
            {result.participants_detected.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p>No participants detected</p>
        )}
      </div>

      {/* IMPORTANT POINTS */}

      <div className="summary-section">
        <h3>Important Points</h3>

        {result.important_points?.length > 0 ? (
          result.important_points.map((item, index) => (
            <div key={index} className="insight-card">
              {typeof item === "string" ? (
                <p>{item}</p>
              ) : (
                <>
                  <h4>{item.topic}</h4>

                  <p>{item.details}</p>
                </>
              )}
            </div>
          ))
        ) : (
          <p>No important points found</p>
        )}
      </div>

      {/* DETAILED DISCUSSIONS */}

      <div className="summary-section">
        <h3>Detailed Discussions</h3>

        {result.detailed_discussions?.length > 0 ? (
          result.detailed_discussions.map((item, index) => (
            <div key={index} className="discussion-card">
              <h4>{item.topic || "Discussion"}</h4>

              <p>{item.details || item.discussion}</p>
            </div>
          ))
        ) : (
          <p>No discussions found</p>
        )}
      </div>

      {/* ACTION ITEMS */}

      <div className="summary-section">
        <h3>Action Items</h3>

        {result.action_items?.filter(
          (item) => item && (item.task || item.action || item.description),
        )?.length > 0 ? (
          result.action_items

            .filter(
              (item) => item && (item.task || item.action || item.description),
            )

            .map((item, index) => {
              const taskText =
                item.task ||
                item.action ||
                item.description ||
                "No task description";

              return (
                <div key={index} className="action-item">
                  <div>
                    <p>{taskText}</p>
                  </div>

                  <span className="priority-badge">
                    {item.priority || "Medium"}
                  </span>
                </div>
              );
            })
        ) : (
          <p>No action items found</p>
        )}
      </div>

      {/* QUESTIONS & ANSWERS */}

      <div className="summary-section">
        <h3>Questions & Answers</h3>

        {result.questions_and_answers?.length > 0 ? (
          result.questions_and_answers.map((item, index) => (
            <div key={index} className="qa-card">
              <p>
                <strong>Question:</strong> {item.question || "N/A"}
              </p>

              <p>
                <strong>Answer:</strong> {item.answer || "N/A"}
              </p>
            </div>
          ))
        ) : (
          <p>No questions identified</p>
        )}
      </div>

      {/* RISKS */}

      <div className="summary-section">
        <h3>Problems & Risks</h3>

        {result.problems_or_risks?.length > 0 ? (
          <ul>
            {result.problems_or_risks.map((item, index) => (
              <li key={index}>{typeof item === "string" ? item : item.risk}</li>
            ))}
          </ul>
        ) : (
          <p>No risks identified</p>
        )}
      </div>

      {/* FUTURE PLANS */}

      <div className="summary-section">
        <h3>Future Plans</h3>

        {result.future_plans?.length > 0 ? (
          <ul>
            {result.future_plans.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p>No future plans found</p>
        )}
      </div>

      {/* IMPORTANT NOTES */}

      <div className="summary-section">
        <h3>Important Notes</h3>

        {result.important_notes?.length > 0 ? (
          <ul>
            {result.important_notes.map((item, index) => (
              <li key={index}>{typeof item === "string" ? item : item.note}</li>
            ))}
          </ul>
        ) : (
          <p>No important notes</p>
        )}
      </div>

      {/* NEXT STEPS */}

      <div className="summary-section">
        <h3>Next Steps</h3>

        {result.next_steps?.length > 0 ? (
          <ul>
            {result.next_steps.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p>No next steps identified</p>
        )}
      </div>

      {/* FINAL CONCLUSION */}

      <div className="summary-section">
        <h3>Final Conclusion</h3>

        <p>{result.final_conclusion || "No conclusion generated"}</p>
      </div>
    </div>
  );
}
