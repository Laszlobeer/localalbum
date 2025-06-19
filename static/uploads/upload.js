document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    
    // Handle drag events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropZone.classList.add('dragover');
    }
    
    function unhighlight() {
        dropZone.classList.remove('dragover');
    }
    
    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            fileInput.files = files;
            updateFileInfo(files[0]);
        }
    }
    
    // Handle file selection via input
    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            updateFileInfo(this.files[0]);
        }
    });
    
    // Update file info display
    function updateFileInfo(file) {
        fileName.textContent = file.name;
        fileInfo.style.display = 'flex';
    }
    
    // Theme persistence for upload page
    const themeBtns = document.querySelectorAll('.theme-btn');
    const root = document.documentElement;
    
    // Function to set theme
    function setTheme(themeName) {
        // Remove active class from all buttons
        themeBtns.forEach(btn => btn.classList.remove('active'));
        
        // Add active class to selected button
        document.querySelector(`.theme-btn[data-theme="${themeName}"]`).classList.add('active');
        
        // Set CSS variables based on theme
        switch(themeName) {
            case 'dark':
                root.style.setProperty('--theme-primary', '#7c4dff');
                root.style.setProperty('--theme-secondary', '#5e35b1');
                root.style.setProperty('--theme-background', '#0a0a0a');
                root.style.setProperty('--theme-card', '#171717');
                root.style.setProperty('--theme-text', '#f5f5f5');
                root.style.setProperty('--theme-text-secondary', '#b3b3b3');
                break;
            case 'light':
                root.style.setProperty('--theme-primary', '#6200ea');
                root.style.setProperty('--theme-secondary', '#3700b3');
                root.style.setProperty('--theme-background', '#f5f5f5');
                root.style.setProperty('--theme-card', '#ffffff');
                root.style.setProperty('--theme-text', '#212121');
                root.style.setProperty('--theme-text-secondary', '#666666');
                break;
            case 'ocean':
                root.style.setProperty('--theme-primary', '#2196F3');
                root.style.setProperty('--theme-secondary', '#0D47A1');
                root.style.setProperty('--theme-background', '#001f3f');
                root.style.setProperty('--theme-card', '#003366');
                root.style.setProperty('--theme-text', '#e0f7fa');
                root.style.setProperty('--theme-text-secondary', '#81d4fa');
                break;
            case 'forest':
                root.style.setProperty('--theme-primary', '#4CAF50');
                root.style.setProperty('--theme-secondary', '#1B5E20');
                root.style.setProperty('--theme-background', '#0d1f0c');
                root.style.setProperty('--theme-card', '#1b3c1a');
                root.style.setProperty('--theme-text', '#e8f5e9');
                root.style.setProperty('--theme-text-secondary', '#a5d6a7');
                break;
            case 'sunset':
                root.style.setProperty('--theme-primary', '#FF9800');
                root.style.setProperty('--theme-secondary', '#E65100');
                root.style.setProperty('--theme-background', '#2c1a1d');
                root.style.setProperty('--theme-card', '#4a2b2f');
                root.style.setProperty('--theme-text', '#fff3e0');
                root.style.setProperty('--theme-text-secondary', '#ffcc80');
                break;
        }
        
        // Save theme to localStorage
        localStorage.setItem('theme', themeName);
    }
    
    // Event listeners for theme buttons
    themeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const theme = this.getAttribute('data-theme');
            setTheme(theme);
        });
    });
    
    // Check for saved theme or set default
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
});