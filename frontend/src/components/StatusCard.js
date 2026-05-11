export default function StatusCard() {

  return (
    <div className="status-card">

      <h2>System Status</h2>

      <div className="status-item">
        <span>FastAPI Backend</span>
        <span className="active">Active</span>
      </div>

      <div className="status-item">
        <span>Groq AI</span>
        <span className="active">Connected</span>
      </div>

      <div className="status-item">
        <span>PostgreSQL</span>
        <span className="active">Online</span>
      </div>
    </div>
  );
}