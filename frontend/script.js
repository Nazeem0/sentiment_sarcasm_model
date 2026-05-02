document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadSection = document.getElementById('upload-section');
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('results-section');
    const resetBtn = document.getElementById('reset-btn');

    // Tab elements
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // List elements
    const lists = {
        positive: document.getElementById('pos-list'),
        negative: document.getElementById('neg-list'),
        sarcastic: document.getElementById('sarc-list')
    };

    const counts = {
        positive: document.getElementById('pos-count'),
        negative: document.getElementById('neg-count'),
        sarcastic: document.getElementById('sarc-count')
    };

    // Drag and Drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    }

    function handleFileSelect(e) {
        if (e.target.files.length > 0) {
            uploadFile(e.target.files[0]);
        }
    }

    function uploadFile(file) {
        if (!file.name.endsWith('.csv')) {
            alert('Please upload a valid CSV file.');
            return;
        }

        // Show loading state
        dropZone.classList.add('hidden');
        loading.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:5001/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Server error'); });
            }
            return response.json();
        })
        .then(data => {
            displayResults(data);
            uploadSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error processing file: ' + error.message);
            dropZone.classList.remove('hidden');
            loading.classList.add('hidden');
        });
    }

    function getConfidenceClass(score) {
        if (score > 0.8) return 'high';
        if (score > 0.5) return 'med';
        return 'low';
    }

    function renderList(listElement, dataArray) {
        listElement.innerHTML = '';
        
        if (dataArray.length === 0) {
            listElement.innerHTML = '<li><p class="item-text" style="color: var(--text-secondary); text-align: center;">No items found for this category.</p></li>';
            return;
        }

        dataArray.forEach((item, index) => {
            const li = document.createElement('li');
            li.style.animationDelay = `${index * 0.05}s`;
            
            const confClass = getConfidenceClass(item.score);
            const confPercent = (item.score * 100).toFixed(1);

            li.innerHTML = `
                <p class="item-text">${item.text}</p>
                <div class="item-meta">
                    <span class="label">Detected: ${item.original_label}</span>
                    <span class="confidence ${confClass}">Confidence: ${confPercent}%</span>
                </div>
            `;
            listElement.appendChild(li);
        });
    }

    function displayResults(data) {
        // Update counts
        counts.positive.textContent = data.positive.length;
        counts.negative.textContent = data.negative.length;
        counts.sarcastic.textContent = data.sarcastic.length;

        // Render lists
        renderList(lists.positive, data.positive);
        renderList(lists.negative, data.negative);
        renderList(lists.sarcastic, data.sarcastic);
    }

    // Tab switching logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.add('hidden'));

            // Add active to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.remove('hidden');
        });
    });

    // Reset workflow
    resetBtn.addEventListener('click', () => {
        fileInput.value = ''; // Clear file input
        resultsSection.classList.add('hidden');
        uploadSection.classList.remove('hidden');
        dropZone.classList.remove('hidden');
        loading.classList.add('hidden');
    });

    // Real-time Tester Logic
    const testInput = document.getElementById('test-input');
    const testBtn = document.getElementById('test-btn');
    const testResult = document.getElementById('test-result');
    const resultLabel = document.getElementById('result-label');
    const resultConfidence = document.getElementById('result-confidence');

    testBtn.addEventListener('click', () => {
        const text = testInput.value.trim();
        if (!text) return;

        testBtn.disabled = true;
        testBtn.textContent = 'Testing...';

        fetch('http://127.0.0.1:5001/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            resultLabel.textContent = `Result: ${data.label}`;
            resultLabel.className = `label label-${data.label}`;
            
            const confPercent = (data.score * 100).toFixed(1);
            resultConfidence.textContent = `Confidence: ${confPercent}%`;
            
            testResult.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Prediction error: ' + error.message);
        })
        .finally(() => {
            testBtn.disabled = false;
            testBtn.textContent = 'Test Sentiment';
        });
    });

    // Also trigger on Enter key
    testInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') testBtn.click();
    });
});
