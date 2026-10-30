import React, { useState } from 'react';
import {
  FileText,
  Upload,
  CheckCircle,
  AlertTriangle,
  Lock,
  Cpu,
  FileCheck,
  Sparkles,
  Trash2,
  RotateCcw,
  Eye,
  X,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { apiService } from '../services/api';
import { ImageUploadResponse } from '../types';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

const MAX_FILE_SIZE_MB = 15;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;
const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.txt'];

export const Documents: React.FC = () => {
  const { t } = useLanguage();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePreviewUrl, setFilePreviewUrl] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [result, setResult] = useState<ImageUploadResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const validateAndSetFile = (file: File) => {
    setErrorMsg(null);
    setResult(null);

    // Validate size
    if (file.size > MAX_FILE_SIZE_BYTES) {
      setErrorMsg(`File size (${(file.size / (1024 * 1024)).toFixed(1)} MB) exceeds the ${MAX_FILE_SIZE_MB}MB limit.`);
      return;
    }

    // Validate extension
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      setErrorMsg(`Unsupported file type '${ext}'. Please upload PDF, PNG, JPG, JPEG, or TXT.`);
      return;
    }

    setSelectedFile(file);

    // Create image preview if image
    if (file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      setFilePreviewUrl(url);
    } else {
      setFilePreviewUrl(null);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleRemoveFile = () => {
    if (filePreviewUrl) {
      URL.revokeObjectURL(filePreviewUrl);
    }
    setSelectedFile(null);
    setFilePreviewUrl(null);
    setResult(null);
    setErrorMsg(null);
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64String = (reader.result as string).split(',')[1];
        resolve(base64String);
      };
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file);
    });
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setErrorMsg(null);
    setUploadProgress(25);

    try {
      const base64Content = await fileToBase64(selectedFile);
      setUploadProgress(65);

      const res = await apiService.uploadDocument({
        filename: selectedFile.name,
        content_base64: base64Content,
        prompt: prompt.trim() || undefined,
      });

      setUploadProgress(100);
      setResult(res);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to process medical document. Please check the file and try again.');
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  };

  const loadSampleLabReport = () => {
    const sampleText = `PATIENT CLINICAL REPORT: COMPLETE BLOOD COUNT (CBC) & SERUM FERRITIN
Age: 38 | Sex: Female
Date: 2026-10-28

TEST RESULTS:
- Hemoglobin (Hb): 9.4 g/dL [Reference: 12.0 - 15.5 g/dL] (LOW)
- Packed Cell Volume (PCV): 29.5% [Reference: 37.0 - 48.0%] (LOW)
- Mean Corpuscular Volume (MCV): 72.0 fL [Reference: 80.0 - 100.0 fL] (LOW - Microcytic)
- Mean Corpuscular Hemoglobin (MCH): 23.1 pg [Reference: 27.0 - 33.0 pg] (LOW - Hypochromic)
- Serum Ferritin: 8.2 ng/mL [Reference: 15 - 150 ng/mL] (SEVERELY LOW)
- Platelet Count: 245,000 /mcL [Reference: 150,000 - 450,000 /mcL] (NORMAL)

Clinical Notes: Microcytic hypochromic indices consistent with marked iron deficiency.`;

    const blob = new Blob([sampleText], { type: 'text/plain' });
    const file = new File([blob], 'sample_cbc_ferritin_test_report.txt', { type: 'text/plain' });
    validateAndSetFile(file);
    setPrompt('What do these lab values indicate, and what dietary or clinical next steps are recommended?');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Page Title */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <Badge variant="cyan" className="mx-auto">
          Diagnostic Document Analysis
        </Badge>
        <h1 className="text-3xl font-black text-white tracking-tight">
          {t('doc.title') || 'Medical Document & Lab Report Analysis'}
        </h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Securely upload clinical test results, prescriptions, or imaging scans for instant plain-language synthesis.
        </p>
      </div>

      {/* Upload Box */}
      <Card className="p-6 sm:p-8 border-cyan-500/30 bg-slate-900/80 space-y-6">
        {/* Drag & Drop Area */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-all bg-slate-950/60 ${
            isDragging
              ? 'border-cyan-400 bg-cyan-950/20'
              : 'border-slate-700 hover:border-cyan-500/60'
          }`}
        >
          <input
            type="file"
            accept=".pdf,.png,.jpg,.jpeg,.txt"
            onChange={handleFileChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />

          <div className="flex flex-col items-center justify-center space-y-3 pointer-events-none">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              <Upload className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-200">
                {selectedFile ? selectedFile.name : 'Drag & drop your medical document or click to browse'}
              </p>
              <p className="text-xs text-slate-500 mt-1">
                Supports PDF, PNG, JPG, JPEG, and TXT (Max {MAX_FILE_SIZE_MB}MB)
              </p>
            </div>
          </div>
        </div>

        {/* Selected File Card & Preview */}
        {selectedFile && (
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="flex items-center gap-3">
              {filePreviewUrl ? (
                <img
                  src={filePreviewUrl}
                  alt="Document Preview"
                  className="w-12 h-12 object-cover rounded-lg border border-slate-700"
                />
              ) : (
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-800 text-cyan-400">
                  <FileText className="w-5 h-5" />
                </div>
              )}
              <div>
                <h4 className="text-xs font-bold text-white truncate max-w-xs sm:max-w-md">
                  {selectedFile.name}
                </h4>
                <span className="text-[11px] text-slate-400">
                  {(selectedFile.size / 1024).toFixed(1)} KB • {selectedFile.type || 'Plain text document'}
                </span>
              </div>
            </div>

            <button
              onClick={handleRemoveFile}
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-900 transition-colors"
              title="Remove selected file"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Upload Progress Bar if processing */}
        {isLoading && (
          <div className="space-y-1.5">
            <div className="flex items-center justify-between text-xs font-semibold text-cyan-300">
              <span>Extracting and analyzing document text...</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-cyan-500 to-teal-400 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}

        {/* Pre-loaded Sample Option */}
        <div className="flex items-center justify-between text-xs pt-1">
          <span className="text-slate-500">Need a sample lab report to evaluate?</span>
          <button
            onClick={loadSampleLabReport}
            className="text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1 hover:underline"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Load Sample CBC & Ferritin Report</span>
          </button>
        </div>

        {/* Optional Question */}
        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-slate-300">
            Specific Inquiry About This Report (Optional)
          </label>
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. Summarize the diagnostic findings, or What does this ferritin level mean?"
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>

        {/* Security Notice */}
        <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-950/70 p-3 rounded-xl border border-slate-800">
          <Lock className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>
            Uploads are verified with cryptographic SHA-256 hashes and isolated from public index.
          </span>
        </div>

        {/* Submit Button */}
        <div className="flex items-center justify-end gap-3 pt-2">
          {selectedFile && (
            <Button variant="ghost" size="md" onClick={handleRemoveFile}>
              Cancel
            </Button>
          )}
          <Button
            onClick={handleUpload}
            disabled={!selectedFile || isLoading}
            isLoading={isLoading}
            size="lg"
            icon={<FileCheck className="w-4 h-4 text-slate-950" />}
          >
            Analyze Document
          </Button>
        </div>
      </Card>

      {/* Error Message */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-red-950/50 border border-red-500/50 text-xs text-rose-300 flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <AlertTriangle className="w-5 h-5 text-red-400 shrink-0" />
            <span>{errorMsg}</span>
          </div>
          <Button variant="outline" size="sm" onClick={handleUpload} icon={<RotateCcw className="w-3.5 h-3.5" />}>
            Retry
          </Button>
        </div>
      )}

      {/* Analysis Results Display */}
      {result && (
        <Card className="p-6 sm:p-8 border-emerald-500/40 bg-slate-900/90 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4 flex-wrap gap-2">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                <FileCheck className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">{result.original_filename}</h3>
                <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                  <span className="font-mono text-cyan-400 text-[11px]">
                    SHA-256: {result.sha256_hash.substring(0, 16)}...
                  </span>
                  <span>•</span>
                  <span>{(result.size_bytes / 1024).toFixed(1)} KB</span>
                </div>
              </div>
            </div>

            <Badge variant="emerald">Processing Complete</Badge>
          </div>

          {/* Extracted Text */}
          {result.text_extracted && (
            <div className="space-y-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-cyan-400" />
                <span>Extracted Document Text</span>
              </h4>
              <div className="rounded-xl bg-slate-950 p-4 font-mono text-xs text-slate-300 whitespace-pre-wrap max-h-48 overflow-y-auto border border-slate-800">
                {result.text_extracted}
              </div>
            </div>
          )}

          {/* Clinical Interpretation */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Clinical Interpretation & Plain-Language Summary</span>
            </h4>
            <div className="rounded-xl bg-slate-950/80 border border-cyan-500/30 p-5 text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">
              {result.clinical_interpretation}
            </div>
          </div>

          {/* Safety Note */}
          <div className="rounded-xl bg-amber-950/30 border border-amber-500/40 p-4 text-xs text-amber-300 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong className="block font-semibold">Medical Limitation Notice:</strong>
              <span>{result.safety_note}</span>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
