/* SoilVision AI — Upload Page JS */
'use strict';
const uploadZone      = document.getElementById('uploadZone');
const fileInput       = document.getElementById('reportFileInput');
const uploadProgress  = document.getElementById('uploadProgress');
const uploadError     = document.getElementById('uploadError');
const step1           = document.getElementById('step1');
const step2           = document.getElementById('step2');
const uploadTips      = document.getElementById('uploadTips');
const resetUploadBtn  = document.getElementById('resetUploadBtn');
const extractedForm   = document.getElementById('extractedForm');

if (uploadZone) {
  uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
  uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
  uploadZone.addEventListener('drop', e => {
    e.preventDefault(); uploadZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) processFile(file);
  });
}
if (fileInput) fileInput.addEventListener('change', () => { if (fileInput.files[0]) processFile(fileInput.files[0]); });

async function processFile(file) {
  const allowed = ['application/pdf','image/jpeg','image/png','image/jpg'];
  if (!allowed.includes(file.type) && !file.name.match(/\.(pdf|jpg|jpeg|png)$/i)) {
    showError('Unsupported file format. Please upload a PDF, JPG, or PNG file.');
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showError('File size exceeds 10 MB. Please compress or crop the image.');
    return;
  }
  uploadError.style.display = 'none';
  uploadProgress.style.display = 'block';
  uploadZone.style.display = 'none';

  const fd = new FormData();
  fd.append('report_file', file);
  try {
    const res  = await fetch('/api/upload', { method: 'POST', body: fd });
    const data = await res.json();
    if (data.error) { showError(data.error); return; }
    fillExtractedForm(data.extracted || {});
    step2.style.display = 'block';
    if (uploadTips) uploadTips.style.display = 'none';
    step2.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch(e) {
    showError('Upload failed. Please check your connection and try again.');
  } finally {
    uploadProgress.style.display = 'none';
  }
}

function showError(msg) {
  uploadZone.style.display = 'block';
  uploadProgress.style.display = 'none';
  uploadError.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> ${msg}`;
  uploadError.style.display = 'flex';
}

function fillExtractedForm(extracted) {
  const mapping = { ph:'ext_ph', ec:'ext_ec', oc:'ext_oc', nitrogen:'ext_nitrogen', phosphorus:'ext_phosphorus', potassium:'ext_potassium', zinc:'ext_zinc', iron:'ext_iron', copper:'ext_copper', manganese:'ext_manganese', boron:'ext_boron', sulphur:'ext_sulphur', farmer_name:'ext_farmer_name', target_crop:'ext_target_crop' };
  Object.entries(mapping).forEach(([key, id]) => {
    const el = document.getElementById(id);
    if (el && extracted[key] !== undefined && extracted[key] !== null) el.value = extracted[key];
  });
}

if (resetUploadBtn) {
  resetUploadBtn.addEventListener('click', () => {
    step2.style.display = 'none';
    uploadZone.style.display = 'block';
    uploadError.style.display = 'none';
    if (uploadTips) uploadTips.style.display = 'block';
    if (fileInput) fileInput.value = '';
    if (extractedForm) extractedForm.reset();
  });
}

if (extractedForm) {
  extractedForm.addEventListener('submit', async e => {
    e.preventDefault();
    const fd   = new FormData(extractedForm);
    const data = {};
    fd.forEach((v, k) => { if (v.trim()) data[k] = v.trim(); });
    const btn = extractedForm.querySelector('[type="submit"]');
    btn.classList.add('btn-loading'); btn.disabled = true;
    try {
      const res  = await fetch('/api/analyze', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify(data) });
      const result = await res.json();
      if (result.record_id) {
        window.location.href = `/report/${result.record_id}`;
      }
    } catch(e) {
      alert('Analysis failed. Please try again.');
    } finally {
      btn.classList.remove('btn-loading'); btn.disabled = false;
    }
  });
}
