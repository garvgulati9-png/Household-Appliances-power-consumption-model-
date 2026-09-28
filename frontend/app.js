// ==========================================================================
// HOUSEHOLD POWER CONSUMPTION ML SYSTEM - CLIENT CONTROLLER
// Project Authors: Garv Gulati, Umang Gupta, Nikhil Goyal
// Architecture: Stacked Hybrid Super-Learner & Multi-Tier Anomaly Engine
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  initTabNavigation();
  initHeroSlideshow();
  initFormControls();
  initPaperTestControls();
  initDatasetSwitcher();
  fetchInitialData();
  
  // Trigger initial predictions so all cards display active data immediately
  triggerPrediction();
  triggerPaperTest();
});

// 1. Navigation & Tab Switcher
function initTabNavigation() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      switchToTab(tab.dataset.tab);
    });
  });

  const btnPrint = document.getElementById('btn-print-paper');
  if (btnPrint) {
    btnPrint.addEventListener('click', () => {
      window.print();
    });
  }
}

window.switchToTab = function(tabId) {
  const tabs = document.querySelectorAll('.nav-tab');
  const panes = document.querySelectorAll('.tab-pane');

  tabs.forEach(t => {
    t.classList.toggle('active', t.dataset.tab === tabId);
  });

  panes.forEach(p => {
    p.classList.toggle('active', p.id === tabId);
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// 2. Hero Image Slideshow Carousel
function initHeroSlideshow() {
  const slides = document.querySelectorAll('#hero-slideshow .slide');
  const dots = document.querySelectorAll('#slide-dots .dot');
  const prevBtn = document.getElementById('slide-prev');
  const nextBtn = document.getElementById('slide-next');
  const container = document.getElementById('hero-slideshow');

  if (!slides.length) return;

  let currentSlide = 0;
  let slideInterval = null;

  function showSlide(index) {
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));

    currentSlide = (index + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
    if (dots[currentSlide]) {
      dots[currentSlide].classList.add('active');
    }
  }

  function nextSlide() {
    showSlide(currentSlide + 1);
  }

  function prevSlide() {
    showSlide(currentSlide - 1);
  }

  if (nextBtn) nextBtn.addEventListener('click', nextSlide);
  if (prevBtn) prevBtn.addEventListener('click', prevSlide);

  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      showSlide(parseInt(dot.dataset.index, 10));
    });
  });

  function startAutoplay() {
    slideInterval = setInterval(nextSlide, 5000);
  }

  function stopAutoplay() {
    if (slideInterval) clearInterval(slideInterval);
  }

  if (container) {
    container.addEventListener('mouseenter', stopAutoplay);
    container.addEventListener('mouseleave', startAutoplay);
  }

  startAutoplay();
}

// 3. Primary ML Model Form Controls (Original 19,735-Row Dataset Model)
function initFormControls() {
  const hourSlider = document.getElementById('input-hour');
  const tempIndoorSlider = document.getElementById('input-temp-indoor');
  const tempLivingSlider = document.getElementById('input-temp-living');
  const humidityIndoorSlider = document.getElementById('input-humidity-indoor');
  const tempOutdoorSlider = document.getElementById('input-temp-outdoor');
  const windspeedSlider = document.getElementById('input-windspeed');
  const pressureSlider = document.getElementById('input-pressure');

  const valHour = document.getElementById('val-hour');
  const valTempIndoor = document.getElementById('val-temp-indoor');
  const valTempLiving = document.getElementById('val-temp-living');
  const valHumidityIndoor = document.getElementById('val-humidity-indoor');
  const valTempOutdoor = document.getElementById('val-temp-outdoor');
  const valWindspeed = document.getElementById('val-windspeed');
  const valPressure = document.getElementById('val-pressure');

  if (hourSlider) {
    hourSlider.addEventListener('input', (e) => {
      const hr = parseInt(e.target.value, 10);
      const suffix = hr >= 12 ? 'PM' : 'AM';
      const displayHr = hr % 12 === 0 ? 12 : hr % 12;
      valHour.textContent = `${displayHr}:00 ${suffix} (${hr.toString().padStart(2, '0')}:00)`;
      triggerPrediction();
    });
  }

  if (tempIndoorSlider) {
    tempIndoorSlider.addEventListener('input', (e) => {
      valTempIndoor.textContent = `${parseFloat(e.target.value).toFixed(1)} °C`;
      triggerPrediction();
    });
  }

  if (tempLivingSlider) {
    tempLivingSlider.addEventListener('input', (e) => {
      valTempLiving.textContent = `${parseFloat(e.target.value).toFixed(1)} °C`;
      triggerPrediction();
    });
  }

  if (humidityIndoorSlider) {
    humidityIndoorSlider.addEventListener('input', (e) => {
      valHumidityIndoor.textContent = `${parseFloat(e.target.value).toFixed(1)} %`;
      triggerPrediction();
    });
  }

  if (tempOutdoorSlider) {
    tempOutdoorSlider.addEventListener('input', (e) => {
      valTempOutdoor.textContent = `${parseFloat(e.target.value).toFixed(1)} °C`;
      triggerPrediction();
    });
  }

  if (windspeedSlider) {
    windspeedSlider.addEventListener('input', (e) => {
      valWindspeed.textContent = `${parseFloat(e.target.value).toFixed(1)} m/s`;
      triggerPrediction();
    });
  }

  if (pressureSlider) {
    pressureSlider.addEventListener('input', (e) => {
      valPressure.textContent = `${parseInt(e.target.value, 10)} mm`;
      triggerPrediction();
    });
  }

  const btnPredict = document.getElementById('btn-run-predict');
  if (btnPredict) {
    btnPredict.addEventListener('click', triggerPrediction);
  }
}

// Preset Handler for Primary Model
window.applyPreset = function(type) {
  const hourSlider = document.getElementById('input-hour');
  const tempIndoorSlider = document.getElementById('input-temp-indoor');
  const tempLivingSlider = document.getElementById('input-temp-living');
  const humidityIndoorSlider = document.getElementById('input-humidity-indoor');
  const tempOutdoorSlider = document.getElementById('input-temp-outdoor');
  const windspeedSlider = document.getElementById('input-windspeed');
  const pressureSlider = document.getElementById('input-pressure');

  const presets = {
    evening: { hour: 18, temp_in: 21.5, temp_liv: 22.0, hum: 48, temp_out: 14.0, wind: 4.0, press: 755 },
    morning: { hour: 8, temp_in: 20.0, temp_liv: 20.5, hum: 55, temp_out: 10.0, wind: 3.0, press: 758 },
    standby: { hour: 3, temp_in: 18.5, temp_liv: 18.0, hum: 42, temp_out: 7.0, wind: 1.5, press: 762 },
    spike:   { hour: 19, temp_in: 26.0, temp_liv: 27.5, hum: 78, temp_out: 32.0, wind: 9.0, press: 742 }
  };

  const p = presets[type];
  if (!p) return;

  hourSlider.value = p.hour;
  tempIndoorSlider.value = p.temp_in;
  tempLivingSlider.value = p.temp_liv;
  humidityIndoorSlider.value = p.hum;
  tempOutdoorSlider.value = p.temp_out;
  windspeedSlider.value = p.wind;
  pressureSlider.value = p.press;

  // Update labels
  const suffix = p.hour >= 12 ? 'PM' : 'AM';
  const displayHr = p.hour % 12 === 0 ? 12 : p.hour % 12;
  document.getElementById('val-hour').textContent = `${displayHr}:00 ${suffix} (${p.hour.toString().padStart(2, '0')}:00)`;
  document.getElementById('val-temp-indoor').textContent = `${p.temp_in.toFixed(1)} °C`;
  document.getElementById('val-temp-living').textContent = `${p.temp_liv.toFixed(1)} °C`;
  document.getElementById('val-humidity-indoor').textContent = `${p.hum.toFixed(1)} %`;
  document.getElementById('val-temp-outdoor').textContent = `${p.temp_out.toFixed(1)} °C`;
  document.getElementById('val-windspeed').textContent = `${p.wind.toFixed(1)} m/s`;
  document.getElementById('val-pressure').textContent = `${p.press} mm`;

  // Update preset button active state
  document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
  if (event && event.target) {
    event.target.classList.add('active');
  }

  triggerPrediction();
};

// Execute Primary Model Inference
async function triggerPrediction() {
  const hour = parseInt(document.getElementById('input-hour').value, 10);
  const tempIndoor = parseFloat(document.getElementById('input-temp-indoor').value);
  const tempLiving = parseFloat(document.getElementById('input-temp-living').value);
  const humidityIndoor = parseFloat(document.getElementById('input-humidity-indoor').value);
  const tempOutdoor = parseFloat(document.getElementById('input-temp-outdoor').value);
  const windspeed = parseFloat(document.getElementById('input-windspeed').value);
  const pressure = parseFloat(document.getElementById('input-pressure').value);

  const payload = {
    hour: hour,
    minute: 0,
    temp_indoor: tempIndoor,
    temp_living: tempLiving,
    humidity_indoor: humidityIndoor,
    temp_outdoor: tempOutdoor,
    windspeed: windspeed,
    pressure: pressure,
    day: 15,
    month: 3,
    weekday: 2
  };

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Primary Model Prediction API Error');
    const data = await res.json();
    renderPredictionResults(data);
  } catch (err) {
    console.error('Error running primary prediction:', err);
  }
}

function renderPredictionResults(data) {
  const primary = data.primary_output;
  const preds = data.predictions;

  // 1. Primary Output Animate Counter
  const whElem = document.getElementById('pred-primary-wh');
  if (whElem) {
    animateCounter(whElem, primary.predicted_wh);
  }

  const kwElem = document.getElementById('pred-primary-kw');
  if (kwElem) {
    kwElem.textContent = `${primary.predicted_kw.toFixed(3)} kW`;
  }

  // 2. Sub-models in ensemble
  const etrElem = document.getElementById('pred-sub-etr');
  if (etrElem && preds['ExtraTrees Regressor']) {
    etrElem.textContent = `${preds['ExtraTrees Regressor'].toFixed(2)} Wh`;
  }

  const xgbElem = document.getElementById('pred-sub-xgb');
  if (xgbElem && preds['XGBoost Regressor']) {
    xgbElem.textContent = `${preds['XGBoost Regressor'].toFixed(2)} Wh`;
  }

  const hgbElem = document.getElementById('pred-sub-hgb');
  if (hgbElem && preds['HistGradientBoosting']) {
    hgbElem.textContent = `${preds['HistGradientBoosting'].toFixed(2)} Wh`;
  }

  // 3. Multi-tier Anomaly Engine Diagnostics
  const banner = document.getElementById('anomaly-banner');
  const textElem = document.getElementById('anomaly-text');
  const isoStatus = document.getElementById('iso-status');

  if (banner && textElem && isoStatus) {
    if (data.anomaly_diagnostics.is_anomaly) {
      banner.classList.add('is-anomaly');
      banner.querySelector('.status-icon').textContent = '⚠';
      textElem.textContent = 'Anomaly Alert: Reading outside dynamic residual confidence bounds';
      isoStatus.textContent = 'Anomaly Flagged';
      isoStatus.className = 'mini-value text-rose';
    } else {
      banner.classList.remove('is-anomaly');
      banner.querySelector('.status-icon').textContent = '✓';
      textElem.textContent = 'Nominal Household Signature (Within 2σ Envelope)';
      isoStatus.textContent = 'Normal Signature';
      isoStatus.className = 'mini-value text-emerald';
    }
  }
}

// 4. Interactive Cross-Dataset Test Workbench Controls (Paper Dataset 200 Rows)
function initPaperTestControls() {
  const timeSlider = document.getElementById('paper-input-time');
  const tempSlider = document.getElementById('paper-input-temp');
  const occupantsSlider = document.getElementById('paper-input-occupants');
  const housingSelect = document.getElementById('paper-input-housing');
  const acSelect = document.getElementById('paper-input-ac');
  const usageSelect = document.getElementById('paper-input-usage');

  const valTime = document.getElementById('paper-val-time');
  const valTemp = document.getElementById('paper-val-temp');
  const valOccupants = document.getElementById('paper-val-occupants');

  if (timeSlider) {
    timeSlider.addEventListener('input', (e) => {
      const hr = parseInt(e.target.value, 10);
      const suffix = hr >= 12 ? 'PM' : 'AM';
      const displayHr = hr % 12 === 0 ? 12 : hr % 12;
      valTime.textContent = `${displayHr}:00 ${suffix} (${hr.toString().padStart(2, '0')}:00)`;
      triggerPaperTest();
    });
  }

  if (tempSlider) {
    tempSlider.addEventListener('input', (e) => {
      valTemp.textContent = `${parseFloat(e.target.value).toFixed(1)} °C`;
      triggerPaperTest();
    });
  }

  if (occupantsSlider) {
    occupantsSlider.addEventListener('input', (e) => {
      const count = parseInt(e.target.value, 10);
      valOccupants.textContent = `${count} ${count === 1 ? 'Person' : 'People'}`;
      triggerPaperTest();
    });
  }

  if (housingSelect) housingSelect.addEventListener('change', triggerPaperTest);
  if (acSelect) acSelect.addEventListener('change', triggerPaperTest);
  if (usageSelect) usageSelect.addEventListener('change', triggerPaperTest);

  const btnPaperTest = document.getElementById('btn-run-paper-test');
  if (btnPaperTest) {
    btnPaperTest.addEventListener('click', triggerPaperTest);
  }
}

window.applyPaperPreset = function(type) {
  const timeSlider = document.getElementById('paper-input-time');
  const tempSlider = document.getElementById('paper-input-temp');
  const occupantsSlider = document.getElementById('paper-input-occupants');
  const housingSelect = document.getElementById('paper-input-housing');
  const acSelect = document.getElementById('paper-input-ac');
  const usageSelect = document.getElementById('paper-input-usage');

  const presets = {
    typical_family: { time: 18, temp: 22.0, occupants: 4, housing: 'House', ac: '1', usage: 'Moderate' },
    high_ac:        { time: 15, temp: 31.5, occupants: 5, housing: 'Duplex', ac: '1', usage: 'High' },
    low_compact:    { time: 23, temp: 17.0, occupants: 1, housing: 'Apartment', ac: '0', usage: 'Low' }
  };

  const p = presets[type];
  if (!p) return;

  timeSlider.value = p.time;
  tempSlider.value = p.temp;
  occupantsSlider.value = p.occupants;
  housingSelect.value = p.housing;
  acSelect.value = p.ac;
  usageSelect.value = p.usage;

  const suffix = p.time >= 12 ? 'PM' : 'AM';
  const displayHr = p.time % 12 === 0 ? 12 : p.time % 12;
  document.getElementById('paper-val-time').textContent = `${displayHr}:00 ${suffix} (${p.time.toString().padStart(2, '0')}:00)`;
  document.getElementById('paper-val-temp').textContent = `${p.temp.toFixed(1)} °C`;
  document.getElementById('paper-val-occupants').textContent = `${p.occupants} People`;

  document.querySelectorAll('#tab-benchmarks .btn-preset').forEach(b => b.classList.remove('active'));
  if (event && event.target) {
    event.target.classList.add('active');
  }

  triggerPaperTest();
};

async function triggerPaperTest() {
  const time = parseFloat(document.getElementById('paper-input-time')?.value || 18);
  const temp = parseFloat(document.getElementById('paper-input-temp')?.value || 22);
  const occupants = parseFloat(document.getElementById('paper-input-occupants')?.value || 4);
  const housing = document.getElementById('paper-input-housing')?.value || 'House';
  const ac = document.getElementById('paper-input-ac')?.value === '1';
  const usage = document.getElementById('paper-input-usage')?.value || 'Moderate';

  const payload = {
    user_id: 100,
    time: time,
    temperature: temp,
    occupants: occupants,
    housing_type: housing,
    ac_room: ac,
    device_usage: usage
  };

  try {
    const res = await fetch('/api/predict_paper_test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Paper Test API Error');
    const data = await res.json();
    const p = data.predictions;

    document.getElementById('paper-pred-svm').textContent = `${p['Support Vector Machine (SVR)'].toFixed(3)} kW`;
    document.getElementById('paper-pred-lr').textContent = `${p['Linear Regression (OLS)'].toFixed(3)} kW`;
    document.getElementById('paper-pred-xgb').textContent = `${p['XGBoost (Regularized)'].toFixed(3)} kW`;
    document.getElementById('paper-pred-rf').textContent = `${p['Random Forest'].toFixed(3)} kW`;
    document.getElementById('paper-pred-mlp').textContent = `${p['Deep Neural Network (MLP)'].toFixed(3)} kW`;
    document.getElementById('paper-pred-ens').textContent = `${p['Cross-Dataset Ensemble'].toFixed(3)} kW`;
  } catch (err) {
    console.error('Error in paper test:', err);
  }
}

// 5. Dataset View Switcher (Paper 200 Rows vs Primary 19,735 Rows)
function initDatasetSwitcher() {
  const btnPaper = document.getElementById('btn-show-paper-ds');
  const btnUci = document.getElementById('btn-show-uci-ds');
  const viewPaper = document.getElementById('view-paper-dataset');
  const viewUci = document.getElementById('view-uci-dataset');

  if (btnPaper && btnUci && viewPaper && viewUci) {
    btnPaper.addEventListener('click', () => {
      btnPaper.classList.add('active');
      btnUci.classList.remove('active');
      viewPaper.classList.add('active');
      viewUci.classList.remove('active');
    });

    btnUci.addEventListener('click', () => {
      btnUci.classList.add('active');
      btnPaper.classList.remove('active');
      viewUci.classList.add('active');
      viewPaper.classList.remove('active');
    });
  }
}

// 6. Fetch Dataset Summaries & Paper Markdown
async function fetchInitialData() {
  // Load Paper Dataset Summary
  try {
    const dsRes = await fetch('/api/dataset_summary');
    const ds = await dsRes.json();
    const statsBody = document.getElementById('dataset-stats-body');
    if (statsBody && ds.statistics) {
      statsBody.innerHTML = '';
      ds.statistics.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${s.index}</strong></td>
          <td>${s.count}</td>
          <td>${parseFloat(s.mean).toFixed(2)}</td>
          <td>${parseFloat(s.std).toFixed(2)}</td>
          <td>${parseFloat(s.min).toFixed(2)}</td>
          <td>${parseFloat(s['25%']).toFixed(2)}</td>
          <td>${parseFloat(s['50%']).toFixed(2)}</td>
          <td>${parseFloat(s['75%']).toFixed(2)}</td>
          <td>${parseFloat(s.max).toFixed(2)}</td>
        `;
        statsBody.appendChild(tr);
      });
    }
  } catch (err) {
    console.error('Failed to load paper dataset summary:', err);
  }

  // Load Primary Smart Home Telemetry Summary (19,735 rows)
  try {
    const uciRes = await fetch('/api/uci_summary');
    const uci = await uciRes.json();
    const uciBody = document.getElementById('uci-stats-body');
    if (uciBody && uci.statistics) {
      uciBody.innerHTML = '';
      uci.statistics.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${s.index}</strong></td>
          <td>${s.count}</td>
          <td>${parseFloat(s.mean).toFixed(2)}</td>
          <td>${parseFloat(s.std).toFixed(2)}</td>
          <td>${parseFloat(s.min).toFixed(2)}</td>
          <td>${parseFloat(s['25%']).toFixed(2)}</td>
          <td>${parseFloat(s['50%']).toFixed(2)}</td>
          <td>${parseFloat(s['75%']).toFixed(2)}</td>
          <td>${parseFloat(s.max).toFixed(2)}</td>
        `;
        uciBody.appendChild(tr);
      });
    }
  } catch (err) {
    console.error('Failed to load primary dataset summary:', err);
  }

  // Load Research Paper Markdown
  try {
    const paperRes = await fetch('/api/paper_text');
    const paperData = await paperRes.json();
    const container = document.getElementById('paper-content-render');
    if (container) {
      if (window.marked) {
        container.innerHTML = marked.parse(paperData.content);
      } else {
        container.innerText = paperData.content;
      }
    }
  } catch (err) {
    console.error('Failed to load paper markdown:', err);
  }
}

// Counter Animation Utility
function animateCounter(elem, targetVal) {
  const duration = 300;
  const startVal = parseFloat(elem.textContent) || 89.66;
  const startTime = performance.now();

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1.0);
    const cur = startVal + (targetVal - startVal) * progress;
    elem.textContent = cur.toFixed(2);
    if (progress < 1.0) {
      requestAnimationFrame(update);
    }
  }
  requestAnimationFrame(update);
}
