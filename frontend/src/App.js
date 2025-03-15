import { useState } from 'react';

export default function App() {
  const [mriFile, setMriFile] = useState(null);
  const [dnaSequence, setDnaSequence] = useState('');
  const [result, setResult] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [alertMessage, setAlertMessage] = useState(null); // New state for alert messages

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
    setPrediction(data.predicted_class); // Store tumor prediction result
  };

  const analyzeGeneSequence = async () => {
    const res = await fetch("http://localhost:8000/analyze_gene_sequence/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tumor_type: prediction, dna_sequence: dnaSequence })
    });
    const data = await res.json();

    // Check if the response contains an alert (short sequence case)
    if (data.alert) {
      setAlertMessage(data.alert);
      setResult(null); // Clear the result so no error occurs
    } else {
      setAlertMessage(null);
      setResult(data);
    }
  };

  return (
    <div className="p-5 max-w-lg mx-auto">
      <h1 className="text-xl font-bold">Medical Analysis</h1>
      
      <div className="my-4">
        <label className="block">Upload MRI</label>
        <input type="file" onChange={(e) => setMriFile(e.target.files[0])} />
        <button className="bg-blue-500 text-white px-3 py-1 mt-2" onClick={uploadMRI}>Upload</button>
      </div>

      

      <div className="my-4">
        <label className="block">DNA Sequence</label>
        <textarea className="border p-2 w-full" value={dnaSequence} onChange={(e) => setDnaSequence(e.target.value)} />
      </div>

      <button className="bg-green-500 text-white px-3 py-1" onClick={analyzeGeneSequence}>Analyze</button>

      {alertMessage && (
        <div className="mt-5 p-4 border border-red-500 bg-red-100 text-red-700 rounded">
          <h2 className="text-lg font-bold">⚠ Warning</h2>
          <p>{alertMessage}</p>
        </div>
      )}

      {result && (
        <div className="mt-5 p-4 border rounded">
          <h2 className="text-lg font-bold">Gene Analysis Results</h2>
          <p><strong>Tumor Type:</strong> {result.tumor_type}</p>
          <p><strong>GC Content:</strong> {result.gc_content !== null ? result.gc_content.toFixed(2) : "N/A"}</p>
          <h3 className="text-md font-semibold">Recommended Treatments</h3>
          <h4 className="text-md font-semibold">Standard Treatments</h4>
          <ul>
            {result.standard_treatments.map((t, i) => (
              <li key={i}>{t.name} - {t.mechanism}</li>
            ))}
          </ul>
          <h4 className="text-md font-semibold">Personalized Treatments</h4>
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