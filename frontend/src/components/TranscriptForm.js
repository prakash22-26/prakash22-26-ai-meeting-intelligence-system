"use client";

import { useState } from "react";

import axios from "axios";

export default function TranscriptForm({
  setResult,

  setLoading,

  setError,
}) {
  const [file, setFile] = useState(null);

  const uploadMeeting = async () => {
    if (!file) {
      setError("Please select a file");

      return;
    }

    try {
      setLoading(true);

      setError("");

      const formData = new FormData();

      formData.append("file", file);

      const response = await axios.post(
        "https://prakash22-26-ai-meeting-intelligence.onrender.com",

        formData,

        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);

      setError(error.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="transcript-card">
      <h2>Upload Audio or Video Meeting</h2>

      <p className="upload-info">
        Supported formats: mp3, wav, m4a, mp4, mov, mkv
      </p>

      <input
        type="file"
        accept="
          .mp3,
          .wav,
          .m4a,
          .mp4,
          .mov,
          .mkv
        "
        onChange={(e) => setFile(e.target.files[0])}
        className="file-input"
      />

      {file && (
        <div className="selected-file">
          <p>Selected: {file.name}</p>
        </div>
      )}

      <button onClick={uploadMeeting}>Upload & Analyze</button>
    </div>
  );
}
