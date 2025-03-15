import { useState } from 'react';

import './frontend_styles.css';
export default function App() {
  const [mriFile, setMriFile] = useState(null);
  const [dnaSequence, setDnaSequence] = useState('');
  const [result, setResult] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [alertMessage, setAlertMessage] = useState(null);

  const uploadMRI = async () => {
    if (!mriFile) return alert("Please select an MRI file");
    const formData = new FormData();
    formData.append('file', mriFile);
    const res = await fetch("http://localhost:8000/upload_mri/", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    alert(data.message);
    setPrediction(data.predicted_class);
  };

  const analyzeGeneSequence = async () => {
    const res = await fetch("http://localhost:8000/analyze_gene_sequence/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tumor_type: prediction, dna_sequence: dnaSequence })
    });
    const data = await res.json();

    if (data.alert) {
      setAlertMessage(data.alert);
      setResult(null);
    } else {
      setAlertMessage(null);
      setResult(data);
    }
  };

  return (
    <div className="container">
      <h1>Medical Analysis System</h1>
      
      <div className="card">
        <label>Upload MRI</label>
        <input type="file" onChange={(e) => setMriFile(e.target.files[0])} />
        <button onClick={uploadMRI}>Upload</button>
      </div>

      {prediction && (
        <div className="result-card">
          <h2>Tumor Prediction</h2>
          <p><strong>Predicted Tumor Type:</strong> {prediction}</p>
        </div>
      )}

      <div className="card">
        <label>DNA Sequence</label>
        <textarea value={dnaSequence} onChange={(e) => setDnaSequence(e.target.value)} />
        <button onClick={analyzeGeneSequence}>Analyze</button>
      </div>

      {alertMessage && (
        <div className="alert">
          <h2>⚠ Warning</h2>
          <p>{alertMessage}</p>
        </div>
      )}

      {result && (
        <div className="result-card">
          <h2>Gene Analysis Results</h2>
          <p><strong>Tumor Type:</strong> {result.tumor_type}</p>
          <p><strong>GC Content:</strong> {result.gc_content !== null ? result.gc_content.toFixed(2) : "N/A"}</p>
          <h3>Recommended Treatments</h3>
          <h4>Standard Treatments</h4>
          <ul>
            {result.standard_treatments.map((t, i) => (
              <li key={i}>{t.name} - {t.mechanism}</li>
            ))}
          </ul>
          <h4>Personalized Treatments</h4>
          <ul>
            {result.personalized_treatments.map((t, i) => (
              <li key={i}>{t.name} - {t.mechanism} ({t.reason})</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
