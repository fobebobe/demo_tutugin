
class CustomSlider {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        
        this.slides = this.container.querySelectorAll('.custom-slider-slide');
        this.currentIndex = 0;
        this.interval = null;
        this.autoPlayDelay = options.autoPlayDelay || 5000; 
        
        this.init();
    }
    
    init() {
        if (this.slides.length === 0) return;
        
    
        this.slides[0].classList.add('active');
        

        const prevBtn = this.container.querySelector('.btn-prev');
        const nextBtn = this.container.querySelector('.btn-next');
        
        if (prevBtn) prevBtn.addEventListener('click', () => this.prev());
        if (nextBtn) nextBtn.addEventListener('click', () => this.next());
        
     
        const dots = this.container.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => this.goTo(index));
        });
        
        
        this.startAutoPlay();
        
    
        this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
        this.container.addEventListener('mouseleave', () => this.startAutoPlay());
    }
    
    updateDots() {
        const dots = this.container.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            if (index === this.currentIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }
    
    showSlide(index) {
        if (index < 0) index = this.slides.length - 1;
        if (index >= this.slides.length) index = 0;
        
        this.slides.forEach(slide => {
            slide.classList.remove('active');
        });
        
  
        this.slides[index].classList.add('active');
        this.currentIndex = index;
        

        this.updateDots();
    }
    
    next() {
        this.showSlide(this.currentIndex + 1);
    }
    
    prev() {
        this.showSlide(this.currentIndex - 1);
    }
    
    goTo(index) {
        this.showSlide(index);
    }
    
    startAutoPlay() {
        if (this.autoPlayDelay > 0) {
            this.stopAutoPlay();
            this.interval = setInterval(() => this.next(), this.autoPlayDelay);
        }
    }
    
    stopAutoPlay() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const sliderContainer = document.getElementById('customSlider');
    if (sliderContainer) {
        new CustomSlider('customSlider', {
            autoPlayDelay: 5000
        });
    }
});