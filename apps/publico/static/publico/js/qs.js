    // Función para animar elementos cuando aparecen en la pantalla
    document.addEventListener('DOMContentLoaded', function() {
      // Obtener todos los elementos con la clase fade-in
      const fadeElements = document.querySelectorAll('.fade-in');
      
      // Función para verificar si un elemento está en el viewport
      const isInViewport = (element) => {
        const rect = element.getBoundingClientRect();
        return (
          rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.85 &&
          rect.bottom >= 0
        );
      };
      
      // Función para animar elementos visibles
      const animateOnScroll = () => {
        fadeElements.forEach(el => {
          if (isInViewport(el)) {
            el.classList.add('appear');
          }
        });
      };
      
      // Iniciar animación de elementos visibles al cargar la página
      animateOnScroll();
      
      // Animar elementos cuando se hace scroll
      window.addEventListener('scroll', animateOnScroll);
      
      // Contador de estadísticas
      const counters = document.querySelectorAll('.counter');
      const speed = 200; // Velocidad de la animación (ms)
      
      const animateCounter = () => {
        counters.forEach(counter => {
          if (isInViewport(counter)) {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            
            // Calcular incremento
            const inc = target / speed;
            
            if (count < target) {
              // Incrementar el contador y actualizar el valor
              counter.innerText = Math.ceil(count + inc);
              // Llamar a la función nuevamente
              setTimeout(animateCounter, 1);
            } else {
              // Asegurarse de que el valor final sea exactamente el target
              counter.innerText = target;
            }
          }
        });
      };
      
      // Iniciar animación de contadores cuando sean visibles
      window.addEventListener('scroll', () => {
        counters.forEach(counter => {
          if (isInViewport(counter) && counter.innerText === '0') {
            animateCounter();
          }
        });
      });
      
      // Verificar contadores al cargar la página
      counters.forEach(counter => {
        if (isInViewport(counter)) {
          animateCounter();
        }
      });
    });
    
    // Animación para la línea de tiempo
    document.addEventListener('DOMContentLoaded', function() {
      const timelineItems = document.querySelectorAll('.timeline-item');
      
      const animateTimeline = () => {
        timelineItems.forEach((item, index) => {
          // Verificar si el elemento está en el viewport
          const rect = item.getBoundingClientRect();
          const isVisible = rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.85 && rect.bottom >= 0;
          
          if (isVisible) {
            // Añadir clase con un retraso basado en el índice
            setTimeout(() => {
              item.classList.add('opacity-100', 'translate-y-0');
              
              // Animar el círculo
              const dot = item.querySelector('.timeline-dot');
              dot.classList.add('scale-110');
              setTimeout(() => {
                dot.classList.remove('scale-110');
              }, 300);
            }, index * 300);
          }
        });
      };
      
      // Configurar estados iniciales
      timelineItems.forEach(item => {
        item.classList.add('opacity-0', 'translate-y-10', 'transition-all', 'duration-500', 'ease-in-out');
      });
      
      // Ejecutar animación al cargar y al hacer scroll
      animateTimeline();
      window.addEventListener('scroll', animateTimeline);
    });
    
    // Efecto de parallax para los fondos
    window.addEventListener('scroll', function() {
      const sections = document.querySelectorAll('section');
      sections.forEach(section => {
        const scrollPosition = window.pageYOffset;
        // Aplicar un sutil efecto parallax
        section.style.backgroundPositionY = scrollPosition * 0.05 + 'px';
      });
    });