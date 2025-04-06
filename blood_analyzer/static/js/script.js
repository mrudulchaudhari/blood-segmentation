document.addEventListener('DOMContentLoaded', function() {
    // Image preview functionality
    const fileInput = document.getElementById('file');
    const preview = document.getElementById('preview');
    
    if (fileInput && preview) {
        fileInput.addEventListener('change', function() {
            preview.innerHTML = '';
            
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    preview.appendChild(img);
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Animate confidence bars on results page
    const confidenceValue = document.querySelector('.confidence-value');
    if (confidenceValue) {
        const width = confidenceValue.style.width;
        confidenceValue.style.width = '0';
        
        setTimeout(() => {
            confidenceValue.style.transition = 'width 1s ease-out';
            confidenceValue.style.width = width;
        }, 300);
    }
    
    // Add hover effect for analysis items
    const analysisItems = document.querySelectorAll('.analysis-item, .history-card');
    analysisItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length) {
        setTimeout(() => {
            messages.forEach(message => {
                message.style.opacity = '0';
                message.style.transition = 'opacity 0.5s ease';
                
                setTimeout(() => {
                    message.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }
});