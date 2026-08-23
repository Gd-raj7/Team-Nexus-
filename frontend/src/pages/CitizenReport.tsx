import { useState, useEffect, useRef } from 'react';
import { api } from '../lib/api';
import { FilePlus, ClipboardCheck, ArrowRight, UploadCloud, Compass, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

type LocationStatus = 'idle' | 'detecting' | 'success' | 'denied';

export default function CitizenReport() {
  const navigate = useNavigate();


  
  // Upload Mode States
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string>('');
  const [dragActive, setDragActive] = useState(false);

  const [citizenName, setCitizenName] = useState('');
  const [phone, setPhone] = useState('');
  const [description, setDescription] = useState('');
  
  // Location States (explicit for Upload mode)
  const [locationName, setLocationName] = useState('');
  const [latitude, setLatitude] = useState<string>('');
  const [longitude, setLongitude] = useState<string>('');
  const [locationStatus, setLocationStatus] = useState<LocationStatus>('idle');
  
  const mapRef = useRef<any>(null);
  const markerRef = useRef<any>(null);

  const [submitting, setSubmitting] = useState(false);
  const [submittedReport, setSubmittedReport] = useState<any>(null);





  // Synchronize Leaflet map with coordinate states
  useEffect(() => {
    const L = (window as any).L;
    if (!L) return;

    const latVal = parseFloat(latitude);
    const lonVal = parseFloat(longitude);

    if (isNaN(latVal) || isNaN(lonVal)) {
      // If coordinates are cleared, remove the map
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
        markerRef.current = null;
      }
      return;
    }

    const container = document.getElementById('report-map');
    if (!container) return;

    // Use a premium looking custom circle marker
    const customIcon = L.divIcon({
      html: `<div style="
        background-color: var(--accent-blue, #2563eb); 
        width: 14px; 
        height: 14px; 
        border-radius: 50%; 
        border: 2px solid white; 
        box-shadow: 0 0 6px rgba(0,0,0,0.3);
      "></div>`,
      className: 'custom-gps-marker',
      iconSize: [14, 14],
      iconAnchor: [7, 7]
    });

    if (!mapRef.current) {
      mapRef.current = L.map('report-map', {
        zoomControl: true,
      }).setView([latVal, lonVal], 15);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
      }).addTo(mapRef.current);

      markerRef.current = L.marker([latVal, lonVal], { icon: customIcon }).addTo(mapRef.current);
    } else {
      mapRef.current.setView([latVal, lonVal], 15);
      if (markerRef.current) {
        markerRef.current.setLatLng([latVal, lonVal]);
      } else {
        markerRef.current = L.marker([latVal, lonVal], { icon: customIcon }).addTo(mapRef.current);
      }
    }
  }, [latitude, longitude]);

  // Cleanup map on component unmount
  useEffect(() => {
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
        markerRef.current = null;
      }
    };
  }, []);


  // Browser Geolocation
  const handleGetLocation = () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by your browser');
      return;
    }
    setLocationStatus('detecting');
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(String(position.coords.latitude.toFixed(6)));
        setLongitude(String(position.coords.longitude.toFixed(6)));
        setLocationName('Current Location');
        setLocationStatus('success');
      },
      (error) => {
        console.error(error);
        setLocationStatus('denied');
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  // Drag and Drop validation helpers
  const handleFile = (file: File) => {
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      alert('Unsupported file format. Only JPG, PNG, and WEBP are supported.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      alert('File size exceeds the 10 MB limit.');
      return;
    }
    setUploadedFile(file);
    const reader = new FileReader();
    reader.onloadend = () => {
      setFilePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  // Drag Handlers
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const removeFile = () => {
    setUploadedFile(null);
    setFilePreview('');
  };

  // Form Submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validations
    if (!uploadedFile) {
      alert('Please upload a civic issue photo.');
      return;
    }
    if (!latitude || !longitude) {
      alert('Location is required. Please use "Use My Current Location" to capture your GPS coordinates.');
      return;
    }

    setSubmitting(true);
    try {
      // Automatically map ward based on coordinate presets, fallback to general ward
      let calculatedWard = 'Ward 1 - Municipal General';

      const payload = {
        citizen_name: citizenName,
        phone,
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        address: locationName || 'Unknown Location',
        ward: calculatedWard,
        description,
        image_file: uploadedFile,
      };

      await api.submitReport(payload);
      // Immediately navigate to dashboard
      navigate('/');
    } catch (err: any) {
      console.error(err);
      alert(`Submission failed: ${err.message || err}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700, color: 'var(--text-primary)' }}>
          Submit Citizen Report
        </h2>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
          Submit a new civic grievance complaint. Choose between real image uploads with automatic GPS detection, or pre-seeded scenario images to trigger demo clustering.
        </p>
      </div>

      {!submittedReport ? (
        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 16 }}>
          
          {/* UPLOAD MODE VIEW */}
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>
              Report Issue Photo
            </label>

              {!filePreview ? (
                /* Drag & Drop Input Area */
                <div
                  onDragEnter={handleDrag}
                  onDragOver={handleDrag}
                  onDragLeave={handleDrag}
                  onDrop={handleDrop}
                  style={{
                    border: `2px dashed ${dragActive ? 'var(--accent-blue)' : 'var(--border-secondary)'}`,
                    borderRadius: 8,
                    background: dragActive ? 'rgba(37, 99, 235, 0.04)' : 'var(--bg-primary)',
                    padding: '32px 16px',
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: 12,
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                  onClick={() => document.getElementById('citizen-photo-input')?.click()}
                >
                  <UploadCloud size={32} color={dragActive ? 'var(--accent-blue)' : 'var(--text-tertiary)'} />
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)', marginBottom: 2 }}>
                      Upload Civic Issue Photo
                    </div>
                    <div style={{ fontSize: 11, color: 'var(--text-secondary)' }}>
                      Drag and drop an image here or click to browse
                    </div>
                  </div>
                  
                  <input
                    id="citizen-photo-input"
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    style={{ display: 'none' }}
                    onChange={handleFileSelect}
                  />

                  <button
                    type="button"
                    className="btn btn-secondary"
                    style={{ fontSize: 11, padding: '4px 12px' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      document.getElementById('citizen-photo-input')?.click();
                    }}
                  >
                    CHOOSE IMAGE
                  </button>

                  <div style={{ fontSize: 10, color: 'var(--text-tertiary)' }}>
                    JPG, PNG, WEBP • Max 10 MB
                  </div>
                </div>
              ) : (
                /* Preview Area */
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 16,
                  padding: 12,
                  background: 'var(--bg-primary)',
                  border: '1px solid var(--border-primary)',
                  borderRadius: 8,
                }}>
                  <img
                    src={filePreview}
                    alt="Citizen Upload Preview"
                    style={{
                      width: 90,
                      height: 70,
                      borderRadius: 6,
                      objectFit: 'cover',
                      border: '1px solid var(--border-primary)'
                    }}
                  />
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6, flex: 1 }}>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-primary)' }}>Image Selected</span>
                      <span style={{ fontSize: 10, color: 'var(--text-secondary)', wordBreak: 'break-all' }}>
                        File: {uploadedFile?.name}
                      </span>
                    </div>
                    <div style={{ display: 'flex', gap: 8 }}>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => document.getElementById('citizen-photo-input')?.click()}
                        style={{ fontSize: 10, padding: '3px 8px' }}
                      >
                        Replace Image
                      </button>
                      <button
                        type="button"
                        className="btn btn-danger"
                        onClick={removeFile}
                        style={{ fontSize: 10, padding: '3px 8px' }}
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          {/* Contact Details Card */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <h3 style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>Contact Details</h3>
              <div>
                <label style={{ display: 'block', fontSize: 11, color: 'var(--text-secondary)', marginBottom: 4 }}>Name</label>
                <input
                  className="input"
                  value={citizenName}
                  onChange={(e) => setCitizenName(e.target.value)}
                  required
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: 11, color: 'var(--text-secondary)', marginBottom: 4 }}>Phone</label>
                <input
                  className="input"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Location Manager Details Card */}
            <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <h3 style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>Report Location</h3>

                /* Auto-detect location for Upload Mode */
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {locationStatus === 'idle' && (
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, padding: '12px 0' }}>
                      <div style={{ fontSize: 12, color: 'var(--text-tertiary)', textAlign: 'center' }}>
                        Tap below to automatically detect your current location
                      </div>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={handleGetLocation}
                        style={{ fontSize: 11, padding: '8px 16px', gap: 6 }}
                      >
                        <Compass size={14} />
                        Use My Current Location
                      </button>
                    </div>
                  )}

                  {locationStatus === 'detecting' && (
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 10,
                      padding: '12px 14px',
                      borderRadius: 8,
                      background: 'rgba(37, 99, 235, 0.06)',
                      border: '1px solid rgba(37, 99, 235, 0.15)',
                    }}>
                      <Compass size={16} color="var(--accent-blue)" className="animate-spin" />
                      <span style={{ fontSize: 12, color: 'var(--accent-blue)', fontWeight: 500 }}>Detecting your location…</span>
                    </div>
                  )}

                  {locationStatus === 'success' && (
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 10,
                      padding: '12px 14px',
                      borderRadius: 8,
                      background: 'rgba(34, 197, 94, 0.06)',
                      border: '1px solid rgba(34, 197, 94, 0.2)',
                    }}>
                      <CheckCircle2 size={18} color="#22c55e" />
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                        <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-primary)' }}>📍 Location Detected</span>
                        <span style={{ fontSize: 11, color: 'var(--text-secondary)' }}>Current location captured successfully</span>
                      </div>
                    </div>
                  )}

                  {locationStatus === 'denied' && (
                    <div style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: 10,
                      padding: '12px 14px',
                      borderRadius: 8,
                      background: 'rgba(239, 68, 68, 0.06)',
                      border: '1px solid rgba(239, 68, 68, 0.2)',
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <AlertTriangle size={16} color="#ef4444" />
                        <span style={{ fontSize: 12, fontWeight: 600, color: '#ef4444' }}>Location Access Denied</span>
                      </div>
                      <span style={{ fontSize: 11, color: 'var(--text-secondary)' }}>
                        Location access is required to connect this report with nearby civic incidents.
                      </span>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={handleGetLocation}
                        style={{ fontSize: 10, padding: '5px 12px', gap: 4, width: 'fit-content' }}
                      >
                        <Compass size={12} />
                        Retry Location Access
                      </button>
                    </div>
                  )}
                </div>

              {/* Leaflet Map Integration */}
              {latitude && longitude && (
                <div 
                  id="report-map" 
                  style={{ 
                    height: '200px', 
                    width: '100%', 
                    borderRadius: '8px', 
                    marginTop: '12px',
                    border: '1px solid var(--border-primary)',
                    zIndex: 10
                  }}
                />
              )}
            </div>
          </div>

          {/* Description Card */}
          <div className="card">
            <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'var(--text-primary)', marginBottom: 6 }}>
              Description
            </label>
            <textarea
              className="input"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Provide a brief description of the issue..."
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={submitting || !uploadedFile}
            style={{ padding: 12, justifyContent: 'center' }}
          >
            {submitting ? (
              <span className="spinner" />
            ) : (
              <>
                <FilePlus size={16} />
                Submit Complaint Report
              </>
            )}
          </button>
        </form>
      ) : (
        /* Submission Success View */
        <div className="card" style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '40px 20px',
          textAlign: 'center',
          gap: 16,
        }}>
          <div style={{
            width: 48,
            height: 48,
            borderRadius: '50%',
            background: 'var(--status-resolved-bg)',
            border: '1px solid var(--status-resolved)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <ClipboardCheck size={24} color="var(--status-resolved)" />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)' }}>
              Grievance Successfully Filed
            </h3>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
              Your complaint has been logged under ID: <strong className="font-mono" style={{ color: 'var(--accent-blue)' }}>{submittedReport.report_id}</strong>
            </p>
          </div>

          <div style={{
            display: 'flex',
            gap: 12,
            marginTop: 12,
          }}>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setSubmittedReport(null);
                setUploadedFile(null);
                setFilePreview('');

                setLatitude('');
                setLongitude('');
                setLocationName('');
                setDescription('');
              }}
            >
              Submit Another Report
            </button>
            <button
              className="btn btn-primary"
              onClick={() => {
                navigate('/', { state: { autoAnalyzeId: submittedReport.report_id } });
              }}
            >
              Go to Dashboard and Analyze
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
